# Portfolio AI v1.1.0 🤖

<p align="left">
  <img src="https://img.shields.io/badge/Status-Active-green" alt="Status">
  <img src="https://img.shields.io/badge/Version-1.1.0-blueviolet" alt="Version">
  <img src="https://img.shields.io/badge/Build-Passing-brightgreen" alt="Build">
</p>

**Portfolio AI** — это интеллектуальный Telegram-бот, представляющий собой цифровую копию Python-разработчика. Бот предназначен для демонстрации профессиональных навыков, проектов и опыта специалиста в интерактивном формате. В основе бота лежит архитектура RAG (Retrieval-Augmented Generation), позволяющая давать точные и контекстуально-обоснованные ответы на основе приватной базы знаний.

<details>
<summary>Посмотреть скриншот</summary>
<img width="1060" height="670" alt="Снимок экрана 2025-10-12 в 02 20 58" src="https://github.com/user-attachments/assets/9ae5a8e3-4421-4cfa-81fa-79bbeca2744f" />

</details>

## 📚 Оглавление
- [Ключевые возможности](#-ключевые-возможности)
- [Технологический стек](#-технологический-стек)
- [Структура проекта](#-структура-проекта)
- [Инструкции по запуску](#-инструкции-по-запуску)

## ✨ Ключевые возможности

*   **Интеллектуальные ответы (RAG):** Бот отвечает на вопросы, основываясь на документах из локальной базы знаний (`app/knowledge_base`), используя векторный поиск в **ChromaDB**.
*   **Интерактивное иерархическое меню:** Реализовано многоуровневое inline-меню для удобной навигации по разделам "Навыки", "Проекты", "Контакты" без перезагрузки чата.
*   **Статические UI-элементы:** Команды `/help`, `/reset` и кнопка "Hello world!" работают без обращения к LLM, обеспечивая мгновенный отклик и улучшенный UX.
*   **Память диалогов:** Бот поддерживает контекст диалога в рамках одной сессии, что позволяет задавать уточняющие вопросы.
*   **Отказоустойчивость LLM:** Интеграция с **OpenRouter** и механизм фолбэка обеспечивают стабильную работу: при сбое основной модели система автоматически переключается на резервную.
*   **Модульная архитектура:** Код четко разделен на слои (`handlers`, `core`, `keyboards`, `utils`), что упрощает поддержку и расширение.
*   **Готовность к контейнеризации:** Проект полностью готов к развертыванию с помощью Docker.

## 🔧 Технологический стек

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python version">
  <img src="https://img.shields.io/badge/aiogram-3.x-0088cc.svg" alt="aiogram">
  <img src="https://img.shields.io/badge/LangChain-Orchestrator-blueviolet.svg" alt="LangChain">
  <img src="https://img.shields.io/badge/OpenRouter-LLM_Gateway-purple.svg" alt="OpenRouter">
  <img src="https://img.shields.io/badge/ChromaDB-Vector_Store-9f4ae6.svg" alt="ChromaDB">
  <img src="https://img.shields.io/badge/Docker-Containerization-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/Pydantic-Data_Validation-cyan.svg" alt="Pydantic">
  <img src="https://img.shields.io/badge/code%20style-ruff-black.svg" alt="Code style: ruff">
</p>

## 📁 Структура проекта
```text
portfolio-ai/
├── app/
│   ├── core/             # Основная логика (RAG, память, цепочки)
│   ├── handlers/         # Обработчики сообщений и колбэков
│   ├── keyboards/        # Модули для создания клавиатур
│   ├── utils/            # Вспомогательные утилиты
│   ├── knowledge_base/   # Исходные документы для базы знаний
│   └── ui_commands.py    # Установка команд в меню Telegram
├── chroma_db/            # Локальное хранилище векторов ChromaDB
├── 4dev/                 # Документация для разработки
├── main.py               # Точка входа в приложение
├── .env                  # Файл с секретными ключами (не отслеживается Git)
├── Dockerfile            # Инструкция для сборки Docker-образа
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

    # (Optional) Path to the welcome photo for the /start command.
    WELCOME_PHOTO_PATH="path/to/your/welcome_photo.jpg"

    # (Optional) Path to the help photo for the /help command.
    HELP_PHOTO_PATH="path/to/your/help_photo.jpg"
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

<details>
<summary>Развернуть</summary>

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

</details>
