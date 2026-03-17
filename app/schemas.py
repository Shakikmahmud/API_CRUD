from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=4, max_length=72)


class LoginRequest(BaseModel):
    username: str
    password: str = Field(..., min_length=4, max_length=72)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class MovieBase(BaseModel):
    title: str
    director: str
    genre: str
    year: int
    rating: float


class MovieCreate(MovieBase):
    pass


class MovieUpdate(MovieBase):
    pass


class MovieResponse(MovieBase):
    id: int

    class Config:
        from_attributes = True