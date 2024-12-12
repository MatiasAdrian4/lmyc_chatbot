import uvicorn
from fastapi import FastAPI

from routes import messages

app = FastAPI()

app.include_router(messages.router, prefix="/messages", tags=["messages"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
