import requests
import openai

from config import settings

def send_api(data, path) :
    url = settings.API_HOST + f"/{path}"
    headers = {
        "Content-Type" :  "application/json", 
        "accept" : "application/json"
    }
    
    try :
        #response = requests.post(url, headers=headers, json=data)
        #return response.json()
        return requests.post(url, headers=headers, json=data, stream=True)

    except Exception as e :
        return {"generated_text" : e}

def check_apiKey(api_key) :
    openai.api_key = api_key

    # api key 맞는지 확인
    try :
        openai.Engine.list()
        return True
    except openai.error.AuthenticationError :
        return False