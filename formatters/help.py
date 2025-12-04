from typing import Any, Optional

from lxml import html

from tools.help_utils import html_to_markdown


def format_help_info(html_content: str, params: Optional[dict] = None) -> dict[str, Any]:
    base_url = params.get("base_url")
    return {
        "help_content": html_to_markdown(html_content, base_url=base_url),
        "help_url": base_url
    }

def format_list_real_devices_extended_commands_info(html_content: str, params: Optional[dict] = None) -> dict[str, Any]:
    # Parse HTML with lxml
    tree = html.fromstring(html_content)

    results = []

    # Get the main div with role="main"
    main_div = tree.xpath('//div[@role="main"]')

    if not main_div:
        return {
            "error": "Error reading the help webpage",
        }

    main_div = main_div[0]

    # Search all the headers h2
    h2_elements = main_div.xpath('.//h2')

    for h2 in h2_elements:
        title = ''.join(h2.xpath('.//text()')).strip()
        if not title:
            continue

        # Search the next table to the header h2
        tables = h2.xpath('./following-sibling::table[1]')
        if not tables:
            tables = h2.xpath('./following::table[1]')
        if not tables:
            continue
        table = tables[0]

        # Extract table headers
        headers = []
        thead = table.xpath('.//thead//th')
        if thead:
            headers = [''.join(th.xpath('.//text()')).strip() for th in thead]

        # Without headers, set default values
        if not headers:
            headers = ['Command', 'Description']

        # Extract rows
        rows = table.xpath('.//tbody//tr | .//tr[td]')

        commands = []
        for row in rows:
            cells = row.xpath('.//td')
            if not cells:
                continue

            # Extract text and links
            cell_texts = []
            command_id = None

            for i, cell in enumerate(cells):
                # Extract text
                cell_text = ''.join(cell.xpath('.//text()')).strip()
                cell_text = ' '.join(cell_text.split())  # Normalize spaces
                cell_texts.append(cell_text)

                # On Command, extract link
                if i == 0:
                    links = cell.xpath('.//a/@href')

                    if links:
                        link = links[0]
                        # Extract the ID from the link
                        if '/' in link:
                            filename = link.split('/')[-1]
                        else:
                            filename = link

                        # Remove extension
                        if '.htm' in filename:
                            command_id = filename.split('.htm')[0]

            # Create dictionary
            if len(cell_texts) >= len(headers):
                row_dict = {}
                for i, header in enumerate(headers):
                    if i < len(cell_texts):
                        row_dict[header.lower()] = cell_texts[i]
                if command_id:
                    row_dict["id"] = command_id

                commands.append(row_dict)
            elif len(cell_texts) >= 2:
                # In case doesn't match, use Command and Description by default
                command_dict = {
                    "command": cell_texts[0],
                    "description": cell_texts[1]
                }
                if command_id:
                    command_dict["id"] = command_id
                commands.append(command_dict)

        if commands:
            results.append({
                "title": title,
                "commands": commands
            })

    # Create the final result
    return {
        "total_sections": len(results),
        "sections": results
    }


def format_read_real_devices_extended_command_info(html_content: str, params: Optional[dict] = None) -> dict[str, Any]:
    base_url = params.get("base_url")
    return {
        "command_content": html_to_markdown(html_content, base_url=base_url),
        "command_url": base_url
    }
