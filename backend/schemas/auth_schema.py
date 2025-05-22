from pydantic import BaseModel, EmailStr

# Schemat do logowania użytkownika
class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

# Schemat odpowiedzi zawierającej token uwierzytelniający
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
