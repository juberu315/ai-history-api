from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud


app = FastAPI(
    title="AI History API",
    description="FastAPI project for saving AI request and response history.",
    version="1.0.0"
)


@app.get("/")
def api_status():
    return {
        "message": "AI History API is running",
        "status": "success"
    }


@app.post("/users", response_model=schemas.UserResponse)
def create_user(
    request: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, request)


@app.post("/chat", response_model=schemas.AIProcessResponse)
def chat(
    request: schemas.AIProcessRequest,
    db: Session = Depends(get_db)
):
    user = crud.get_user(db, request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Replace this later with real OpenAI response.
    ai_result = f"AI chat response for: {request.input}"

    ai_request = crud.save_ai_history(
        db=db,
        user_id=request.user_id,
        endpoint_type="chat",
        input_text=request.input,
        output_text=ai_result
    )

    return {
        "result": ai_result,
        "request_id": ai_request.id
    }


@app.post("/summarize", response_model=schemas.AIProcessResponse)
def summarize(
    request: schemas.AIProcessRequest,
    db: Session = Depends(get_db)
):
    user = crud.get_user(db, request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ai_result = f"Summary for: {request.input}"

    ai_request = crud.save_ai_history(
        db=db,
        user_id=request.user_id,
        endpoint_type="summarize",
        input_text=request.input,
        output_text=ai_result
    )

    return {
        "result": ai_result,
        "request_id": ai_request.id
    }


@app.post("/translate", response_model=schemas.AIProcessResponse)
def translate(
    request: schemas.AIProcessRequest,
    db: Session = Depends(get_db)
):
    user = crud.get_user(db, request.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ai_result = f"Translated text for: {request.input}"

    ai_request = crud.save_ai_history(
        db=db,
        user_id=request.user_id,
        endpoint_type="translate",
        input_text=request.input,
        output_text=ai_result
    )

    return {
        "result": ai_result,
        "request_id": ai_request.id
    }


@app.get("/history", response_model=list[schemas.AIHistoryResponse])
def view_history(
    endpoint_type: str | None = None,
    db: Session = Depends(get_db)
):
    return crud.get_history(db, endpoint_type)


@app.delete("/history/{request_id}")
def remove_history(
    request_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_history(db, request_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="History not found")

    return {
        "message": "History deleted successfully"
    }


@app.get("/history/stats/count")
def request_count(db: Session = Depends(get_db)):
    total = crud.count_requests(db)

    return {
        "total_requests": total
    }