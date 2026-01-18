from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Nome do usuário (único)",
    )
    email: str = Field(
        ...,
        description="Email do usuário (único)",
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Senha do usuário",
    )


class UserResponse(BaseModel):
    username: str
    email: str
    user_id: int

    @classmethod
    def from_entity(cls, entity) -> "UserResponse":
        return cls(
            username=entity.username,
            email=entity.email,
            user_id=entity.id,
        )


class UserDetailResponse(BaseModel):
    user_id: int
    username: str
    email: str

    @classmethod
    def from_entity(cls, entity) -> "UserDetailResponse":
        return cls(
            user_id=entity.id,
            username=entity.username,
            email=entity.email,
        )
