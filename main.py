import logging.config
from fastapi import FastAPI, Request
from service import IntegrationService
from dotenv import load_dotenv
import uvicorn
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

if not os.path.exists('./logs'):
    os.mkdir('logs')

logging.basicConfig(level=logging.DEBUG,
                    format="<%(asctime)s> [%(levelname)s]: %(message)s",
                    handlers=[
                        TimedRotatingFileHandler(f'./logs/integration1c-{datetime.date.today().isoformat()}.log', when="D", backupCount=0),
                        logging.StreamHandler()
                    ])

load_dotenv()

app = FastAPI()
service = IntegrationService()


@app.get('/ping')
async def ping(request: Request):
    client_host = request.client.host

    logging.debug(f'{__name__}.ping - ping from {client_host}')

    return "pong"


@app.post('/')
async def save_data(request: Request):
    body_json = await request.json()
    our_org_code = body_json['OurOrg']['OurOrgCode']

    body_bytes = await request.body()
    body_str = body_bytes.decode('utf-8')

    client_host = request.client.host

    logging.debug(f'{__name__}.save_data - from {client_host} >> [{our_org_code}] >> {body_str}')

    last_request_id = await service.get_last_request_id()

    next_request_id = last_request_id + 1
    result = await service.save_json_data(next_request_id, client_host, our_org_code, body_str)

    return result


if __name__ == '__main__':
    uvicorn.run('main:app',
                host=os.environ['APP_HOST'],
                port=int(os.environ['APP_PORT']),
                log_level='trace')