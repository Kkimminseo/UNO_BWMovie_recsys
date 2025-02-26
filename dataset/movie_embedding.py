import os
import pickle
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

# 환경 변수 로드
from dotenv import load_dotenv

load_dotenv()


def process_and_store_embeddings(csv_file):
    """
    CSV 파일을 읽어와 전처리 후, 기존 FAISS 인덱스에 추가하여 저장하는 함수
    기존 `faiss_index.faiss`, `documents.pkl`을 유지하면서 업데이트함.
    """
    # 경로 상수 정의
    FAISS_DIR = "faiss"
    DOCUMENTS_PATH = os.path.join(FAISS_DIR, "documents.pkl")

    # 디렉토리가 없으면 생성
    os.makedirs(FAISS_DIR, exist_ok=True)

    # 1️⃣ 데이터 로드 및 전처리
    print("📥 데이터 로드 중...")
    df = pd.read_csv(csv_file)

    # 'softcore' 키워드 제거
    df = df[~df["keywords"].str.contains("softcore", case=False, na=False)]

    # 필요한 컬럼 결합
    df["combined_text"] = (
        df["title"] + " " + df["overview"] + " " + df["genres"] + " " + df["keywords"]
    )
    df["combined_text"] = df["combined_text"].astype(str)

    # LangChain Document 객체 변환
    new_docs = [Document(page_content=text) for text in df["combined_text"].tolist()]

    print(f"✅ 데이터 로드 완료! 추가할 문서 수: {len(new_docs)}")

    # 2️⃣ 기존 FAISS 인덱스 및 메타데이터 불러오기
    embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

    if os.path.exists(FAISS_DIR):
        print("📂 기존 FAISS 인덱스 로드 중...")
        try:
            faiss_index = FAISS.load_local(
                FAISS_DIR, embedding_model, allow_dangerous_deserialization=True
            )
        except EOFError:
            print("❌ 기존 FAISS 인덱스가 손상되었습니다. 새로 생성합니다.")
            faiss_index = FAISS.from_documents([], embedding_model)
    else:
        print("🆕 기존 인덱스 없음. 새로운 FAISS 인덱스 생성 중...")
        faiss_index = FAISS.from_documents([], embedding_model)

    # 기존 문서 정보 불러오기
    if os.path.exists(DOCUMENTS_PATH):
        with open(DOCUMENTS_PATH, "rb") as f:
            existing_docs = pickle.load(f)
        print(f"📜 기존 문서 수: {len(existing_docs)}")
    else:
        existing_docs = []
        print("⚠ 기존 documents.pkl 없음. 새로운 파일 생성.")

    # 3️⃣ FAISS 인덱스에 새로운 데이터 추가
    print("🚀 새로운 문서 FAISS에 추가 중...")
    try:
        faiss_index.add_documents(new_docs)
        print(f"✅ 총 {len(new_docs)}개의 문서 추가 완료!")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

    # 기존 문서 리스트에 새로운 문서 추가
    all_docs = existing_docs + new_docs

    # 4️⃣ FAISS 및 메타데이터 저장
    faiss_index.save_local(
        FAISS_DIR
    )  # `faiss_index.faiss`, `faiss_index.pkl` 자동 생성
    print("✅ FAISS 인덱스 저장 완료!")

    with open(DOCUMENTS_PATH, "wb") as f:
        pickle.dump(all_docs, f)
    print("✅ documents.pkl 저장 완료!")

    print("🎉 모든 작업 완료!")


# 실행 예제
csv_file_path = "recent_movies.csv"  # 새로운 CSVc 파일 경로
process_and_store_embeddings(csv_file_path)
