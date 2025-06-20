from pydantic import BaseModel, EmailStr

# Schema for validating user creation data from the request body
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Schema for formatting the user data in the response
class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
