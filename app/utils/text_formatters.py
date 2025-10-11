# app/utils/text_formatters.py

import re


def escape_markdown_v2(text: str) -> str:
    """
    Escapes special characters for Telegram's MarkdownV2 parse mode.

    Args:
        text: The input string to be escaped.
    Returns:
        The string with all special MarkdownV2 characters escaped.
    """
    escape_chars = r"([_*\[\]()~`>#+\-=|{}.!])"
    return re.sub(escape_chars, r"\\\1", text)


def sanitize_for_telegram_markdown(text: str) -> str:
    """
    Proactively sanitizes text to make it compatible with Telegram's MarkdownV2.

    This function converts unsupported markdown (like headers) into a supported
    format and escapes specific characters that are known to cause parsing errors.

    Args:
        text: The raw string from the LLM to be sanitized.
    Returns:
        A sanitized string ready for Telegram's MarkdownV2 parser.
    """
    if not text:
        return ""

    processed_lines = []
    for line in text.split('\n'):
        # Preserve empty lines
        if not line.strip():
            processed_lines.append(line)
            continue

        # Make a copy to modify
        processed_line = line

        # Rule 1: Convert main headers (e.g., ### Title) to bold text.
        processed_line = re.sub(r'^\s*#+\s+(.+)', r'*\1*', processed_line)

        # Rule 2: Convert list headers (e.g., "- **Tools:**") to just bold text.
        processed_line = re.sub(r'^\s*-\s+(\*\*.*?\*\*)', r'\1', processed_line)

        # Rule 3: Convert indented list items (e.g., "  - Ruff") to use a bullet point.
        processed_line = re.sub(r'^(\s+)-\s+', r'\1• ', processed_line)

        # Rule 4: Convert any remaining top-level list items.
        processed_line = re.sub(r'^\s*-\s+', '• ', processed_line)

        # Rule 5: Convert standard markdown bold (**text**) to Telegram's MarkdownV2 bold (*text*).
        processed_line = re.sub(r'\*\*(.*?)\*\*', r'*\1*', processed_line)

        processed_lines.append(processed_line)

    # Join the lines back and perform a final escape of all special characters.
    sanitized_text = '\n'.join(processed_lines)

    # Final escape for all special characters not part of intended formatting.
    escape_chars = r"(?<!\\)([\[\]\(\)~`>+\-=|{}.!])"
    sanitized_text = re.sub(escape_chars, r'\\\1', sanitized_text)

    return sanitized_text