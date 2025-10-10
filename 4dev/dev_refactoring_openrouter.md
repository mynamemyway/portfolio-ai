# Рефакторинг для перехода на OpenRouter

## Введение
Этот план описывает последовательность действий для рефакторинга проекта с целью перехода от прямого использования API Mistral AI к использованию агрегатора OpenRouter.

**Цель:**
1.  Устранить проблему с жесткими лимитами бесплатного API Mistral.
2.  Получить доступ к широкому спектру бесплатных и более производительных моделей.
3.  Унифицировать взаимодействие с LLM через OpenAI-совместимый интерфейс.

Разработка будет вестись послойно, затрагивая конфигурацию, слой данных (embeddings) и сервисный слой (LLM).

---

### **Этап 1: Подготовка - Зависимости и Конфигурация**

На этом этапе мы подготовим проект к работе с OpenRouter, обновив зависимости и переменные окружения.

#### **1.1. Обновление `requirements.txt`**
*   **Цель:** Заменить специфичные для Mistral библиотеки на универсальную библиотеку для работы с OpenAI-совместимыми API.
*   **Файл:** `requirements.txt`
*   **Логика:**
    1.  Удалить строки `langchain-mistralai` и `mistralai`.
    2.  Добавить строку `langchain-openai`.
    3.  Выполнить `pip install -r requirements.txt` для применения изменений.

#### **1.2. Обновление `.env.example`**
*   **Цель:** Отразить в примере файла окружения новые переменные, необходимые для OpenRouter.
*   **Файл:** `.env.example`
*   **Логика:**
    1.  Заменить `MISTRAL_API_KEY` на `OPENROUTER_API_KEY`.
    2.  Добавить комментарии, поясняющие назначение нового ключа.

#### **1.3. Обновление `app/config.py`**
*   **Цель:** Адаптировать Pydantic-модель `Settings` для работы с новыми переменными окружения.
*   **Файл:** `app/config.py`
*   **Класс / Сигнатура:** `class Settings(BaseSettings):`
*   **Логика:**
    1.  Заменить поле `MISTRAL_API_KEY: str` на `OPENROUTER_API_KEY: str`.
    2.  Удалить поле `MISTRAL_CHAT_MODEL`.
    3.  Добавить новые поля с значениями по умолчанию для моделей и базового URL:
        *   `OPENROUTER_CHAT_MODEL: str = "google/gemini-flash-1.5"`
        *   `OPENROUTER_EMBEDDING_MODEL: str = "mixedbread-ai/mxbai-embed-large-v1"`
        *   `OPENROUTER_API_BASE: str = "https://openrouter.ai/api/v1"`

---

### **Этап 2: Рефакторинг Слоя Данных (Embedding Model)**

На этом этапе мы заменим модель для создания векторов (эмбеддингов).

#### **2.1. Обновление `app/core/rag.py`**
*   **Цель:** Заменить `MistralAIEmbeddings` на `OpenAIEmbeddings`, настроенный для OpenRouter.
*   **Файл:** `app/core/rag.py`
*   **Функция / Сигнатура:** `get_embedding_model()`
*   **Логика:**
    1.  Удалить импорт `MistralAIEmbeddings`.
    2.  Импортировать `OpenAIEmbeddings` из `langchain_openai`.
    3.  Внутри функции `get_embedding_model` удалить инициализацию `httpx.AsyncClient`.
    4.  Инициализировать и вернуть `OpenAIEmbeddings`, передав в конструктор:
        *   `model=settings.OPENROUTER_EMBEDDING_MODEL`
        *   `openai_api_key=settings.OPENROUTER_API_KEY`
        *   `base_url=settings.OPENROUTER_API_BASE`
        *   `http_client`: `langchain-openai` управляет им самостоятельно, поэтому ручная настройка `httpx` больше не нужна.

---

### **Этап 3: Рефакторинг Сервисного Слоя (LLM)**

На этом этапе мы заменим основную чат-модель.

#### **3.1. Обновление `app/core/chain.py`**
*   **Цель:** Заменить `ChatMistralAI` на `ChatOpenAI`, настроенный для OpenRouter.
*   **Файл:** `app/core/chain.py`
*   **Функция / Сигнатура:** `get_rag_chain()`
*   **Логика:**
    1.  Удалить импорт `ChatMistralAI`.
    2.  Импортировать `ChatOpenAI` из `langchain_openai`.
    3.  Внутри функции `get_rag_chain` заменить инициализацию `llm`:
        *   Было: `llm = ChatMistralAI(...)`
        *   Стало: `llm = ChatOpenAI(...)`
    4.  Передать в конструктор `ChatOpenAI` следующие параметры:
        *   `model=settings.OPENROUTER_CHAT_MODEL`
        *   `openai_api_key=settings.OPENROUTER_API_KEY`
        *   `base_url=settings.OPENROUTER_API_BASE`

---

### **Этап 4: Обновление Документации**

На этом этапе мы актуализируем `README.md`, чтобы он отражал изменения в стеке и инструкциях по настройке.

#### **4.1. Обновление `README.md`**
*   **Цель:** Привести документацию в соответствие с новым стеком технологий.
*   **Файл:** `README.md`
*   **Логика:**
    1.  В разделе "Стек технологий" заменить шильдик `Mistral AI` на `OpenRouter`.
    2.  В разделе "Инструкции по запуску" обновить шаг 3 (Настройка переменных окружения), заменив `MISTRAL_API_KEY` на `OPENROUTER_API_KEY` и обновив описание.

---

### **Этап 5: Тестирование**

*   **Цель:** Убедиться, что после рефакторинга система работает корректно.
*   **Инструкции:**
    1.  Удалить старую векторную базу `chroma_db/`.
    2.  Выполнить переиндексацию командой `python -m app.core.rag`. Убедиться, что процесс проходит без ошибок.
    3.  Запустить бота командой `python main.py`.