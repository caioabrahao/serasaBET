from sqlalchemy.orm import Session
from models import Event

def add_event(db, name, date, description, category, created_by):
    new_event = Event(
        name=name,
        date=date,
        description=description,
        category=category,
        created_by=created_by,
        status='pending'
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def get_events(db, status=None):
    query = db.query(Event)
    if status:
        query = query.filter(Event.status == status)
    return query.all()

def delete_event(db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event:
        event.status = 'deleted'  # Excluir
        db.commit()
        return event
    return None

def evaluate_event(db, event_id, approve):
    # Buscar o evento no banco de dados
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        return {"message": "Event not found"}, 404

    if approve:
        event.status = 'approved'
        event.approved = True
    else:
        event.status = 'rejected'
        event.approved = False

    db.commit()
    db.refresh(event)
    return event