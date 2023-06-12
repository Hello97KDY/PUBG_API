# from chicken_dinner.pubgapi import PUBG
# from chicken_dinner.models.telemetry.events import PlayerPositionEvent

# from chicken_dinner import API
# import chicken_dinner
# api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628'
# match_id = 'd42a5fed-cfd5-438c-8a73-b84eae9b75e3'
# player_name = "breakthebalance"

# pubg_api = API(api_key)

# def get_player_positions(telemetry, player_name):
#     positions = []

#     for event in telemetry.events:
#         if event['_T'] == 'LogPlayerPosition':
#             player = event['character']
#             location = player['location']
#             name = player['name']
#             if name == player_name:
#                 position = (location['x'], location['y'])
#                 positions.append(position)
#     return positions

# match = pubg_api.match(match_id)
# telemetry = match.get_telemetry()
# positions = get_player_positions(telemetry, player_name)
# print(positions)

import requests
from chicken_dinner.pubgapi import PUBG

# API 키 설정 (https://developer.pubg.com/ 사이트에서 발급받은 API 키를 사용)
api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628"
pubg = PUBG(api_key, "kakao")

# 플레이어 이름에 따른 위치 조회 (예 : player_name = "PLAYER_NAME")
player_name = "breakthebalance"
player = pubg.player(player_name)
recent_match_id = player.match_ids[0]

# 최근 매치 정보와 매치 상세 정보 가져오기
match = pubg.match(recent_match_id)
telemetry = match.get_telemetry()

# 이벤트로부터 플레이어 위치 추출
events = telemetry.events
player_location_events = [event for event in events if event.event_type == "log_player_position"]

# 플레이어 위치 출력
for i, event in enumerate(player_location_events):
    point = event.data["location"]
    print(f"#{i + 1}: {point}")