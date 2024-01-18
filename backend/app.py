from datetime import datetime

import requests

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



templates = Jinja2Templates(directory="templates/")

app = FastAPI()

rori_base_url = "https://rori-answers-api-iadgvfgdkq-ew.a.run.app/v2/nlu"

dbStore = [
    {
        "id": 1,
        "question": "What is 4 * 5?",
        "expected_answer": "20"
     },
    {
        "id": 2,
        "question": "What do I get if I add 99 to 2?",
        "expected_answer": "101"
    },
    {
        "id": 3,
        "question": "I have four apples, I get another eight from my father, but I share the apples equally with my friend. How many apples do I have?",
        "expected_answer": "6"
    },
    {
        "id": 4,
        "question": "If I count up from 997 as follows, what is the next number? 997, 998, 999, ...",
        "expected_answer": "1000"
    },
    {
        "id": 5,
        "question": "How mmuch is 2 to the power 3 or 2^3?",
        "expected_answer": "8"
    },
]
# call to
@app.get("/form/{questionId}", response_class=HTMLResponse)
def root(request: Request, questionId: int = 1):
    result = "Answer the Question"
    return templates.TemplateResponse('form.html', context={'request': request, 'question':dbStore[questionId].question,'result': result})



@app.post("/form", response_class=HTMLResponse)
def form_post(request: Request, num: int = Form(...)):
    result = rori_math_call(num)# response from rori apivfgn
    return templates.TemplateResponse('frontend/question.html', context={'request': request, 'result': result})


# rori api call function
def rori_math_call(question, expected_answer, user_answer):
    payload =  {
        "message_data": {
        "author_id":"27833335555",
        "author_type": "OWNER",
        "contact_uuid": "e331dc93-1b9a-4db4-ad58-315d1c95f243",
        "message_direction": "inbound", 
        "message_id": "ABGGJ4MzZWFfAgs-sCaxu0X72jwgbg",
        "message_body": user_answer,
        "question": question,
        "expected_answer": expected_answer,
        "message_inserted_at": datetime.now(),
        "message_updated_at": datetime.now()
        }
    }

    rori_response = requests.get(rori_base_url).json()

    # check rori response params
    # if correct, wrong or otherwise
    rori_response_parsed = rori_response
    return rori_response_parsed