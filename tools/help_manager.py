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
import traceback
from copy import deepcopy
from itertools import chain
from typing import Optional, Any, Dict, List

import httpx
from mcp.server.fastmcp import Context
from pydantic import Field

from config.blazemeter import TOOLS_PREFIX, SUPPORT_MESSAGE, \
    HELP_INDEX_URL, HELP_TOC_URL, HELP_BASE_CONTENT_URL
from config.token import BzmToken
from formatters.help import format_help_info
from models.manager import Manager
from models.result import BaseResult
from tools.help_utils import convert_js_to_py_dict
from tools.utils import http_request


class HelpManager(Manager):
    help_tree = None  # Static to share between different instance of HelpManager
    help_items_index = {}
    help_index_nodes = {}
    help_content_cache = {}

    def __init__(self, token: Optional[BzmToken], ctx: Context):
        super().__init__(token, ctx)

    async def _load_help_tree(self):
        help_index_url = HELP_INDEX_URL
        help_index_response = await http_request("GET", endpoint=help_index_url)

        help_index_response.result = convert_js_to_py_dict(help_index_response.result)

        num_chunks = help_index_response.result.get("numchunks", 2)
        chunk_prefix = help_index_response.result.get("prefix", "azure_toc_public_Chunk")
        help_tree_index = help_index_response.result.get("tree", {})

        # Flat the tree to obtain each item nodes
        help_tree_index_flat = {}
        stack = list(help_tree_index.get("n", []))  # Root

        while stack:
            node = stack.pop()
            children = node.get("n", [])

            node_copy = deepcopy(node)
            node_id = node_copy.get("i")
            node_copy.pop("n", None)
            node_copy.pop("c", None)
            node_copy.pop("i", None)

            help_tree_index_flat[node_id] = {
                **node_copy,
                "n": [ch["i"] for ch in children]
            }
            if children:
                stack.extend(children)

        help_chunk_urls = []

        for i in range(num_chunks):
            help_chunk_url = f"{HELP_TOC_URL}{chunk_prefix}{i}.js"
            help_chunk_urls.append(help_chunk_url)

        async def fetch_chunk(chunk_url: str):
            help_chunk_response = await http_request("GET", endpoint=chunk_url)
            help_chunk_response.result = convert_js_to_py_dict(help_chunk_response.result)
            help_content = []
            for url, content in help_chunk_response.result.items():
                help_item = {"title": content.get("t", [""])[0],
                             "help_id": url.replace("/content/", "").removesuffix(".html"),
                             "help_tree_id": content.get("i", [""])[0]
                             }
                # Exclude '___', release-notes and all the 'signup'
                if help_item.get("help_id") == "___" or help_item.get("help_id").startswith(
                        "/guide/release-notes") or help_item.get("help_id").startswith("signup"):
                    continue
                help_content.append(help_item)
            return help_content

        tasks = [fetch_chunk(url) for url in help_chunk_urls]
        results = await asyncio.gather(*tasks)

        merged = list(chain.from_iterable(results))

        help_tree = {}
        for item in merged:
            tree_id = item.get("help_tree_id", 0)
            sections = item.get("help_id").split("/")
            category = sections[0]
            if len(sections) > 2:
                subcategory = sections[1]
                new_id = "/".join(sections[2:])
            else:
                subcategory = "self"
                new_id = "/".join(sections[1:])

            item["help_id"] = new_id
            if category not in help_tree:
                help_tree[category] = {}
            if subcategory not in help_tree[category]:
                help_tree[category][subcategory] = []
            help_tree[category][subcategory].append(item)

            HelpManager.help_items_index[f"{category}:{subcategory}:{new_id}"] = tree_id

            if tree_id not in HelpManager.help_index_nodes:
                HelpManager.help_index_nodes[tree_id] = {
                    "category": category,
                    "subcategory": subcategory,
                    "help_id": new_id,
                    "sub_nodes": help_tree_index_flat[tree_id]["n"]
                }
        if '' in help_tree.keys():
            help_tree['root_category'] = help_tree.pop('')  # Assign a name to the root category
        HelpManager.help_tree = help_tree

    async def list_help_categories(self) -> BaseResult:
        if HelpManager.help_tree is None:
            await self._load_help_tree()
        categories = []
        for key in HelpManager.help_tree.keys():
            category = {
                "category": key,
                "subcategories": list(HelpManager.help_tree[key].keys()),
            }
            categories.append(category)
        return BaseResult(
            result=categories,
            info=["A list of subcategories is provided for each category"]
        )

    async def list_help_category_content(self, category_id: str, subcategory_id_list: List[str]) -> BaseResult:
        if HelpManager.help_tree is None:
            await self._load_help_tree()
        results = []
        for subcategory_id in subcategory_id_list:
            if subcategory_id == "":
                subcategory_id = "self"
            if category_id in HelpManager.help_tree.keys() and subcategory_id in HelpManager.help_tree[category_id]:
                results.append(HelpManager.help_tree[category_id][subcategory_id])
            else:
                results.append(
                    BaseResult(warning=[f"Category '{category_id}' and subcategory '{subcategory_id}' not found."]))
        return BaseResult(
            result=results,
        )

    @staticmethod
    def get_sub_nodes(category_id: str, subcategory_id: str, help_id: str) -> Any:
        index_id = f"{category_id}:{subcategory_id}:{help_id}"
        sub_nodes_items = []
        if index_id in HelpManager.help_items_index:
            node_id = HelpManager.help_items_index[index_id]
            sub_nodes = HelpManager.help_index_nodes[node_id]["sub_nodes"]
            for sub_node in sub_nodes:
                if sub_node in HelpManager.help_index_nodes:
                    sub_nodes_items.append(HelpManager.help_index_nodes[sub_node])
        return sub_nodes_items

    @staticmethod
    async def get_help_object(category_id: str, subcategory_id: str, help_id: str) -> Any:
        help_cache_key = f"{category_id}:{subcategory_id}:{help_id}"
        help_base_url = HELP_BASE_CONTENT_URL
        help_url = f"{help_base_url}/"  # BlazeMeter doesn't use category_id
        if subcategory_id != "self":
            help_url += f"{subcategory_id}/"

        if not help_id.endswith(".htm"):  # only if it's not a htm extension
            help_url += f"{help_id}.html"  # Restore the html extension
        else:
            help_url += f"{help_id}"

        help_object = {}
        # If it's cached, it returns the cached version.
        if help_cache_key in HelpManager.help_content_cache:
            help_object = HelpManager.help_content_cache[help_cache_key]
            help_object["help_cached"] = True
        else:
            help_object["help_cached"] = False
            try:
                result = await http_request("GET", endpoint=help_url, result_formatter=format_help_info,
                                            result_formatter_params={"base_url": help_url})
                # Expand or "Augment" the content ending with ""
                if result.result is not None:
                    if result.result.get("help_content", "").endswith("In this section:"):
                        help_object["sub_nodes"] = HelpManager.get_sub_nodes(category_id, subcategory_id, help_id)
                    help_object["help_result"] = result.result
                    # Store on cache
                    HelpManager.help_content_cache[help_cache_key] = help_object
                else:
                    help_object["help_result"] = f"URL:{help_url}, Error:{result.error}"
            except httpx.HTTPStatusError as e:
                help_object["help_result"] = f"URL:{help_url}, Error:{e.response.text}"
        help_object["help_id"] = help_id

        return help_object

    async def read_help_info(self, category_id: str, subcategory_id: str, help_id_list: List[str]) -> BaseResult:
        if HelpManager.help_tree is None:
            await self._load_help_tree()
        results = []
        if subcategory_id == "":
            subcategory_id = "self"
        for help_id in help_id_list:
            help_object = await HelpManager.get_help_object(category_id, subcategory_id, help_id)
            results.append(help_object)

        return BaseResult(
            result=[{
                "category_id": category_id,
                "subcategory_id": subcategory_id,
                "help_results": results,
            }],
        )


def register(mcp, token: Optional[BzmToken]):
    @mcp.tool(
        name=f"{TOOLS_PREFIX}_help",
        description="""
Operations on documentation and help information.
**Note**: If you need to call this action multiple times (even with different parameters), 
use the `batch` action instead of making separate calls.
Actions:
- list_help_categories: List all category_ids and for each of them list their subcategory_ids.
- list_help_category_content: List all help_id list related with a category_id and subcategory_id.
    args(dict): Dictionary with the following required parameters:
        category_id (str): The category id.
        subcategory_id_list (List[str]): The subcategory id list.
- read_help_info: Read the content of a help_id providing category_id, subcategory_id and help_id
    args(dict): Dictionary with the following required parameters:
        category_id (str): The category id.
        subcategory_id (str): The sub-category id.
        help_id_list (List[str]): The help id list to read.
- batch: Execute multiple actions in one call.
    args(dict): Dictionary with the following required parameters:
        batch_calls (List[Dict]): List of Actions dictionaries (excluding the action batch), each with 'action' (str) and 'args' (Dict).
Hints:
- Always generates the url attributes as a link in markdown format (like command_url).
- **CRITICAL**: For multiple actions, always use the 'batch' action.
"""
    )
    async def help_main(
            action: str = Field(description="The action id to execute"),
            args: Dict[str, Any] = Field(description="Dictionary with parameters", default=None),
            ctx: Context = Field(description="Context object providing access to MCP capabilities")
    ) -> BaseResult:
        if args is None:
            args = {}
        help_manager = HelpManager(token, ctx)
        try:
            match action:
                case "list_help_categories":
                    return await help_manager.list_help_categories()
                case "list_help_category_content":
                    return await help_manager.list_help_category_content(args.get("category_id", "home"),
                                                                         args.get("subcategory_id_list", []))
                case "read_help_info":
                    return await help_manager.read_help_info(args.get("category_id", "home"),
                                                             args.get("subcategory_id", ""),
                                                             args.get("help_id_list", []))
                case "batch":
                    # Make sure this initialization doesn't run in parallel
                    if HelpManager.help_tree is None:
                        await help_manager._load_help_tree()

                    batch_calls = args.get("batch_calls", [])
                    if not isinstance(batch_calls, list) or not batch_calls:
                        return BaseResult(
                            error="batch_calls must be a non-empty list of dicts with 'action' and 'args'")

                    async def process_call(call: Dict[str, Any]) -> BaseResult | List[BaseResult]:
                        sub_action = call.get("action", "")
                        sub_args = call.get("args", {})
                        try:
                            # Recursively call the skills function itself
                            return await help_main(sub_action, sub_args, ctx)
                        except httpx.HTTPStatusError as e:
                            return BaseResult(error=f"HTTP error in sub-action {sub_action}: {traceback.format_exc()}")
                        except Exception as e:
                            return BaseResult(
                                error=f"Error in sub-action {sub_action}: {traceback.format_exc()}\n{SUPPORT_MESSAGE}")

                    # Parallel execution with asyncio.gather
                    results = await asyncio.gather(*[process_call(call) for call in batch_calls],
                                                   return_exceptions=True)
                    # Handle any exceptions returned
                    processed_results = [
                        r if not isinstance(r, Exception) else BaseResult(error=f"Unhandled exception: {str(r)}")
                        for r in results
                    ]
                    return BaseResult(result=processed_results)
                case _:
                    return BaseResult(
                        error=f"Action {action} not found in help manager tool"
                    )
        except httpx.HTTPStatusError:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}"
            )
        except Exception:
            return BaseResult(
                error=f"Error: {traceback.format_exc()}\n{SUPPORT_MESSAGE}"
            )
