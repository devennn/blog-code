from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

APP_2_ALIASES = "app2"


class Body(BaseModel):
    text: str


def perform_call(text: str) -> str:
    url = "http://{}:8002/app2".format(APP_2_ALIASES)

    try:
        res = requests.post(url, json={
            "text": text
        })
        print("Success request")
        return res.text
    except Exception as e:
        print("Fail request")
        return "FAIL PERFORM CALL IN APP 1"


@app.post("/app1")
async def gateway(body: Body):
    result = perform_call(body.text)
    return {
        "message": "Success",
        "reply_app_1": "Received in app1 => {}".format(body.text),
        "call_result": result
    }
