
# import requests
# import pandas as pd

# # 함수 정의: API 응답 데이터를 데이터프레임으로 변환
# def get_dataframe(url, header):
#     response = requests.get(url, headers=header)
#     json_data = response.json()
#     return pd.DataFrame(json_data['data'][0]['relationships']['matches']['data'])
# # 함수 정의: 플레이어 PUBG 경기 통계 정보 획득
# def get_statistics(username, url, header):
#     player_df = get_dataframe(url, header)
#     match_url = f'https://api.pubg.com/shards/kakao/matches/{player_df["id"][1]}'
#     match_response = requests.get(match_url, headers=header)
#     match_json = match_response.json()
#     print(match_json)
    #     match_response = requests.get(match_url, headers=header)
    #     match_json = match_response.json()
    
    # for index in range(len(player_df)):
    #     match_url = f'https://api.pubg.com/shards/kakao/matches/{player_df["id"][index]}'
    #     match_response = requests.get(match_url, headers=header)
    #     match_json = match_response.json()
    # # return print(match_json['data']['attributes'])
    #     participant_list, rank_list = [], [] # 참가자 및 순위 리스트 생성
        
    #     print(f"/n/n---------------{username}님의 {index+1}번째 판---------------/n")
        
    #     for entry in match_json['included']:
    #         if entry['type'] == 'participant': # 게임내 데이터를 불러와 리스트안에 dirt형식으로 저장
    #             participant_list.append({'id': entry['id'], **entry['attributes']['stats']})
    #         elif entry['type'] == 'roster':
    #             rank = entry['attributes']['stats']['rank']
    #             data_list = entry['relationships']['participants']['data']
    #             rank_list.extend({'rankx': rank, **data} for data in data_list)
                
    #     # 데이터프레임 생성 및 병합
    #     participant_df = pd.DataFrame(participant_list)
    #     rank_df = pd.DataFrame(rank_list)
    #     game_result_df = pd.merge(left=participant_df, right=rank_df, how='inner', on='id')
        
        # 순위별 팀원 이름 및 통계 출력
        # grouped_df = game_result_df.groupby('rankx')
        # for rank, group in grouped_df:
        #     names = ', '.join(group['name'])
        #     total_kills = group['kills'].sum()
        #     total_assists = group['assists'].sum()
        #     print(f"{rank}등: {names}/n/t총 킬 수: {total_kills}/t총 어시스트 수: {total_assists}")

# 메인: 플레이어 이름 및 API 정보 설정 후 통계 함수 호출
# if __name__ == "__main__":
#     username = 'breakthebalance' #input("user name를 입력하세요: ") #
#     url = f'https://api.pubg.com/shards/kakao/players?filter[playerNames]={username}'
#     header = {
#         "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628",
#         "Accept": "application/vnd.api+json"
#     }
#     # get_dataframe(url, header)
#     get_statistics(username, url, header)
#-----------------------------------------------------------------------------
# import requests

# api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628"
# match_id = 'e51170a3-1f3f-4660-a924-b9f41dae04d5'

# headers = {
#     'Authorization': f'Bearer {api_key}',
#     'Accept': 'application/vnd.api+json'
# }

# # 매치 정보 요청
# url = f'https://api.pubg.com/shards/kakao/matches/{match_id}'
# response = requests.get(url, headers=headers)

# # Telemetry 데이터 URL 추출
# if response.status_code == 200:
#     data = response.json()
#     print(f"data : {data['included']}")
#     for item in data['included']:
#         if item['type'] == 'asset':
#             telemetry_url = item['attributes']['URL']

#             # Telemetry 데이터 요청
#             response = requests.get(telemetry_url)

#             # Telemetry 데이터 처리
#             if response.status_code == 200:
#                 telemetry_data = response.json()
#                 # Telemetry 데이터 활용
#                 # print(f"telemetry_data:{telemetry_data}")
#-----------------------------------------------------------------------------
# import requests

# def get_match_data(api_key: str, match_id: str) -> dict:
#     url = f'https://api.pubg.com/shards/steam/matches/{match_id}'
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Accept": "application/vnd.api+json"
#     }
#     response = requests.get(url, headers=headers)
#     return response.json()

# api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628"
# match_id = 'e51170a3-1f3f-4660-a924-b9f41dae04d5'
# match_data = get_match_data(api_key, match_id)

# def get_telemetry_url(match_data: dict) -> str:
#     assets = [item for item in match_data.get("included", []) if item["type"] == "asset"]
    
#     if assets:
#         asset = assets[0]
#         telemetry_url = asset["attributes"]["URL"]
#         return telemetry_url
#     else:
#         return None

# telemetry_url = get_telemetry_url(match_data)

# def get_telemetry_data(telemetry_url: str) -> list:
#     response = requests.get(telemetry_url)
#     telemetry_data = response.json()
#     return telemetry_data
# telemetry_data = get_telemetry_data(telemetry_url)
#-----------------------------------------------------------------------------


# 항 경기 기준 player별 위치 출력(x,y,z)
import requests
import pandas as pd
def get_match_data(api_key: str, match_id: str) -> dict:
    url = f'https://api.pubg.com/shards/steam/matches/{match_id}'
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/vnd.api+json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_telemetry_url(match_data: dict) -> str:
    for item in match_data.get("included", []):
        if item["type"] == "asset":
            return item["attributes"]["URL"]
    return None

def get_telemetry_data(telemetry_url: str) -> list:
    response = requests.get(telemetry_url)
    return response.json()


api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628"
match_id = 'e51170a3-1f3f-4660-a924-b9f41dae04d5'
match_data = get_match_data(api_key, match_id)
telemetry_url = get_telemetry_url(match_data)
telemetry_data = get_telemetry_data(telemetry_url)

# def get_player_positions(telemetry_data: list) -> list:
#     player_positions = []
#     for event in telemetry_data:
#         if event["_T"] == "LogPlayerPosition":
#             position_data = {
#                 "timestamp": event["_D"],
#                 "player_name": event["character"]["name"],
#                 "location_x": event["character"]["location"]["x"],
#                 "location_y": event["character"]["location"]["y"],
#                 "location_z": event["character"]["location"]["z"],
#             }
#             player_positions.append(position_data)
#     player_positions_df = pd.DataFrame(player_positions)
#     player_positions_player_sort = player_positions_df.sort_values(by = 'player_name')
#     name_mask = player_positions_player_sort['player_name'] == 'breakthebalance'
#     mask_player_positions_player_sort = player_positions_player_sort[name_mask]
#     return mask_player_positions_player_sort

# player_positions = get_player_positions(telemetry_data)
# #----------------------------------------------------------------------
def get_player_positions(telemetry_data: list) -> list:
    positions = []

    for event in telemetry_data:
        if event["_T"] in ("LogPlayerPosition", "LogParachuteLanding"):
            if event["character"]["name"] == 'breakthebalance':
                positions.append({
                    "player_name": event["character"]["name"],
                    "location_x": event["character"]["location"]["x"],
                    "location_y": event["character"]["location"]["y"],
                    "location_z": event["character"]["location"]["z"]
                })

    return positions

positions = get_player_positions(telemetry_data)

import cv2
import matplotlib.pyplot as plt

def draw_positions_on_map(map_image_path, positions, scale_factor=0.005):
    # 맵 이미지 불러오기
    map_image = cv2.imread(map_image_path)

    # 위치 데이터를 이미지 좌표로 변환하고 맵 위에 그리기
    for position in positions:
        x = int(position["location_x"] * scale_factor)
        y = int(position["location_y"] * scale_factor)
        print(f'x:{x}\ty:{y}')
        cv2.circle(map_image, (x, y), 5, (0, 255, 0), -1)
   
    # 맵 이미지와 위치 표시 출력
    plt.figure(figsize=(16, 16))
    plt.imshow(cv2.cvtColor(map_image, cv2.COLOR_BGR2RGB))
    plt.show()


def draw_positions_on_map1(map_image_path, positions, scale_factor=0.001):
    # 맵 이미지 불러오기
    map_image = cv2.imread(map_image_path)

    # 위치 데이터를 이미지 좌표로 변환하고 맵 위에 그리기
    for index in range(len(positions)-1):    
        x = int(positions[index]["location_x"] * scale_factor)
        y = int(positions[index]["location_y"] * scale_factor)
        
        x1 = int(positions[index+1]["location_x"] * scale_factor)
        y1 = int(positions[index+1]["location_y"] * scale_factor)
        
        cv2.line(map_image, (x, y), (x1,y1), (255, 0, 0),5)
        # cv2.line(map_image, (250, 690), (400,300), (255, 0,0 ),5)
    plt.figure(figsize=(4, 4))
    plt.imshow(cv2.cvtColor(map_image, cv2.COLOR_BGR2RGB))
    plt.show()
    
        # print(f'x:{x}\ty:{y}\tx1:{x1}\ty1:{y1}')
    return 0

map_image_path = "C:/Users/Admin/Desktop/pubg_map.jpg"  # 배틀그라운드 맵 이미지의 경로를 지정합니다.
draw_positions_on_map1(map_image_path, positions)

# print(positions)



'''
매치 id하나와 닉네임을 지정하고 매치 id에 해당하는 breakthebalance

'''































