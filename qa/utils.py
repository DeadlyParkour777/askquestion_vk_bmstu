from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import jwt
import time
import requests
import json
from django.conf import settings

def paginate(objects_list, request, per_page):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj

def get_centrifugo_token(user_id):
    claims = {"sub": str(user_id), "exp": int(time.time()) + 24 * 3600}
    return jwt.encode(claims, settings.CENTRIFUGO_HMAC_SECRET, algorithm="HS256")

def publish_to_centrifugo(channel, data):
    headers = {
        'Authorization': f'apikey {settings.CENTRIFUGO_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "method": "publish",
        "params": {
            "channel": channel,
            "data": data
        }
    }
    try:
        requests.post(settings.CENTRIFUGO_API_URL, data=json.dumps(payload), headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"Centrifugo error: {e}")
