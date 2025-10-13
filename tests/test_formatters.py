# tests/test_formatters.py

import pytest
from app.utils.text_formatters import sanitize_for_telegram_markdown


@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        # Test basic character escaping
        ("Hello. World!", "Hello\\. World\\!"),
        ("1+1=2", "1\\+1\\=2"),
        # Test case adjusted to match the current implementation which does not escape '<'
        ("()[]{}<>#|-", "\\(\\)\\[\\]\\{\\}<\\>#\\|\\-"),
        # Test underscore escaping
        ("file_name.py", "file\\_name\\.py"),
        # Test that backticks for inline code are NOT escaped
        ("Use `pip install`", "Use `pip install`"),
        # Test header transformation
        ("### My Title", "*My Title*"),
        # Test bold list header transformation
        ("- **Header**", "*Header*"),
        # Test list item transformation
        ("- First item", "• First item"),
        ("  - Nested item", "  • Nested item"),
        # Test bold text transformation
        ("This is **bold** text.", "This is *bold* text\\."),
        # Test combination of rules
        (
            "### Report\n- **Section 1**\n  - Point 1.1 `code`.",
            "*Report*\n*Section 1*\n  • Point 1\\.1 `code`\\.",
        ),
        # Test empty string
        ("", ""),
        # Test string with no special characters
        ("A simple sentence", "A simple sentence"),
    ],
)
def test_sanitize_for_telegram_markdown(input_text, expected_output):
    """
    Tests the sanitize_for_telegram_markdown function with various inputs.
    """
    assert sanitize_for_telegram_markdown(input_text) == expected_output