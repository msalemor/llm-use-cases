import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
endpoint = os.getenv("OPENAI_ENDPOINT")
model = os.getenv("OPENAI_MODEL")

client = AzureOpenAI(api_key=api_key,
                     azure_endpoint=endpoint,
                     api_version="2024-02-15-preview")


def determine_intent(intent_statement: str):
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),  # model = "deployment_name".
        messages=[
            {"role": "system", "content": "You are a helpful assistant that can perform determine intent from the following list of intents:\n- WeatherIntent: A user asks a question about the weather.\n- ItineraryIntent: A user asks a question about a travel itinerary.\n- ReservationIntent: A user asks a question about making a reservation.\n- OtherIntent: User asks a question about anything else.\n\nNo prologue. Respond in the following JSON format:\n{\"intent\": }."},
            {"role": "user", "content": intent_statement}
        ],
        temperature=0.1,
    )
    json_respond = response.choices[0].message.content
    analysis = json.loads(json_respond)
    return f"Q: {intent_statement} A: {analysis['intent']}"


def get_sentiment():
    print(determine_intent("What is the weather like in Seattle?"))
    print(determine_intent("What is my next trip?"))
    print(determine_intent("Make a travel reservation?"))
    print(determine_intent("What is the speed of light?"))


if __name__ == "__main__":
    get_sentiment()
