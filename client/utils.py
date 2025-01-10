import openai
import requests
from config import settings


def send_api(data, path):
    url = settings.API_HOST + f"/{path}"
    headers = {"Content-Type": "application/json", "accept": "application/json"}

    try:
        # response = requests.post(url, headers=headers, json=data)
        # return response.json()
        return requests.post(url, headers=headers, json=data, stream=True)

    except Exception as e:
        return {"generated_text": e}


def check_api_key(api_key):
    # api key 맞는지 확인
    try:
        # TODO: The resource 'Engine' has been deprecated
        # openai.Engine.list()
        return True
    except openai.AuthenticationError:
        return False
