from fastapi import APIRouter, HTTPException, Depends, Query
from database import verify_user

router = APIRouter()

@router.get("/verify")
async def verify_user_token(email: str = Query(..., alias="user_email"), token: str = Query(...)):
    verification_result = verify_user(email, token)
    if verification_result == "Email verification successful.":
        return {"message": "Verification successful"}
    elif verification_result == "This account has already been verified.":
        raise HTTPException(status_code=400, detail="This account has already been verified.")
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")