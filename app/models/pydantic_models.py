from pydantic import BaseModel


class ReceivedToken(BaseModel):
    token: str
