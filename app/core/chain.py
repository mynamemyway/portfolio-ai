# app/core/chain.py

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

from app.config import settings
from app.core.memory import get_chat_memory
from app.core.rag import get_vector_store

# --- System Prompt ---

SYSTEM_PROMPT = """
Ты — русскоязычная цифровая копия бэкенд-разработчика на Python и консультант по его портфолио.
Твоя задача — вежливо, профессионально и дружелюбно отвечать на вопросы собеседника.
Правила:
1.  Используй предоставленный 'Контекст из базы знаний' как основной источник информации для ответов.
2.  Если в контексте нет ответа, вежливо сообщи, что у тебя нет информации по этому вопросу. Не придумывай факты.
3.  Структурируй ответы, делай их читабельными. Используй списки и абзацы.
4.  Общайся на "Вы", если пользователь не указал иного.
5.  Исключи из ответов ссылки и контактную информацию.
6.  Отвечай только на РУССКОМ языке.
"""


# --- Chain Creation ---


async def _get_async_chat_history(x: dict) -> dict:
    """
    Asynchronously loads chat history directly from SQLiteChatMessageHistory
    and applies windowing logic.

    This is necessary because LangChain's ConversationBufferWindowMemory
    is not fully async-aware for its `chat_memory` attribute's `messages` property,
    leading to `TypeError` when trying to access an awaited coroutine.
    """
    session_id = x["session_id"]
    # Get the ConversationBufferWindowMemory instance, which wraps SQLiteChatMessageHistory
    memory_buffer = get_chat_memory(session_id=session_id)
    # Await the async messages property of the underlying SQLiteChatMessageHistory
    all_messages = await memory_buffer.chat_memory.messages
    # Apply windowing logic (k * 2 messages for k conversation turns)
    k = settings.MEMORY_WINDOW_SIZE
    windowed_messages = all_messages[-k * 2 :] if k > 0 else []
    return {"chat_history": windowed_messages}

def get_rag_chain():
    """
    Creates and returns a conversational RAG (Retrieval-Augmented Generation) chain.

    This function orchestrates the entire process of handling a user query:
    1.  Loads conversation history for the session.
    2.  Retrieves relevant documents (context) from the vector store based on the question.
    3.  Formats the system prompt with the retrieved context.
    4.  Sends the prompt, history, and question to the LLM.
    5.  Parses the LLM's response into a string.
    6.  Saves the new question and answer to the session's history.

    Returns:
        A Runnable object representing the complete conversational RAG chain.
    """
    # 1. Initialize components
    # Initialize the LLM using ChatOpenAI, configured for OpenRouter
    llm = ChatOpenAI(
        model=settings.OPENROUTER_CHAT_MODEL,
        openai_api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_API_BASE,
        temperature=0.7,  # Controls the creativity of the response
        max_tokens=1024,  # Limits the length of the generated response
    )

    retriever = get_vector_store().as_retriever()

    # 2. Define the prompt template
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "Вопрос: {question}\n\nКонтекст из базы знаний:\n{context}"),
        ]
    )

    # 3. Define a function to format retrieved documents
    def format_docs(docs):
        """Converts a list of Document objects into a single string."""
        return "\n\n".join(doc.page_content for doc in docs)

    # 4. Create the core RAG chain using LangChain Expression Language (LCEL)
    rag_chain = (
        RunnablePassthrough.assign(
            context=itemgetter("question") | retriever | format_docs
        )
        | prompt
        | llm
        | StrOutputParser()
    )

    # 5. Create the full conversational chain with memory
    # This chain takes a session_id and a question as input.
    conversational_rag_chain = (
        RunnablePassthrough.assign(
            chat_history=RunnableLambda(_get_async_chat_history) | itemgetter("chat_history")
        )
        | rag_chain
    )

    return conversational_rag_chain