"""
#참고 : https://developers.kakao.com/docs/latest/ko/message/rest-api#send-friend

curl -v -X POST "https://kapi.kakao.com/v1/api/talk/friends/message/default/send" \
    -H "Authorization: Bearer {USER_ACCESS_TOKEN}" \
    -d 'receiver_uuids=["abcdefg0001"]' \
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

import os
import json
import requests

def sendToFriendsMessage(friends_id, text):

    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"  # 친구에게 보내기 주소

    uuidsData = {"receiver_uuids": json.dumps(friends_id)}

    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }

    data = {'template_object': json.dumps(post)}

    print("BEFER")
    print(uuidsData)
 #   print(json.dumps(f_data))
  #  f_data = json.dumps(f_data)
    #data.update(f_data)
    uuidsData.update(data)
    print("AFTER")
    print(uuidsData)
    return requests.post(url, headers=header, data=uuidsData)

def getFriendsList():
    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 정보 요청

    result = json.loads(requests.get(url, headers=header).text)

    print(result)
    friends_list = result.get("elements")
    friends_id_infunction = []

    for friend in friends_list:
        friends_id_infunction.append(friend.get("uuid"))

    return friends_id_infunction

text = "Hello, This is KaKao Message Test!!("+os.path.basename(__file__).replace(".py", ")")

KAKAO_TOKEN = "inS136pP32rp6oSv6PxEPurnCZ2LlpYbFRlWogo9cxgAAAF1KOGJnQ" #1004gmyoul

friends_id = getFriendsList()

print(sendToFriendsMessage(friends_id, text).text)
