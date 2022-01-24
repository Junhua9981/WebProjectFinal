from asyncio import ProactorEventLoop, get_event_loop
from uvicorn import Config, Server
from fastapi import FastAPI
from app import app

if __name__ == "__main__":
    server = Server(config=Config(app=app,loop=ProactorEventLoop(),debug=True,reload=True))
    get_event_loop().run_until_complete(server.serve())