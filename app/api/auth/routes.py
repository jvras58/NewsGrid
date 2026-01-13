from fastapi import APIRouter, Response, Request, Depends
from app.api.auth.schemas import LoginRequest
from app.api.auth.controller import login_logic, logout_logic, verify_session

router = APIRouter()


@router.post("/login")
async def login(response: Response, data: LoginRequest):
    """Troca credenciais (Token) por Sessão (Cookie)."""
    return login_logic(data.token, response)


@router.post("/logout")
async def logout(response: Response, request: Request):
    """Encerra a sessão."""
    return logout_logic(request, response)


@router.get("/me")
async def get_current_user(username: str = Depends(verify_session)):
    """Verifica quem está logado."""
    return {"username": username, "status": "authenticated"}
