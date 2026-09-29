from sqlalchemy.orm import Session

from app.config import settings
from app.models import PriceSnapshot, User
from app.security import get_password_hash


def ensure_seed_data(db: Session) -> None:
    admin = db.query(User).filter(User.username == settings.admin_username).first()
    if not admin:
        admin = User(username=settings.admin_username, password_hash=get_password_hash(settings.admin_password))
        db.add(admin)

    prices = db.query(PriceSnapshot).filter(PriceSnapshot.id == 1).first()
    if not prices:
        prices = PriceSnapshot(id=1, gram_18k=0, half_coin=0, quarter_coin=0, bahar_coin=0)
        db.add(prices)

    db.commit()
