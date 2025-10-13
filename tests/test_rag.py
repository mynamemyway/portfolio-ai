# tests/test_rag.py

import pytest
from langchain_core.documents import Document

# Import the private function we want to test
from app.core.rag import _load_and_split_documents


@pytest.fixture
def temp_knowledge_base(tmp_path, monkeypatch):
    """
    Creates a temporary knowledge base directory with a sample markdown file.
    It then patches the KNOWLEDGE_BASE_DIR constant in the rag module to point
    to this temporary directory.
    """
    # Create a temporary directory for the knowledge base
    kb_dir = tmp_path / "knowledge_base"
    kb_dir.mkdir()

    # Create a sample markdown file
    sample_content = (
        "This is the first sentence. " * 50
        + "This is the second sentence, which will be in a separate chunk. " * 50
    )
    (kb_dir / "sample.md").write_text(sample_content, encoding="utf-8")

    # Patch the constant in the rag module
    monkeypatch.setattr("app.core.rag.KNOWLEDGE_BASE_DIR", kb_dir)
    return kb_dir


def test_load_and_split_documents(temp_knowledge_base):
    """
    Tests that _load_and_split_documents correctly loads a file,
    splits it into chunks, and returns a list of Document objects.
    """
    # Call the function to be tested
    chunked_documents = _load_and_split_documents()

    # Assertions
    assert isinstance(chunked_documents, list)
    assert len(chunked_documents) > 1  # Based on the content and splitter settings
    assert all(isinstance(doc, Document) for doc in chunked_documents)
    assert chunked_documents[0].page_content.startswith("This is the first sentence.")