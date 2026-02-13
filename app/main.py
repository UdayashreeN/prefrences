from fastapi import FastAPI
from .database import engine, Base
from .routers import preferences


# Create DB tables if they do not exist (use migrations for production)
Base.metadata.create_all(bind=engine)


app = FastAPI(title="Preferences Service")
app.include_router(preferences.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "preferences"}