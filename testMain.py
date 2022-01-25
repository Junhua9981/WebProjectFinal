from asyncio import ProactorEventLoop, get_event_loop
from uvicorn import Config, Server
from fastapi import FastAPI
from app import app
# FIX Windows Socket limit of 509
# 使用這個檔案啟動服務的話port會開在8000 在windows上就不會有selector error
# 因為windows的socket有限制
# 如果要啟動服務的話要改成

# Linux 則用main.py就好
if __name__ == "__main__":
    server = Server(config=Config(app=app,loop=ProactorEventLoop(),debug=True,reload=True))
    get_event_loop().run_until_complete(server.serve())