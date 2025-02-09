from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import auth
import did_service
import key_service
import vc_issuer
import vc_verifier
from pydantic import BaseModel
import jwt
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
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"user_id": user_id, "token": token}
    except jwt.JWTError:
        raise credentials_exception


@app.get("/protected")
async def protected_route(user_data: dict = Depends(get_current_user)):
    return {
        "message": "This is a protected route",
        "user_id": user_data["user_id"],
        "decoded_token": jwt.decode(
            user_data["token"], options={"verify_signature": False}
        ),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
