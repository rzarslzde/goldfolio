from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
from app.routes_auth import router as auth_router
from app.routes_portfolio import router as portfolio_router
from app.seed import ensure_seed_data

app = FastAPI(title="Goldfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ensure_seed_data(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"ok": True}


app.include_router(auth_router)
app.include_router(portfolio_router)
