from typing import Annotated

from fastapi import APIRouter, Depends

from src.schemas.auth.token_response import TokenResponseDTO
from src.services.auth import AuthService, PasswordFormDep

AuthServiceDep = Annotated[AuthService, Depends()]

router = APIRouter()


@router.post("/login")
async def login_for_access_token(
    service: AuthServiceDep,
    form_data: PasswordFormDep
) -> TokenResponseDTO:
    return service.get_access_token(form_data)
