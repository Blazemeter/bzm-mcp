import json
import re
from urllib.parse import urljoin

import lxml.html


def clean_text(text, preserve_newlines=False):
    text = text.replace('\xa0', ' ')

    if preserve_newlines:
        lines = text.split('\n')
        cleaned_lines = [' '.join(line.split()) for line in lines]
        return '\n'.join(cleaned_lines).strip()
    else:
        text = ' '.join(text.split())
        return text.strip()


def extract_text_with_br(element):
    html_str = lxml.html.tostring(element, encoding='unicode', method='html')
    html_str = html_str.replace('<br>', '\n').replace('<br/>', '\n').replace('<br />', '\n')
    temp = lxml.html.fromstring(html_str)
    return temp.text_content()


def table_to_markdown(table, base_url=None, as_html=True):
    rows = table.xpath('.//tr')
    if not rows:
        return ""

    markdown = []

    if as_html:
        markdown.append("<table>")

    header_row = table.xpath('.//thead//tr[1] | .//tr[1]')
    if header_row:
        headers = []
        for th in header_row[0].xpath('.//th | .//td'):
            header_text = process_inline_elements(th, base_url, as_html)
            header_text = clean_text(header_text)
            headers.append(header_text)

        if headers and any(h for h in headers if h):
            if as_html:
                header_html = ""
                for header in headers:
                    header_html += "<th>" + header + "</th>"
                header_html = "<thead><tr>" + header_html + "</tr></thead>"
                markdown.append(header_html)
            else:
                markdown.append("| " + " | ".join(headers) + " |")
                markdown.append("| " + " | ".join(["---"] * len(headers)) + " |")
            start_idx = 1
        else:
            start_idx = 0
    else:
        start_idx = 0

    if as_html:
        markdown.append("<tbody>")

    for row in rows[start_idx:]:
        if as_html:
            markdown.append("<tr>")
        cells = row.xpath('.//td | .//th')
        if cells:
            cell_texts = []
            for cell in cells:
                cell_text = process_inline_elements(cell, base_url, as_html)
                cell_text = clean_text(cell_text)
                cell_texts.append(cell_text)

            if any(cell_texts):
                if as_html:
                    cells_html = ""
                    for cell in cell_texts:
                        cells_html += "<td>" + cell.replace("\n", "<br>") + "</td>"
                    markdown.append(cells_html)
                else:
                    markdown.append("| " + " | ".join(cell_texts) + " |")
        if as_html:
            markdown.append("</tr>")

    if as_html:
        markdown.append("</tbody></table>")

    return "\n".join(markdown) if markdown else ""


def process_inline_elements(element, base_url=None, as_html=False):
    parts = []

    if element.text:
        parts.append(element.text)

    for child in element:
        tag = child.tag.lower()

        if tag == 'a':
            href = child.get('href', '')
            text = child.text_content().strip()

            if href and base_url:
                href = urljoin(base_url, href)

            if text.lower() in ['copy', 'link', ''] or 'javascript:' in href:
                if child.tail:
                    parts.append(child.tail)
                continue

            if text and href:
                if as_html:
                    parts.append(f"<a href='{{href}}'>{text}</a>")
                else:
                    parts.append(f"[{text}]({href})")
            elif text:
                parts.append(text)

        elif tag == 'br':
            if as_html:
                parts.append('<br>')
            else:
                parts.append('\n')
        elif tag in ['strong', 'b']:
            text = child.text_content().strip()
            if text:
                if as_html:
                    parts.append(f"<b>{text}</b>")
                else:
                    parts.append(f"**{text}**")
        elif tag in ['em', 'i']:
            text = child.text_content().strip()
            if text:
                if as_html:
                    parts.append(f"<i>{text}</i>")
                else:
                    parts.append(f"*{text}*")
        elif tag == 'code':
            text = child.text_content().strip()
            if text:
                if as_html:
                    parts.append(f"<code>{text}</code>")
                else:
                    parts.append(f"`{text}`")
        else:
            inner_result = process_inline_elements(child, base_url)
            if inner_result:
                parts.append(inner_result)

        if child.tail:
            parts.append(child.tail)

    return ''.join(parts)


def element_to_markdown(element, base_url=None, level=0):
    code_block_lang = ['javascript', 'java', 'python', 'ruby', 'go', 'php', 'c#', 'csharp', 'typescript',
                       'bash', 'shell', 'sql', 'json', 'xml', 'yaml', 'css', 'html']

    tag = element.tag.lower()
    result = []

    # Headers
    if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        level_num = int(tag[1])
        text = clean_text(element.text_content())
        if text:
            result.append(f"{'#' * level_num} {text}\n")

    elif tag == 'p':
        text = clean_text(process_inline_elements(element, base_url))
        if text:
            result.append(f"{text}\n")

    elif tag == 'ul':
        for li in element.xpath('./li'):
            text = clean_text(process_inline_elements(li, base_url))
            if text:
                result.append(f"- {text}\n")
        result.append("")

    elif tag == 'ol':
        for i, li in enumerate(element.xpath('./li'), 1):
            text = clean_text(process_inline_elements(li, base_url))
            if text:
                result.append(f"{i}. {text}\n")
        result.append("")

    elif tag == 'table':
        table_md = table_to_markdown(element, base_url)
        if table_md:
            result.append(f"{table_md}\n")

    elif tag == 'pre' or 'codesnippet' in element.get('class', '').lower():
        lang = ""
        code_element = element

        # Try to get the language code and the source code

        lang_elem = element.xpath('.//*[contains(@class, "language")]')
        if not lang_elem:
            for child in element:
                child_text = child.text_content().strip().lower()
                if child_text in code_block_lang:
                    lang = child_text
                    break

        code_children = element.xpath('.//code')
        if code_children:
            code_element = code_children[0]
            class_attr = code_element.get('class', '')
            if 'language-' in class_attr:
                lang = class_attr.split('language-')[1].split()[0]

        code_text = extract_text_with_br(code_element)
        code_text = clean_text(code_text, preserve_newlines=True)

        lines = code_text.split('\n')
        filtered_lines = []

        for i, line in enumerate(lines):
            line_stripped = line.strip().lower()
            if line_stripped == 'copy':  # Exclude Copy element (UI Element)
                continue
            if line_stripped in code_block_lang:
                lang = line_stripped

            filtered_lines.append(line)

        code_text = '\n'.join(filtered_lines).strip()

        if code_text:
            result.append(f"```{lang}\n{code_text}\n```\n")

    elif tag == 'blockquote':
        text = extract_text_with_br(element)
        text = clean_text(text)
        if text:
            for line in text.split('\n'):
                if line.strip():
                    result.append(f"> {line}\n")
            result.append("")

    elif tag == 'hr':
        result.append("---\n")

    elif tag == 'img':
        alt = element.get('alt', '')
        src = element.get('src', '')
        if src and base_url:
            src = urljoin(base_url, src)
            result.append(f"![{alt}]({src})\n")

    elif tag in ['script', 'style', 'noscript', 'meta', 'link', 'head']:
        # Ignore
        pass

    # For any others elements, process the children
    else:
        for child in element:
            child_md = element_to_markdown(child, base_url, level + 1)
            if child_md:
                result.extend(child_md)

    return result


def html_to_markdown(html_content, base_url=None):
    tree = lxml.html.fromstring(html_content)

    main_div = tree.xpath('//div[@role="main"]')
    if not main_div:
        main_div = tree.xpath('//main | //div[@class="main"] | //article | //body')

    if not main_div:
        return "# Error\n\nMain content not found"

    main_div = main_div[0]

    markdown_lines = []
    for child in main_div:
        result = element_to_markdown(child, base_url)
        if result:
            markdown_lines.extend(result)

    markdown = "".join(markdown_lines)

    while "\n\n\n" in markdown:
        markdown = markdown.replace("\n\n\n", "\n\n")

    return markdown.strip()


def convert_js_to_py_dict(js_text: str) -> dict:
    # Remove signup link
    js_text = js_text.replace(
        "https://www.blazemeter.com/signup", "signup")

    # Convert javascript dictionary to python dictionary
    js_text = js_text.replace("define(", "").replace(");", "").replace("'", '"')
    js_text = re.sub(r'//.*', '', js_text)
    js_text = re.sub(r'/\*[\s\S]*?\*/', '', js_text)
    js_text = re.sub(r',\s*(?=[}\]])', '', js_text)
    js_text = re.sub(r'([{\[,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', js_text)

    return json.loads(js_text)
