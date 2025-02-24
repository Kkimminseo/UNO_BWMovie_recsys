import json
import openai
import logging
import numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-4o")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = FAISS.load_local(
    folder_path="../dataset",
    index_name="index",
    embeddings=embeddings,
    allow_dangerous_deserialization=True,
)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """WebSocket 연결 요청이 오면 실행"""
        print("WebSocket 연결 시도")
        await self.accept()
        print("✅ WebSocket 연결 성공!")  # ✅ 연결 로그 추가

    async def disconnect(self, close_code):
        """WebSocket 연결 해제 시 실행"""
        print("WebSocket 연결 종료")  # ✅ 연결 해제 처리 가능

    async def receive(self, text_data):
        """클라이언트로부터 메시지 수신"""
        try:
            data = json.loads(text_data)
            user_message = data["message"]

            print(f"📩 받은 메시지: {user_message}")  # ✅ 로그 추가

            # 선호 장르 (DB에서 가져와야 함)
            preferred_genre = "action"

            # FAISS를 활용한 벡터 검색
            search_results = await self.genre_weighted_mmr_search(
                user_message, preferred_genre
            )

            # GPT-4o API 호출
            gpt_response = await self.get_movie_recommendation(
                user_message, search_results
            )

            # ✅ 응답 JSON 구조 로그 추가
            response_data = {"response": gpt_response}
            print(f"📤 WebSocket 응답: {response_data}")

            # WebSocket으로 응답 전송
            await self.send(text_data=json.dumps(response_data))
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")  # ✅ 오류 로그 추가
            await self.send(text_data=json.dumps({"response": "서버 오류 발생"}))

    async def genre_weighted_mmr_search(self, query, preferred_genre, k=20):
        """MMR 기반 FAISS 검색 + 선호 장르 필터링"""
        try:
            retriever = vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={"k": k, "fetch_k": 10, "lambda_mult": 0.1},
            )
            # 전체 문서 검색 후 장르 필터링 적용
            all_docs = await asyncio.to_thread(retriever.get_relevant_documents, query)
            # 장르 필터링
            preferred_docs = [
                doc for doc in all_docs if doc.metadata.get("genre") == preferred_genre
            ][: int(k * 0.6)]
            general_docs = [
                doc for doc in all_docs if doc.metadata.get("genre") != preferred_genre
            ][: k - len(preferred_docs)]

            return preferred_docs + general_docs
        except Exception as e:
            return f"장르 기반 검색 중 오류 발생 : {str(e)}"

    async def get_movie_recommendation(self, user_message, context):
        """GPT-4o를 활용한 영화 추천 생성"""
        try:
            formatted_context = (
                "\n\n".join(doc.page_content for doc in context)
                if context
                else "검색된 문서가 없습니다."
            )
            prompt = f"""
            넌 영화를 추천하는 AI야. 너는 안성재 셰프와 백종원 사업가 2명의 입장에서 각각 1개의 영화를 추천해야 해.
            
            먼저, 안성재 셰프는 다양성이 높은 예술적인 영화를 좋아하는 성격이야.
            안성재 셰프의 입장에서 예술적이고 새로운 영화를 1개 추천해줘.
            말투에 영화 관련 특성의 익힘 정도가 완벽하다는 내용을 포함해줘.
            또, 영화 내용과 관련해서 동일한 점이 있으면 이븐하게 되었다는 표현을 자주 사용해줘.
            마지막에 백종원씨에게 '오늘 영화 메뉴는 무엇인가요?'라고 대화를 마무리해줘.
            
            두 번째로, 백종원 사업가는 대중적이고 인기가 많은 영화를 좋아하는 스타일이야.
            백종원 사업가의 입장에서 대중적이고 인기가 많은 영화를 1개 추천해줘.
            영화를 소개할 때, 중간에 '조보아씨 이리 내려와서 이것 좀 봐봐유'라는 내용을 추가해줘.
            
            fewshot 예시의 답변 형태로 답변을 만들어줘.
            
            fewshot:
            1. 질문: "커플이 함께 볼 로맨스 영화를 추천해줘"
            대답: 
            안성재 셰프: "음~ 저는 영화의 예술성 익힘 정도가 완벽한 '노트북'을 추천해드릴게요. 
                                두 주인공의 사랑이 이븐하게 느껴지는군요. 커플과 함께 예술성이 높은 SF 로맨스 이야기 한번 맛보세요.
                                백종원씨, 오늘 영화 메뉴는 무엇인가요?"
                                                        
            백종원 사업가: "오늘 영화 메뉴는 맛있는 '라라랜드'지 말이에유. 전 세계 로맨스 중 인기는 탑이어유. 낭만적인 음악과 댄스, 아주 좋구만유.
                                조보아씨 이리 내려와서 이것 좀 봐봐유, 아주 기가 막히쥬.
                                오늘 백종원의 영화 메뉴 추천은 음악과 낭만의 영화 '라라랜드'에유."
            
            2. 질문: "친구가 함께 볼 액션 영화를 추천해줘"
            대답: 
            안성재 셰프: "음~ 저는 영화의 예술성 익힘 정도가 완벽한 '본레거시'를 추천해드릴게요. 
                                멧 데이먼의 촬영 기법과 액션 디렉팅이 정말 예술적이네요. 친구와 함께 예술성이 높은 액션 이야기 한번 맛보세요.
                                백종원씨, 오늘 영화 메뉴는 무엇인가요?"
                                                        
            백종원 사업가: "오늘 영화 메뉴는 맛있는 '미션 임파서블'이지 말이에유. 전 세계 액션 영화 중 인기는 탑이어유. 유명한 BGM과 말도 안 되는 액션, 아주 신나구만유.
                                조보아씨 이리 내려와서 이것 좀 봐봐유, 아주 기가 막히쥬.
                                오늘 백종원의 영화 메뉴 추천은 액션과 스릴의 영화 '미션 임파서블'이에유."

            {formatted_context}

            질문:
            {user_message}
            """

            response = await client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 영화 추천 전문가입니다. 사용자 질문에 대해 친절하게 답변해주세요.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
            )
            response_dict = response.to_dict()
            return response_dict["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"❌ OpenAI API 호출 중 오류 발생: {str(e)}")
            return "서버에서 응답을 생성하는 중 오류가 발생했습니다."
