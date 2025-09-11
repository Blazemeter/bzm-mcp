from typing import List, Any

from models.user import User
from tools.utils import get_date_time_iso


def format_users(users: List[Any]) -> List[User]:
    formatted_users = []
    for user in users:
        user_element = User(
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
        formatted_users.append(user_element)

    return formatted_users
