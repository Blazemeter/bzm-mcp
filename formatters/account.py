from tools.utils import get_date_time_iso


def format_accounts(accounts):
    formatted_accounts = []
    for account in accounts:
        formatted_account = {
            "account_id": account.get("id"),
            "account_name": account.get("name", "Unknown"),
            "description": account.get("description", ""),
            "created": get_date_time_iso(account.get("created")),
            "updated": get_date_time_iso(account.get("updated")),
        }
        formatted_accounts.append(formatted_account)
    return formatted_accounts
