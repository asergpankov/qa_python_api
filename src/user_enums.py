from enum import Enum


class Gender(Enum):
    female = "female"
    male = "male"


class Statuses(Enum):
    inactive = "inactive"
    active = "active"


class UserErrors(Enum):
    WRONG_EMAIL = "[WARN]-- email doesn't contain '@' symbol"
    EXP_STATUS_200 = "[WARN] -- expected 200, smth went wrong"
    EXP_STATUS_404 = "[WARN] -- expected 404, smth went wrong"
    EXP_COUNT = "[WARN] -- expected 100 objects in [response]"


class BaseUrls(Enum):
    DEV_URL = "https://jsonplaceholder.typicode.com"
    STAGING_URL = "https://jsonplaceholder-rc.typicode.com"
