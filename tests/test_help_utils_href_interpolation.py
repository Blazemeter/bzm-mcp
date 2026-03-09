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

import lxml.html

from tools.help_utils import process_inline_elements, table_to_markdown, html_to_markdown


class TestHelpUtilsHrefInterpolation:
    def test_process_inline_elements_interpolates_href_in_html_mode(self):
        element = lxml.html.fromstring("<p>Go <a href='/docs/page.html'>here</a></p>")

        rendered = process_inline_elements(
            element,
            base_url="https://help.blazemeter.com",
            as_html=True,
        )

        assert "<a href='https://help.blazemeter.com/docs/page.html'>here</a>" in rendered
        assert "{href}" not in rendered

    def test_table_to_markdown_interpolates_href_inside_html_table_cells(self):
        table = lxml.html.fromstring(
            "<table>"
            "<tr><th>Doc</th></tr>"
            "<tr><td><a href='/docs/guide.html'>Guide</a></td></tr>"
            "</table>"
        )

        rendered = table_to_markdown(
            table,
            base_url="https://help.blazemeter.com",
            as_html=True,
        )

        assert "<a href='https://help.blazemeter.com/docs/guide.html'>Guide</a>" in rendered
        assert "{href}" not in rendered

    def test_html_to_markdown_outputs_markdown_links_without_literal_template(self):
        html = (
            "<html><body><main>"
            "<p>Read <a href='/docs/start.html'>Start</a></p>"
            "</main></body></html>"
        )
        rendered = html_to_markdown(html, base_url="https://help.blazemeter.com")

        assert "[Start](https://help.blazemeter.com/docs/start.html)" in rendered
        assert "{href}" not in rendered
