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
from datetime import datetime, timedelta, time
from typing import List, Dict, Any, Tuple

from config.blazemeter import SEARCH_ENDPOINT, BZM_BASE_URL
from config.token import BzmToken
from models.result import BaseResult
from tools.utils import api_request, get_date_time_iso

OPERATORS_VALUES_MAP = {
    "=": {"op": "$eq", "name": "equal"},
    "!=": {"op": "$ne", "name": "not equal"},
    "<": {"op": "$lt", "name": "less than"},
    "<=": {"op": "$lte", "name": "less than or equal"},
    ">": {"op": "$gt", "name": "greater than"},
    ">=": {"op": "$gte", "name": "greater than or equal"},
}


async def search(token: BzmToken, account_id: int, entity: str, fields: List[Any], filters: Dict[str, Any],
                 ordering: List[Any], skip: int = 0, page_size: int = 50,
                 platform: str = "performance") -> BaseResult:
    search_request_body = {
        "entity": entity,
        "fields": fields,
        "accountId": account_id,
        "workspaceId": None,
        "filters": filters,
        "ordering": ordering,
        "distinct": "true",
        "skip": skip, "limit": page_size,
        "platform": platform,
    }
    return await api_request(
        token,
        "POST",
        f"{SEARCH_ENDPOINT}",
        json=search_request_body
    )


def build_filter_list(args: Dict[str, Any], filters_list_map: Dict[str, Any], filters_list: List[Any]) -> List[Any]:
    for filter_list_id in filters_list_map.keys():
        if filter_list_id in args.keys():
            filter_list_values = args.get(filter_list_id, [])
            if len(filter_list_values) > 0:
                filter_id = filters_list_map[filter_list_id]["id"]
                filter_op = filters_list_map[filter_list_id]["op"]
                if filter_op == "op":
                    # Translate operators
                    for filter_op_list in filter_list_values:
                        for filter_op_key, filter_op_value in filter_op_list.items():
                            filter_op_key_mapped = OPERATORS_VALUES_MAP[filter_op_key]["op"]
                            filters_list.append({filter_id: {filter_op_key_mapped: filter_op_value}})
                else:
                    filters_list.append(
                        {filter_id: {filter_op: filter_list_values}}
                    )
    return filters_list


def compute_start_end_filter(time_frame: str = "latest", start_time_str: str = "", end_time_str: str = "") -> Tuple[
    int, int]:
    now_dt = datetime.now()
    start_time_dt = now_dt
    if time_frame == "latest":
        start_time_dt = start_time_dt - timedelta(days=0)
    elif time_frame == "last24":
        start_time_dt = start_time_dt - timedelta(days=1)
    elif time_frame == "lastWeek":
        start_time_dt = start_time_dt - timedelta(days=7)
    elif time_frame == "lastMonth":
        start_time_dt = start_time_dt - timedelta(days=30)
    elif time_frame == "custom":
        start_time_dt = datetime.fromisoformat(start_time_str)
    start_time_dt = start_time_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    start_time = int(start_time_dt.timestamp())
    end_time_dt = datetime.combine(now_dt.date(), time(23, 59, 59))
    end_time = int(end_time_dt.timestamp())
    if time_frame == "custom":
        end_time_dt = datetime.fromisoformat(end_time_str)
        end_time_dt = end_time_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = int(end_time_dt.timestamp())
    return start_time, end_time


async def test_execution_search(entity: str, token: BzmToken, account_id: int, args: dict[str, Any]) -> BaseResult:
    # Paging
    page_size = 50
    page_index = args.get("page_index", 1)
    skip = (page_size * page_index) - page_size

    start_time, end_time = compute_start_end_filter(
        args.get("time_frame", "latest"),
        args.get("start_time", ""),
        args.get("end_time", "")
    )

    execution_name = args.get("execution_name", "")

    filters_list = [
        {
            "name": {
                "$ilike": f"{execution_name}"
            }
        },
    ]

    if entity == "master":
        filters_list.append(
            {
                "runDateFrom": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            }
        )
    elif entity == "test-union":
        filters_list.append(
            {
                "created": {
                    "$gte": start_time,
                    "$lte": end_time
                }
            }
        )

    filters_list_map = {
        "workspace_id_list": {"id": "workspace.id", "op": "$in"},
        "cloud_provider_name_list": {"id": "locations.provider", "op": "$in"},
        "created_by_id_list": {"id": "userId", "op": "$in"},
        "locations_id_list": {"id": "locations.id", "op": "$in"},
        "project_id_list": {"id": "projectId", "op": "$in"},
        "duration_list": {"id": "duration", "op": "op"},
        "number_of_engines_list": {"id": "numEngines", "op": "op"},
        "virtual_users_list": {"id": "numVirtualUsers", "op": "op"},
    }
    filters_list = build_filter_list(args, filters_list_map, filters_list)

    if entity == "master":
        fields = ["*", "owner.*", "project.*", "locations.*", "workspace.*", "tags.*", "runner.*"]
    elif entity == "test-union":
        fields = ["*", "owner.*", "project.*", "locations.*", "workspace.*", "tags.*"]
    filters = {"$and": filters_list}
    if entity == "master":
        ordering = [{"runDateFrom": -1}]
    elif entity == "test-union":
        ordering = [{"updated": -1}]
    filter_result = await search(
        token, account_id,
        entity,
        fields,
        filters,
        ordering,
        skip, page_size,
        "performance"
    )

    search_result = []
    for element in filter_result.result:
        if entity == "master":
            id_key = "execution_id"
            id_value = element.get("id")
            name_key = "execution_name"
            name_value = element.get("name")
            created = get_date_time_iso(element.get("runDateFrom"))
            ended = get_date_time_iso(element.get("runDateTo"))
            user_id = element.get("runner").get("id")
            user_display_name = element.get("runner").get("displayName")
            id_url_key = "execution_url"
            id_url = f"{BZM_BASE_URL}/app/#/masters/{id_value}"
        elif entity == "test-union":
            id_key = "test_id"
            id_value = element.get("id")
            name_key = "test_name"
            name_value = element.get("name")
            created = get_date_time_iso(element.get("created"))
            ended = created
            user_id = element.get("owner").get("id")
            user_display_name = element.get("owner").get("displayName")
            id_url_key = "test_url"
            id_url = f"{BZM_BASE_URL}/app/#/tests/{id_value}"

        formated_element = {
            id_key: id_value,
            name_key: name_value,
            "created": created,
            "ended": ended,
            "updated": get_date_time_iso(element.get("updated")),
            "users": element.get("numVirtualUsers"),
            "project_id": element.get("project").get("id"),
            "project_name": element.get("project").get("name"),
            "duration": element.get("duration"),
            "user_id": user_id,
            "user_display_name": user_display_name,
            "workspace_id": element.get("workspace").get("id"),
            "workspace_name": element.get("workspace").get("name"),
            "engines": element.get("numEngines"),
            id_url_key: id_url,
        }
        locations = element.get("locations")
        locations = [] if locations is None else locations
        locations_titles = []
        locations_ids = []
        for location in locations:
            locations_ids.append(location.get("id"))
            locations_titles.append(location.get("title"))
        formated_element["locations_titles"] = ",".join(locations_titles)
        formated_element["locations_ids"] = ",".join(locations_ids)

        search_result.append(formated_element)

    return BaseResult(
        result=search_result,
        error=filter_result.error,
        warning=filter_result.warning,
        total=filter_result.total,
        has_more=filter_result.has_more,
    )


async def test_execution_search_filter_values(entity: str, account_id: int, token: BzmToken,
                                              filter_names: List[str]) -> BaseResult:
    filters_fields_map = {
        "workspace_id_list": ["workspace.accountId", "workspace.id", "workspace.name"],
        "cloud_provider_name_list": ["locations.provider"],
        "locations_id_list": ["locations.id", "locations.title"],
        "project_id_list": ["project.id", "project.name", "project.workspaceId"],
        "tag_id_list": ["tags.id", "tags.label", "tags.workspaceId"]
    }

    if entity == "master":
        filters_fields_map["created_by_id_list"] = ["runner.id", "runner.displayName"]
    elif entity == "test-union":
        filters_fields_map["created_by_id_list"] = ["owner.id", "owner.displayName"]

    result_entity_map = {
        "workspace_id_list": "workspace",
        "cloud_provider_name_list": "provider",
        "locations_id_list": "location",
        "project_id_list": "project",
        "tag_id_list": "tags",
    }

    if entity == "master":
        result_entity_map["created_by_id_list"] = "runner"
    elif entity == "test-union":
        result_entity_map["created_by_id_list"] = "owner"

    operators_list = [
        'duration_list',
        "number_of_engines_list",
        "virtual_users_list",
    ]
    filter_value_info = {
        'duration_list': {"type": "int", "description": "duration value in seconds"},
        'number_of_engines_list': {"type": "int", "description": "number of engines"},
        'virtual_users_list': {"type": "int", "description": "number of virtual users"},
    }
    numeric_usage_filter = "Each list item MUST be a single-key object: the key is the operator string, and the value is the value as the data type defined. Examples: [{\">=\": 2}]"
    filter_usage_info = {
        'duration_list': numeric_usage_filter,
        'number_of_engines_list': numeric_usage_filter,
        'virtual_users_list': numeric_usage_filter,
    }

    result_field_map = {
        "workspace.accountId": "account_id",
        "workspace.id": "workspace_id",
        "workspace.name": "workspace_name",
        "provider.provider": "provider_name",
        "owner.id": "user_id",
        "owner.displayName": "display_name",
        "runner.id": "user_id",
        "runner.displayName": "display_name",
        "location.id": "location_id",
        "location.title": "location_title",
        "project.id": "project_id",
        "project.name": "project_name",
        "project.workspaceId": "workspace_id",
        "tags.id": "tags_id",
        "tags.label": "tags_label",
        "tags.workspaceId": "workspace_id",
    }
    filter_request_body_template = {
        "entity": entity,
        "fields": None,
        "accountId": account_id,
        "workspaceId": None,
        "filters": {"$and": []},
        "ordering": [],
        "format": "flat",
        "distinct": "true",
        "skip": 0, "limit": 999,
        "platform": "performance",
    }
    # Get the metadata for each filter name using the search api
    filter_values = {}
    filter_not_found = []
    valid_filters = ['workspace_id_list', 'cloud_provider_name_list', 'created_by_id_list', 'locations_id_list',
                     'project_id_list', 'tag_id_list', 'duration_list', 'number_of_engines_list',
                     'virtual_users_list']
    for filter_name in filter_names:
        if filter_name in valid_filters:
            # Detect operator or list values type
            if filter_name in operators_list:
                filter_values[filter_name] = {
                    "operators": list(OPERATORS_VALUES_MAP.keys()),
                    "value_info": filter_value_info[filter_name],
                    "usage_info": filter_usage_info[filter_name],
                }
            else:
                filter_entity = result_entity_map[filter_name]
                filter_request_body = filter_request_body_template.copy()
                filter_request_body["fields"] = filters_fields_map[filter_name]
                filter_result = await api_request(
                    token,
                    "POST",
                    f"{SEARCH_ENDPOINT}",
                    json=filter_request_body
                )
                filter_result_formated = []
                for element in filter_result.result:
                    element_formated = {}
                    for k, v in element.items():
                        new_k = result_field_map[f"{filter_entity}.{k}"]
                        element_formated[new_k] = v
                    filter_result_formated.append(element_formated)
                filter_values[filter_name] = filter_result_formated
        else:
            filter_not_found.append(filter_name)
    error = None
    warnings = None
    if len(filter_not_found) > 0:
        error = f"Error, invalid filter_names values: {','.join(filter_not_found)}"
        warnings = [f"Make sure to use valid filter_names values: {','.join(valid_filters)}"]
    return BaseResult(
        result=[filter_values],
        error=error,
        warning=warnings,
        has_more=False,
    )
