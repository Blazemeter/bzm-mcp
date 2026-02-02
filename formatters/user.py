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
from typing import List, Any, Optional

from models.user import User
from tools.utils import get_date_time_iso


def format_users(users: List[Any], params: Optional[dict] = None) -> List[User]:
    formatted_users = []
    for user in users:
        formatted_users.append(
            User(
                user_id=user.get("id"),
                display_name=user.get("displayName"),
                first_name=user.get('firstName'),
                last_name=user.get('lastName'),
                email=user.get("email"),
                access=get_date_time_iso(user.get("access")),
                login=get_date_time_iso(user.get("login")),
                created=get_date_time_iso(user.get("created")),
                updated=get_date_time_iso(user.get("updated")),
                time_zone=user.get("timezone", 0),
                enabled=user.get("enabled"),
                default_project_id=user.get("defaultProjectId"),
            )
        )
    return formatted_users
