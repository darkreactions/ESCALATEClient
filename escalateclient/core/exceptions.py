import requests


class LoginError(Exception):
    """ Raised when there is a login issue """

    def __init__(self, r: requests.Response) -> None:
        message = f'Login failed, Code {r.status_code}: {r.reason} {r.text}'
        super().__init__(message)
