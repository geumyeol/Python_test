import os
import json
import requests

"""
#참고 : https://developers.kakao.com/docs/latest/ko/message/rest-api#send-me

curl -v -X POST "https://kapi.kakao.com/v2/api/talk/memo/default/send" \
    -H "Authorization: Bearer {USER_ACCESS_TOKEN}" \
    -d 'template_object={
        "object_type": "text",
        "text": "텍스트 영역입니다. 최대 200자 표시 가능합니다.",
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }'
"""

def sendToMeMessage(text):
    header = {"Authorization": 'Bearer' + KAKAO_TOKEN}

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send" #나에게 보내기 주소 gmyoul

    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }
    data = {"template_object": json.dumps(post)}
    return requests.post(url, headers=header, data=data)

text = "Hello, This is KaKao Message Test!!("+os.path.basename(__file__).replace(".py", ")")

KAKAO_TOKEN = "int0LEUbiFWU_neJfU0OTdD5g0PpsIHvTD6I9QorDR8AAAF1EpB9Uw" #1004gmyoul
#KAKAO_TOKEN = "HEkt3Zr2TplcuBrqhG013KEPJw52UwXIBQFcAgo9dRkAAAF1EOyVfg" #miran87

#KAKAO_TOKEN = "vq2amtkTHqbJD17yprktUMGiDxdSEe44Z2FAo9dZoAAAF1Em2ePQ" #developer APP

print(len(KAKAO_TOKEN))

print(sendToMeMessage(text).text)
