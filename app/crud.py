from sqlalchemy.orm import Session
from app import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def save_ai_history(
    db: Session,
    user_id: int,
    endpoint_type: str,
    input_text: str,
    output_text: str
):
    ai_request = models.AIRequest(
        user_id=user_id,
        endpoint_type=endpoint_type,
        input_text=input_text
    )

    db.add(ai_request)
    db.commit()
    db.refresh(ai_request)

    ai_response = models.AIResponse(
        request_id=ai_request.id,
        output_text=output_text
    )

    db.add(ai_response)
    db.commit()
    db.refresh(ai_response)

    return ai_request


def get_history(db: Session, endpoint_type: str | None = None):
    query = (
        db.query(models.AIRequest, models.AIResponse)
        .join(models.AIResponse)
        .order_by(models.AIRequest.created_at.desc())
    )

    if endpoint_type:
        query = query.filter(models.AIRequest.endpoint_type == endpoint_type)

    rows = query.all()

    return [
        {
            "request_id": request.id,
            "user_id": request.user_id,
            "endpoint_type": request.endpoint_type,
            "input_text": request.input_text,
            "output_text": response.output_text,
            "created_at": request.created_at,
        }
        for request, response in rows
    ]


def delete_history(db: Session, request_id: int):
    ai_request = (
        db.query(models.AIRequest)
        .filter(models.AIRequest.id == request_id)
        .first()
    )

    if not ai_request:
        return None

    db.delete(ai_request)
    db.commit()

    return ai_request


def count_requests(db: Session):
    return db.query(models.AIRequest).count()