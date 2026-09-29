from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Holding, PriceSnapshot
from app.schemas import HoldingInput, HoldingOutput, PortfolioSummary, PriceInput, PriceOutput

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/prices", response_model=PriceOutput)
def get_prices(db: Session = Depends(get_db), _=Depends(get_current_user)):
    price = db.query(PriceSnapshot).filter(PriceSnapshot.id == 1).first()
    if not price:
        price = PriceSnapshot(id=1, gram_18k=0, half_coin=0, quarter_coin=0, bahar_coin=0)
        db.add(price)
        db.commit()
        db.refresh(price)
    return price


@router.put("/prices", response_model=PriceOutput)
def upsert_prices(payload: PriceInput, db: Session = Depends(get_db), _=Depends(get_current_user)):
    price = db.query(PriceSnapshot).filter(PriceSnapshot.id == 1).first()
    if not price:
        price = PriceSnapshot(id=1)
        db.add(price)

    price.gram_18k = payload.gram_18k
    price.half_coin = payload.half_coin
    price.quarter_coin = payload.quarter_coin
    price.bahar_coin = payload.bahar_coin
    db.commit()
    db.refresh(price)
    return price


@router.get("/holdings", response_model=list[HoldingOutput])
def list_holdings(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return db.query(Holding).order_by(Holding.id.desc()).all()


@router.post("/holdings", response_model=HoldingOutput)
def add_holding(payload: HoldingInput, db: Session = Depends(get_db), _=Depends(get_current_user)):
    if payload.asset_type not in {"18k_gram", "half_coin", "quarter_coin", "bahar_coin"}:
        raise HTTPException(status_code=400, detail="Unsupported asset_type")

    row = Holding(asset_type=payload.asset_type, quantity=payload.quantity)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.put("/holdings/{holding_id}", response_model=HoldingOutput)
def update_holding(holding_id: int, payload: HoldingInput, db: Session = Depends(get_db), _=Depends(get_current_user)):
    row = db.query(Holding).filter(Holding.id == holding_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Holding not found")

    if payload.asset_type not in {"18k_gram", "half_coin", "quarter_coin", "bahar_coin"}:
        raise HTTPException(status_code=400, detail="Unsupported asset_type")

    row.asset_type = payload.asset_type
    row.quantity = payload.quantity
    db.commit()
    db.refresh(row)
    return row


@router.delete("/holdings/{holding_id}")
def delete_holding(holding_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    row = db.query(Holding).filter(Holding.id == holding_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Holding not found")
    db.delete(row)
    db.commit()
    return {"ok": True}


@router.get("/summary", response_model=PortfolioSummary)
def summary(db: Session = Depends(get_db), _=Depends(get_current_user)):
    price = db.query(PriceSnapshot).filter(PriceSnapshot.id == 1).first()
    if not price:
        price = PriceSnapshot(id=1, gram_18k=0, half_coin=0, quarter_coin=0, bahar_coin=0)

    holdings = db.query(Holding).all()
    by_asset = {
        "18k_gram": 0.0,
        "half_coin": 0.0,
        "quarter_coin": 0.0,
        "bahar_coin": 0.0,
    }

    price_map = {
        "18k_gram": price.gram_18k,
        "half_coin": price.half_coin,
        "quarter_coin": price.quarter_coin,
        "bahar_coin": price.bahar_coin,
    }

    for h in holdings:
        by_asset[h.asset_type] += h.quantity * price_map.get(h.asset_type, 0)

    total = sum(by_asset.values())
    return PortfolioSummary(total_irt=total, by_asset=by_asset)
