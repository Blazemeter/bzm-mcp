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

from config.blazemeter import SEARCH_ENDPOINT
from config.token import BzmToken
from models.result import BaseResult
from tools.utils import api_request


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
