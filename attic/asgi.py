# -*- coding: utf-8 -*-
from app.server import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
