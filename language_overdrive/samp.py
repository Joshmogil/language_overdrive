from google.cloud import translate
import os

path_to_gcp_service_account = "/home/jmogil/gcp_service_accounts/language-overdrive-4fde6440ef31.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= path_to_gcp_service_account

# Initialize Translation client
def translate_text(text: str = "YOUR_TEXT_TO_TRANSLATE", target_language: str = "it", project_id: str = "language-overdrive"):
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
            "source_language_code": "en-US",
            "target_language_code": "fr",
        }
    )

    # Display the translation for each input text provided
    for translation in response.translations:
        print("Translated text: {}".format(translation.translated_text))

translate_text("Hello!")