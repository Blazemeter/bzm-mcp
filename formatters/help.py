from typing import Any, Optional

from tools.help_utils import html_to_markdown


def format_help_info(html_content: str, params: Optional[dict] = None) -> dict[str, Any]:
    base_url = params.get("base_url")
    return {
        "help_content": html_to_markdown(html_content, base_url=base_url),
        "help_url": base_url
    }
