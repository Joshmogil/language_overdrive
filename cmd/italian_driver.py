from google.cloud import translate
import os
import openai
import random

from dotenv import load_dotenv

load_dotenv("./.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set the path to the service account in gcp with api usage permission for Cloud Translate
path_to_gcp_service_account = "/home/jmogil/gcp_service_accounts/language-overdrive-4fde6440ef31.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= path_to_gcp_service_account

# Initialize Translation client
def translate_text(text: str = "YOUR_TEXT_TO_TRANSLATE", srcl: str = "en-US" , tgl: str = "it", project_id: str = "language-overdrive"):
    """Translating Text."""

    client = translate.TranslationServiceClient()

    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    # Translate text from English to French
    # Detail on supported types can be found here:
    # https://cloud.google.com/translate/docs/supported-formats

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": srcl,
            "target_language_code": tgl,
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        return(translation.translated_text)

def chatgpt(text, previous_text,level="beg"):
    
    levels={
        "beg": "in the style of a 8 year old.",
        "int": "in the style of a 14 year old.",
        "adv" : "."
    }
    tone, max_tokens = max_tokens_based_on_input(text)
    
    prompt=f"""Respond in a {tone} way to: {text}. End each sentence with punctuation."""
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


def respond_to_message(message_text: str) -> str:
    italian_response = chatgpt(message_text)
    in_english = translate_text(italian_response,srcl="it", tgl="en-US")
    print(italian_response)
    print(in_english)
    

