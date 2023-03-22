import json
import string
from pydantic import BaseModel, ValidationError, validator, Field, root_validator
from typing import Optional
from src.user_enums import UserErrors
import re


class UserSchema(BaseModel):
    id: int = Field(ge=0)
    name: str
    email: str
    gender: Optional[str]
    status: Optional[str]

    @validator("id")
    def id_valid(cls, id: int) -> int:
        if len(str(id)) != 4:
            raise ValueError("'id' must be at least 4 characters long")
        if not all(d.isnumeric() for d in str(id)):
            raise ValueError("'id' must consist only from digits")
        if not id >= 0:
            raise ValueError("'id' must be positive")
        return id

    @validator("name")
    def name_valid(cls, name):
        if any(p in name for p in "!#$%&'()*+,-/:;<=>?@[\]^_`{|}~"):
            # string.punctuation without dot
            raise ValueError("'name' must not include punctuation symbols")
        return name

    @validator("email")
    def check_dog_presented_in_email(cls, email):
        if "@" not in email:
            raise ValueError(UserErrors.WRONG_EMAIL.value)
        return email

    @root_validator(pre=True)
    def validate_gender_or_status_are_inputed(cls, values):
        if "gender" or "status" in values:
            return values
        else:
            raise ValueError("input at least 'gender' or 'status'")


class GetPosts(BaseModel):
    userId: int = Field(ge=1, le=10)
    id: int = Field(gt=0, lt=101)
    title: str = Field(max_length=100)
    body: str = Field(max_length=300)

    @validator("title")
    def expect_title_without_punctuation_symbols(cls, title):
        if any(p in title for p in string.punctuation):
            raise ValidationError("'title' must not include punctuation symbols")
        return title

    @validator("body")
    def expect_body_without_digits(cls, body):
        if any(d in body for d in string.digits):
            raise ValidationError("'body' must not include any digits")
        return body
