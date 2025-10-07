# Portfolio-AI 🤖

<p align="left">
  <img src="https://img.shields.io/badge/Status-In_Development-blue" alt="Status">
  <img src="https://img.shields.io/badge/Version-0.2.0-blueviolet" alt="Version">
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
  <img src="https://img.shields.io/badge/Mistral_AI-LLM_&_Embeddings-teal.svg" alt="Mistral AI">
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
│   ├── core/
│   │   ├── config.py     # Управление конфигурацией и API-ключами
│   │   └── rag.py        # Логика создания и индексации базы знаний (RAG)
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
    # Токен вашего Telegram-бота от @BotFather
    BOT_TOKEN="your_telegram_bot_token"

    # Ваш API-ключ от Mistral AI
    MISTRAL_API_KEY="your_mistral_api_key"
    ```

4.  **Наполните базу знаний:**
    Поместите ваши документы (в формате `.md`) в директорию `app/knowledge_base/`.

5.  **Создайте векторный индекс:**
    Запустите скрипт индексации. Он прочитает документы, векторизует их и сохранит в `chroma_db/`.
    ```bash
    python -m app.core.rag
    ```

6.  **Запустите бота (будет реализовано на следующих этапах):**
    ```bash
    python -m app.main
    ```

## 📅 План разработки

🛠️ **Прогресс разработки MVP** 🛠️
`[████████░░░░░░░░░░░░░] 33%`

### Шаг 1: Подготовка Проекта и Безопасность
- [x] Создана структура проекта, настроено виртуальное окружение.
- [x] Обеспечено безопасное хранение API-ключей через `.env` и Pydantic.

### Шаг 2: Создание и Индексирование Базы Знаний (RAG)
- [x] Подготовлены документы для базы знаний.
- [x] Реализован модуль для загрузки, разделения и векторизации документов.
- [x] Векторы успешно сохраняются в локальной ChromaDB.

### Шаг 3: Модуль Памяти и Хранение Истории
- [ ] Настроить SQLite для хранения истории сообщений с каждым пользователем.
- [ ] Интегрировать механизм хранения с LangChain `ChatMessageHistory`.

### Шаг 4: Основная Логика LLM и RAG-Цепочки
- [ ] Написать Системный Промпт для AI-консультанта.
- [ ] Создать LangChain Retrieval Chain, объединяющую RAG, память и LLM.

### Шаг 5: Интеграция с Telegram (aiogram)
- [ ] Реализовать обработчики команд `/start` и текстовых сообщений.
- [ ] Интегрировать вызов RAG-цепочки в обработчик сообщений.

### Шаг 6: Тестирование и Развертывание
- [ ] Провести локальное тестирование всей системы.
- [ ] Подготовить проект к развертыванию на Render.com.
