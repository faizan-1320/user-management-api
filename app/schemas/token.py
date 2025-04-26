from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    cellnumber: str | None = None


class TokenBase(BaseModel):
    token: str
    ttl: int
    userId: int


class TokenCreate(TokenBase):
    pass
