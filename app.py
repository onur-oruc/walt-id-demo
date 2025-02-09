from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import auth
import did_service
import key_service
from oem_service import OEMService
import vc_issuer
import vc_verifier
from pydantic import BaseModel
from jose import jwt, JWTError
from typing import Optional


class LoginResponse(BaseModel):
    id: str
    username: str
    token: str


class LoginRequest(BaseModel):
    email: str
    password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(title="Walt.id API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Walt.id API"}


@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    try:
        return auth.login_with_email(request.email, request.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"token": token}


@app.get("/protected")
async def protected_route(user_data: dict = Depends(get_current_user)):
    return {"message": "This is a protected route", "token": user_data["token"]}


@app.post("/battery/did")
async def create_battery_did(
    request: dict, current_user: dict = Depends(get_current_user)
):
    oem = OEMService()
    return oem.create_battery_did(request["serial_number"], current_user["token"])


@app.post("/issuer/oem/onboard")
async def onboard_oem_issuer(current_user: dict = Depends(get_current_user)):
    oem = OEMService()
    return oem.create_oem_issuer_did_web(current_user["token"])


@app.post("/issuer/oem/battery/{serial_number}/initial-vc")
async def create_oem_vc(
    serial_number: str, current_user: dict = Depends(get_current_user)
):
    oem = OEMService()
    return oem.create_initial_battery_vc(serial_number, current_user["token"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
