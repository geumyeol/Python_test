import os
import json
import requests

"""
#참고 : https://developers.kakao.com/docs/latest/ko/kakaotalk-social/rest-api#get-friends

curl -v -X GET "https://kapi.kakao.com/v1/api/talk/friends?limit=3" \
    -H "Authorization: Bearer {USER_ACCESS_TOKEN}"
"""
def getFriendsList():
    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v1/api/talk/friends" #친구 정보 요청

    result = json.loads(requests.get(url, headers=header).text)

    friends_list = result.get("elements")
    friends_id = []

    print(friends_list)
    for friend in friends_list:
        friends_id.append(str(friend.get("uuid")))

    return friends_id

KAKAO_TOKEN = "TFS_TBzR5-mX_1-4hQnF0d86AF5v67qAw7UkWgorDR4AAAF1EG9_sQ"  #1004gmyoul


print(getFriendsList())