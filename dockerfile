# Використовуємо легкий образ Python
FROM python:3.11-slim

# Встановлюємо системні залежності для роботи з PDF та графікою
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Створюємо робочу директорію
WORKDIR /app

# Копіюємо файл залежностей
COPY requirements.txt .

# Встановлюємо бібліотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли проекту
COPY . .

# Відкриваємо порт для Streamlit
EXPOSE 8501

# Команда для запуску
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]