from fastapi import HTTPException


class DuplicatePublicationNameError(HTTPException):
    def __init__(self, detail: str = "Duplicate publication name"):
        super().__init__(status_code=400, detail=detail)


class InvalidInputError(HTTPException):
    def __init__(self, detail: str = "Invalid input"):
        super().__init__(status_code=400, detail=detail)


class RepositoryError(HTTPException):
    def __init__(self, detail: str = "Repository error"):
        super().__init__(status_code=500, detail=detail)


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Authentication error"):
        super().__init__(status_code=401, detail=detail)
