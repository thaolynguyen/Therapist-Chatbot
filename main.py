import openai
import os
from google.protobuf.json_format import MessageToJson
from flask import Flask, request, make_response
import dialogflow_v2 as dialogflow
from dialogflow_v2.types import QueryResult
import json

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])

def webhook():
    req = request.get_json(silent=True, force=True)
    query_result = QueryResult.from_json(json.dumps(req['queryResult']))
    fulfillment_text = process_dialogflow_response(query_result)
    res = {'fulfillmentText': fulfillment_text}
    return make_response(json.dumps(res))

def process_dialogflow_response(query_result):
    question = query_result.query_text
    answer = generate_answer(question)
    return answer

def generate_answer(question):
    openai.api_key = "YOUR_OPENAI_API_KEY"
    prompt = f"Question: {question}\nAnswer:"
    response = openai.Completion.create(
        model="davinci:ft-personal-2023-02-24-13-50-55",
        prompt="This is a discussion between a therapist and a patient",
        temperature=0.7,
        max_tokens=1024,
        n = 1,
        stop=None,
        timeout=15,
        frequency_penalty=0,
        presence_penalty=0
    )
    answer = response.choices[0].text.strip()
    return answer
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
