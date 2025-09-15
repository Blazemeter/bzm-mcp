from typing import Optional

from pydantic import BaseModel, Field


class Account(BaseModel):
    account_id: int = Field("The unique identifier of the account")
    account_name: str = Field("The name of the account")
    description: str = Field("The description of the account")
    ai_consent: Optional[bool] = Field("The AI Consent")
    created: str = Field("The datetime that the account was created")
    updated: str = Field("The datetime that the account was updated")
