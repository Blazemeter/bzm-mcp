from models.account import Account
from tools.utils import get_date_time_iso


def format_accounts(accounts):
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
