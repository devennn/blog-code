from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Body(BaseModel):
    text: str


@app.post("/app3")
async def gateway(body: Body):
    return {"message": "Success", "reply_app_3": "Behold app3 => {}".format(body.text)}
