import os
import openai
import random
from typing import Any
import json
#from dotenv import load_dotenv

# Set the path to the service account in gcp with api usage permission for Cloud Translate


#load_dotenv("./.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

def chatgpt(text, language):
    tone, max_tokens = max_tokens_based_on_input(text)
    
    prompt=f"""In {language}, respond in a {tone} way to: {text}. End each sentence with punctuation."""
    #print(prompt)

    
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    temperature=1,
    max_tokens=max_tokens,
    top_p=1,
    frequency_penalty=2,
    presence_penalty=2
    )
    #print(response)
    r = response["choices"][0]["text"].replace("\n","").replace("?","")
    #print(r)
    return r

def max_tokens_based_on_input(text):
    #base line: shorter input = shorter response, vice versa
    max_length = len(text)*5.5 if len(text) <20 else 125
    min_length = len(text)*1.5 if len(text) <20 else 40


    #if the text is questionish then give longer responses.
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Describe the the tone of the following sentence using one or more adjectives: {text}",
    temperature=1,
    max_tokens=40,
    top_p=1,
    frequency_penalty=2,
    presence_penalty=2
    )
    r = response["choices"][0]["text"].replace("\n","").replace("?","").lower()
    #print(r)
    #experimenting with something here don't look
    if "curious" in r or \
    "inquisitive" in r:
        max_length = max_length*3.5
        min_length = min_length*3

    max_tokens=random.randrange(int(min_length),int(max_length))
    tone = r
    return tone, max_tokens


def respond_to_message(request: dict | Any) -> str:
    print(type(request))
    
    
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        print("Answered preflight request!")

        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request=request.get_json()
    response = chatgpt(request["message"], request["language"])
    return (json.dumps({"response":response}),200,headers)


if __name__ == "__main__":
    respond_to_message(
        {
            "message":"hello!",
            "language":"German"
        }
    )