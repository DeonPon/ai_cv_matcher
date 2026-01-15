import streamlit as st
import os
from dotenv import load_dotenv
from utils import extract_text_from_pdf, analyze_cv_with_jd
from langchain_groq import ChatGroq

load_dotenv()

st.set_page_config(page_title="AI CV Matcher")
st.title("AI CV Matcher & Ranker")
st.subheader("Бізнес-кейс: Оптимізація скринінгу кандидатів")

# 1. Поля вводу
job_description = st.text_area("Вставте опис вакансії (Job Description):", height=200)
uploaded_files = st.file_uploader("Завантажте резюме (PDF):", type="pdf", accept_multiple_files=True)

# 2. ОДНА кнопка для запуску процесу
if st.button("Проаналізувати кандидатів", key="analyze_button") and job_description and uploaded_files:
    with st.spinner("Проводимо AI-скринінг... Це може зайняти хвилину."):
        # Витягуємо текст
        resumes = extract_text_from_pdf(uploaded_files)

        # Ініціалізуємо ШІ (Groq)
        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.3,
            groq_api_key=os.getenv("GROQ_API_KEY")  # Явне вказання ключа
        )

        # Аналізуємо кожне резюме
        for res in resumes:
            with st.expander(f"📊 Результат для: {res['name']}"):
                # Отримуємо релевантний контекст через FAISS (RAG)
                context = analyze_cv_with_jd(job_description, res['content'])

                prompt = f"""
                Ти - професійний IT-рекрутер. Твоє завдання - оцінити відповідність резюме до вакансії.

                ОПИС ВАКАНСІЇ:
                {job_description}

                РЕЙЕВАНТНИЙ ДОСВІД З РЕЗЮМЕ:
                {context}

                Надай відповідь у такому форматі:
                1. Оцінка відповідності (Score): від 0 до 100%.
                2. Hard Skills: Які ключові навички збігаються.
                3. Missing: Чого не вистачає.
                4. Verdict: Чому варто або не варто запрошувати на інтерв'ю.
                """

                response = llm.invoke(prompt)
                st.markdown(response.content)