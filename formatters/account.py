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
from typing import Optional, List

from models.account import Account
from tools.utils import get_date_time_iso


def format_accounts(accounts, params: Optional[dict] = None) -> List[Account]:
    formatted_accounts = []
    for account in accounts:
        formatted_accounts.append(
            Account(
                account_id=account.get("id"),
                account_name=account.get("name", "Unknown"),
                description=account.get("description", ""),
                ai_consent=account.get("aiConsent", None),
                created=get_date_time_iso(account.get("created")),
                updated=get_date_time_iso(account.get("updated")),
            )
        )
    return formatted_accounts
