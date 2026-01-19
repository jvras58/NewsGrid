from fastapi import HTTPException

from app.core.container import Container

container = Container()


async def login(username: str, password: str, session):
    use_case = container.login_use_case()
    try:
        return await use_case.execute(session, username, password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
