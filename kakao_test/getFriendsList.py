

"""
#참고 : https://developers.kakao.com/docs/latest/ko/kakaotalk-social/rest-api#get-friends

curl -v -X GET "https://kapi.kakao.com/v1/api/talk/friends?limit=3" \
    -H "Authorization: Bearer {USER_ACCESS_TOKEN}"
"""

import json
import requests

def getFriendsList():
    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 정보 요청

    result = json.loads(requests.get(url, headers=header).text)

    friends_list = result.get("elements")
    friends_id = []

    print(requests.get(url, headers=header).text)
    print(friends_list)
    for friend in friends_list:
        friends_id.append(str(friend.get("uuid")))

    return friends_id

KAKAO_TOKEN = "uj9WrKnmLkiP--6ZjvJWug0Pz5RoGNdEI1A5Lgo9cpcAAAF1I6l2ew"  #1004gmyoul


print(getFriendsList())