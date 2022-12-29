from fastapi import FastAPI
from pydantic import BaseModel
import logging
import random
import string
from requests import Request
import time
from italian_driver import respond_to_message

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
logger.info("logging from the root logger") 



app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response

@app.get("/chat/")
async def create_item():
    return {"hello":"world"}

class Message(BaseModel):
    message: str
    

@app.post("/chat/")
async def create_item(message: Message):
    return respond_to_message(message.message)