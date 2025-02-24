import os
import json
import asyncio
import requests
import logging
from dotenv import load_dotenv
from django.conf import settings
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from django.contrib.auth import get_user_model
from movies.models import Movie, Genre, MoviePreference, GenrePreference
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

User = get_user_model()

load_dotenv()
logger = logging.getLogger(__name__)

# ElevenLabs API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
print(f"{ELEVENLABS_API_KEY}")

# Voice IDs (각 인물별)
ANSUNGJAE_VOICE_ID = "rTsJeYsqsSoHL7m9QbIV"
PAIKJONGWON_VOICE_ID = "zPEmr71Vsf4rNSF8d2Fs"

# FAISS 벡터 DB 로드
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = FAISS.load_local(
    folder_path="../dataset/",
    index_name="index",
    embeddings=embeddings,
    allow_dangerous_deserialization=True,
)
db = vectorstore

# LLM 모델 설정
llm = ChatOpenAI(model="gpt-4o")


class ChatConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_user_from_token(self, token_string):
        try:
            # 토큰 검증
            access_token = AccessToken(token_string)
            user_id = access_token.payload.get("user_id")

            # 사용자 조회
            return User.objects.get(id=user_id)
        except (TokenError, User.DoesNotExist) as e:
            logger.error(f"토큰 검증 실패: {str(e)}")
            return None

    async def connect(self):
        # URL 쿼리 파라미터에서 토큰 추출
        query_string = self.scope.get("query_string", b"").decode()
        token = dict(pair.split("=") for pair in query_string.split("&") if pair).get(
            "token"
        )

        if not token:
            logger.error("❌ 토큰이 없습니다.")
            await self.close()
            return

        # 토큰으로 사용자 인증
        self.user = await self.get_user_from_token(token)
        if not self.user:
            logger.error("❌ 유효하지 않은 토큰입니다.")
            await self.close()
            return

        await self.accept()
        logger.info(f"✅ 사용자 {self.user.username} 연결됨")

    @database_sync_to_async
    def get_user_preferences(self):
        # 사용자가 좋아하는 장르 조회
        genre_preferences = GenrePreference.objects.filter(
            user_id_fk=self.user, preference_type="like"
        ).values_list("genre_id", flat=True)

        # 사용자가 좋아하는 영화 조회
        movie_preferences = MoviePreference.objects.filter(
            user_id_fk=self.user, preference_type="like"
        ).values_list("movie_id_fk__title", flat=True)

        return list(genre_preferences), list(movie_preferences)

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        question = data.get("message", "")

        # 사용자의 선호도 정보 조회
        preferred_genres, preferred_movies = await self.get_user_preferences()

        if not question:
            await self.send(text_data=json.dumps({"error": "질문이 없습니다."}))
            return

        # 벡터 검색 및 GPT 호출
        response = await self.get_movie_recommendation(
            question, preferred_genres, preferred_movies
        )

        # 음성 변환 실행
        ansungjae_audio = await self.text_to_speech(
            response["ansungjae"], ANSUNGJAE_VOICE_ID
        )
        paikjongwon_audio = await self.text_to_speech(
            response["paikjongwon"], PAIKJONGWON_VOICE_ID
        )

        # 결과 전송
        await self.send(
            text_data=json.dumps(
                {
                    "ansungjae_text": response["ansungjae"],
                    "paikjongwon_text": response["paikjongwon"],
                    "ansungjae_audio": ansungjae_audio,
                    "paikjongwon_audio": paikjongwon_audio,
                }
            )
        )

    async def genre_weighted_mmr_search(self, query, preferred_genre, k=20):
        retriever = db.as_retriever(
            search_type="mmr", search_kwargs={"k": k, "fetch_k": 10, "lambda_mult": 0.1}
        )

        preferred_count = int(k * 0.6)
        general_count = k - preferred_count

        preferred_filter = {"genre": {"$eq": preferred_genre}}

        preferred_docs = await asyncio.to_thread(
            retriever.get_relevant_documents,
            query,
            filter=preferred_filter,
            k=preferred_count,
        )
        all_docs = await asyncio.to_thread(
            retriever.get_relevant_documents, query, k=general_count + 10
        )
        general_docs = [
            doc for doc in all_docs if doc.metadata.get("genre") != preferred_genre
        ][:general_count]

        return preferred_docs + general_docs

    async def get_movie_recommendation(self, query, preferred_genres, preferred_movies):
        retrieved_docs = await self.genre_weighted_mmr_search(query, preferred_genres)
        formatted_context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        prompt = ChatPromptTemplate.from_template(
            """
넌 영화를 추천하는 AI야. 너는 안성재 셰프와 백종원 사업가 2명의 입장에서 각각 1개의 영화를 추천해야해.
입력받은 {preferred_genres}, {preferred_movies}와 유사한 영화를 추천해줘. 단, 아예 똑같은 영화는 추천하지 말아줘.
먼저, 안성재 셰프는 다양성이 높은 예술적인 영화를 좋아하는 성격이야.
안성재 셰프의 입장에서 예술적이고 새로운 영화를 1개 추천해줘.
말투에 영화 관련 특성의 익힘정도가 완벽하다는 내용을 포함해줘.
또, 영화 내용과 관련해서 동일한 점이 있으면 이븐하게 되었다는 표현을 자주 사용해줘.
마지막에 백종원씨에게 '오늘 영화 메뉴는 무엇인가요?" 라고 대화를 마무리해줘.                                         
두번째로, 백종원 사업가는 대중적이고 인기가 많은 영화를 좋아하는 스타일이야.
백종원 사업가의 입장에서 대중적이고 인기가 많은 영화를 1개 추천해줘.
영화를 소개할 때, 중간에 "조보아씨 이리 내려와서 이것좀 봐봐유"라는 내용을 추가해줘
fewshot 예시처럼 사용자가 {question}을 입력하면 영어로 번역해서 조회한 뒤, response를 한글로 출력해줘.
답변은 response만 반드시 출력해줘.
이제 나의 말에 대답하도록 해. \
오로지 아래의 context 기반으로 질문에 fewshot 형태로 대답하세요
fewshot:
1. 'question': "커플이 함께 볼 로맨스 영화를 추천해줘"
   'response': 안성재 셰프: "음~ 저는 영화의 예술성 익힘 정도가 완벽한 '노트북'을 추천해드릴게요.\n 
                    두 주인공의 사랑이 이븐하게 느껴지는군요. 커플과 함께 예술성이 높은 SF 로맨스 이야기 한번 맛보세요.\n 
                    백종원씨, 오늘 영화 메뉴는 무엇인가요?"\n 
                                           
        백종원 사업가:"오늘 영화 메뉴는 맛있는 '라라랜드'지 말이에유.\n  전세계 로맨스중 인기는 탑이어유.\n  낭만적인 음악과 댄스, 아주 좋구만유.\n 
                    조보아씨 이리 내려와서 이것좀 봐봐유, 아주 기가막히쥬.\n 
                    오늘 백종원의 영화 메뉴 추천은 음악과 낭만의 영화 '라라랜드'에유."

2. 'question': "친구가 함께 볼 액션 영화를 추천해줘"
   'response': 안성재 셰프: "음~ 저는 영화의 예술성 익힘 정도가 완벽한 '본레거시'를 추천해드릴게요.\n  
                    멧 데이먼의 촬영 기법과 액션 디렉팅이 정말 예술적이네요.\n  친구와 함께 예술성이 높은 액션 이야기 한번 맛보세요.\n 
                    백종원씨, 오늘 영화 메뉴는 무엇인가요?"\n 
                                           
        백종원 사업가:"오늘 영화 메뉴는 맛있는 '미션 임파서블'이지 말이에유.\n  전세계 액션영화 중 인기는 탑이어유. \n 유명한 BGM과 말도안되는 액션, 아주 신나구만유.\n 
                    조보아씨 이리 내려와서 이것좀 봐봐유, 아주 기가막히쥬.\n 
{preferred_genres}
{preferred_movies}
{context}
질문:
{question} """
        )

        response = await asyncio.to_thread(
            llm.invoke,
            prompt.format(
                context=formatted_context,
                question=query,
                preferred_genres=preferred_genres,
                preferred_movies=preferred_movies,
            ),
        )

        response_text = response.content

        try:
            an_response = response_text.split("백종원 사업가:")[0].strip()
            paik_response = (
                "백종원 사업가:" + response_text.split("백종원 사업가:")[1].strip()
            )
        except IndexError:
            an_response, paik_response = (
                response_text,
                "추천 결과를 생성할 수 없습니다.",
            )

        return {"ansungjae": an_response, "paikjongwon": paik_response}

    async def text_to_speech(self, text, voice_id):
        """ElevenLabs API를 사용해 텍스트를 음성으로 변환"""
        if not ELEVENLABS_API_KEY:
            logger.error("❌ ElevenLabs API 키가 설정되지 않았습니다.")
            return None

        if not text or not text.strip():
            logger.error("❌ 변환할 텍스트가 없습니다.")
            return None

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {"xi-api-key": ELEVENLABS_API_KEY, "Content-Type": "application/json"}
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 1,
                "style": 0.8,
                "use_speaker_boost": True,
            },
        }

        try:
            response = await asyncio.to_thread(
                requests.post, url, json=data, headers=headers
            )
            response.raise_for_status()

            audio_content = response.content
            audio_filename = f"tts_output_{voice_id}.mp3"
            media_path = os.path.join(settings.MEDIA_ROOT, audio_filename)

            # media 디렉토리가 없으면 생성
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            with open(media_path, "wb") as f:
                f.write(audio_content)

            # URL 경로 수정
            audio_url = f"{settings.MEDIA_URL}{audio_filename}".replace("//", "/")
            print(f"생성된 오디오 파일 : {audio_url}")
            return audio_url
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ ElevenLabs API 호출 오류: {str(e)}")
            return None
