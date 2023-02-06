from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

APP_3_ALIASES = "host.docker.internal"


class Body(BaseModel):
    text: str


def perform_call(text: str) -> str:
    url = "http://{}:8003/app3".format(APP_3_ALIASES)

    try:
        res = requests.post(url, json={
            "text": text
        })
        print("Success request")
        return res.text
    except Exception as e:
        print("Fail request")
        return "FAIL PERFORM CALL IN APP 2"


@app.post("/app2")
async def gateway(body: Body):
    result = perform_call(body.text)
    return {"message": "Success", "reply_app_2": "Received in app2 => {}".format(result)}
