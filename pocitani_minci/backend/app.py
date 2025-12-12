from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import register_routes

def create_app() -> FastAPI:
    app = FastAPI(
        title="Coin Detection API",
        description="API for detecting and counting coins in images",
        version="1.0.0"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_routes(app)
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
