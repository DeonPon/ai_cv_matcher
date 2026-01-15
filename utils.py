from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


def extract_text_from_pdf(pdf_files):
    resumes_data = []
    for pdf in pdf_files:
        reader = PdfReader(pdf)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        resumes_data.append({"name": pdf.name, "content": text})
    return resumes_data


def analyze_cv_with_jd(job_description, resume_text):
    # 1. Розбиваємо резюме на шматочки (щоб ШІ було легше шукати)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(resume_text)

    # 2. Створюємо векторні представлення (Embeddings)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 3. Тимчасова база даних FAISS в оперативній пам'яті
    vector_db = FAISS.from_texts(chunks, embeddings)

    # 4. Шукаємо в резюме шматочки, які найбільше схожі на опис вакансії
    relevant_docs = vector_db.similarity_search(job_description, k=3)
    relevant_context = "\n".join([doc.page_content for doc in relevant_docs])

    return relevant_context