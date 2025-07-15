from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from together import Together
from . import auth, models, schemas
import os

from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
client = Together(api_key=os.getenv("bcd2dd05a7e39583b65eab3b13a6f825744234645d15604203de39ec1058e831"))

@router.post("/chat")
def chat(request: schemas.ChatRequest, db: Session = Depends(auth.get_db), user: models.User = Depends(auth.get_current_user)):
    try:
        # Call Together API
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": m.role, "content": m.content} for m in request.messages]
        )

        reply = response.choices[0].message  # assistant reply

        # Save messages to DB
        for m in request.messages:
            db.add(models.Message(user_id=user.id, role=m.role, content=m.content))
        db.add(models.Message(user_id=user.id, role=reply.role, content=reply.content))
        db.commit()

        # Return reply only
        return {"role": reply.role, "content": reply.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
