# Portfolio-AI 🤖

<p align="left">
  <img src="https://img.shields.io/badge/Status-In_Development-blue" alt="Status">
  <img src="https://img.shields.io/badge/Version-0.3.0-blueviolet" alt="Version">
  <img src="https://img.shields.io/badge/Build-Passing-brightgreen" alt="Build">
</p>

Персональный AI-ассистент в Telegram, который выступает в роли цифрового портфолио и консультанта. Бот автономно, на основе базы знаний, презентует разработчика, его проекты и экспертизу.

## 📚 Оглавление
- [Стек технологий](#-стек-технологий)
- [Структура проекта](#-структура-проекта)
- [Инструкции по запуску](#-инструкции-по-запуску)
- [План разработки](#-план-разработки)

## 🔧 Стек технологий

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python version">
  <img src="https://img.shields.io/badge/aiogram-3.x-0088cc.svg" alt="aiogram">
  <img src="https://img.shields.io/badge/LangChain-Orchestrator-blueviolet.svg" alt="LangChain">
  <img src="https://img.shields.io/badge/OpenRouter-LLM_Gateway-purple.svg" alt="OpenRouter">
  <img src="https://img.shields.io/badge/Self_Hosted-Embedding_Service-9cf.svg" alt="Self-Hosted Embedding Service">
  <img src="https://img.shields.io/badge/ChromaDB-Vector_Store-9f4ae6.svg" alt="ChromaDB">
  <img src="https://img.shields.io/badge/SQLite-Database-orange.svg" alt="SQLite">
  <img src="https://img.shields.io/badge/Pydantic-Data_Validation-cyan.svg" alt="Pydantic">
  <img src="https://img.shields.io/badge/Uvicorn-ASGI_Server-green.svg" alt="Uvicorn">
  <img src="https://img.shields.io/badge/code%20style-ruff-black.svg" alt="Code style: ruff">
</p>

## 📁 Структура проекта
```text
Portfolio-AI/
├── app/
│   ├── core/             # Ключевая бизнес-логика
│   │   ├── config.py     # Управление конфигурацией и API-ключами
│   │   ├── memory.py     # Модуль памяти для хранения истории чатов
│   │   └── rag.py        # Логика создания и индексации базы знаний
│   ├── db/               # Локальное хранилище контекста из чатов телеграм
│   ├── knowledge_base/   # Исходные документы для базы знаний (.md)
│   └── main.py           # Точка входа для Telegram-бота (будет создана)
├── chroma_db/            # Локальное хранилище векторов ChromaDB
├── .env                  # Файл с секретными ключами (не отслеживается Git)
├── .gitignore
├── README.md
└── requirements.txt
```

## 📦 Инструкции по запуску

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/mynamemyway/Portfolio-AI.git
    cd Portfolio-AI
    ```

2.  **Создайте виртуальное окружение и установите зависимости:**
    Убедитесь, что у вас установлен Python 3.12+.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    pip install -r requirements.txt
    ```

3.  **Настройте переменные окружения:**
    Создайте файл `.env` в корневой папке проекта.
    ```bash
    touch .env
    ```
    Откройте файл `.env` и добавьте в него следующие переменные, заменив значения на ваши:
    ```dotenv
    # Telegram Bot Token from @BotFather
    BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"

    # OpenRouter API Key from https://openrouter.ai/keys
    OPENROUTER_API_KEY="YOUR_OPENROUTER_API_KEY"

    # URL for the self-hosted embedding service API
    EMBEDDING_SERVICE_URL="http://your_server_ip:8000/embed"

    # (Optional) Controls the creativity of the response (e.g., 0.7).
    OPENROUTER_TEMPERATURE=0.7

    # (Optional) Limits the length of the generated response in tokens (e.g., 1024).
    OPENROUTER_MAX_TOKENS=1024

    # (Optional) The number of recent messages to keep in the conversation memory window.
    MEMORY_WINDOW_SIZE=10
    ```

4.  **Запустите сервис эмбеддингов:**
    Этот проект требует запущенного e5-large-embedding-service. Убедитесь, что Docker-контейнер с этим сервисом запущен и доступен по адресу, указанному в `EMBEDDING_SERVICE_URL`.

5.  **Наполните базу знаний:**
    Поместите ваши документы (в формате `.md`) в директорию `app/knowledge_base/`.

6.  **Создайте векторный индекс:**
    Запустите скрипт индексации. Он прочитает документы, векторизует их и сохранит в `chroma_db/`.
    ```bash
    python -m app.core.rag
    ```

7.  **Запустите бота:**
    ```bash
    python main.py
    ```

## 📅 План разработки

**✨ Прогресс разработки MVP ✨**
`[████████████████████] 100%`

### Шаг 1: Подготовка Проекта и Безопасность
- [x] Создана структура проекта, настроено виртуальное окружение.
- [x] Обеспечено безопасное хранение API-ключей через `.env` и Pydantic.

### Шаг 2: Создание и Индексирование Базы Знаний (RAG)
- [x] Подготовлены документы для базы знаний.
- [x] Реализован модуль для загрузки, разделения и векторизации документов.
- [x] Векторы успешно сохраняются в локальной ChromaDB.

### Шаг 3: Модуль Памяти и Хранение Истории
- [x] Настроен SQLite для асинхронного хранения истории сообщений.
- [x] Реализован и интегрирован механизм памяти с LangChain.

### Шаг 4: Основная Логика LLM и RAG-Цепочки
- [x] Написан Системный Промпт для AI-консультанта.
- [x] Создана LangChain Retrieval Chain, объединяющая RAG, память и LLM.

### Шаг 5: Интеграция с Telegram (aiogram)
- [x] Реализованы обработчики команд `/start` и текстовых сообщений.
- [x] Интегрирован вызов RAG-цепочки в обработчик сообщений.

### Шаг 6: Тестирование и Развертывание
- [x] Проведено локальное тестирование всей системы.
- [x] Проведена интеграция и отладка собственного embedding-сервиса.
- [ ] Подготовить проект к деплою на Render.com или собственном сервере.
