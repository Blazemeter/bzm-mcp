"""
Copyright 2025 Perforce Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
from itertools import islice

import httpx
import pytest

from config.blazemeter import HELP_INDEX_URL, HELP_TOC_URL
from tools.help_utils import convert_js_to_py_dict, html_to_markdown
from tools.utils import http_request


class TestHelpLiveHrefRendering:
    def test_live_help_page_does_not_contain_literal_href_template(self):
        async def _run():
            help_index_response = await http_request("GET", endpoint=HELP_INDEX_URL)
            if help_index_response.error:
                pytest.skip(f"Help index not reachable: {help_index_response.error}")

            index_data = convert_js_to_py_dict(help_index_response.result)
            chunk_prefix = index_data.get("prefix", "azure_toc_public_Chunk")
            chunk_url = f"{HELP_TOC_URL}{chunk_prefix}0.js"

            chunk_response = await http_request("GET", endpoint=chunk_url)
            if chunk_response.error:
                pytest.skip(f"Help chunk not reachable: {chunk_response.error}")

            chunk_data = convert_js_to_py_dict(chunk_response.result)
            page_response = None
            page_url = None
            for help_path in islice(chunk_data.keys(), 30):
                candidate_url = f"https://help.blazemeter.com{help_path}"
                try:
                    page_response = await http_request("GET", endpoint=candidate_url)
                    page_url = candidate_url
                    break
                except httpx.HTTPStatusError:
                    continue

            if page_response is None or page_url is None:
                pytest.skip("Could not fetch a live help page with HTTP 200 from first chunk.")

            markdown = html_to_markdown(page_response.result, base_url=page_url)
            assert "{href}" not in markdown

        asyncio.run(_run())
