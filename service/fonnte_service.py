# service/fonnte_service.py

import requests
from config import FONNTE_TOKEN

def send_whatsapp(target, message):
    url = "https://api.fonnte.com/send"
    payload = {"target": target, "message": message}
    headers = {"Authorization": FONNTE_TOKEN}
    requests.post(url, data=payload, headers=headers)
