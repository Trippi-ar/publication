from fastapi import Depends, status
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException


from app.repository import repository





def autocomplete(db: Session, word: str):
    if word == "":
        raise (
            HTTPException(status_code=status.HTTP_404_CONFLICT, detail="Word not provide")
        )
    
    suggestions = repository.get_suggestions(db, word)

    return suggestions