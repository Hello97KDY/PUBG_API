import cv2
import matplotlib.pyplot as plt
import pandas as pd
import requests
from sqlalchemy import create_engine

# players api를 player name으로 가져와 한 경기에 해당하는 정보들 추출하는 함수
def get_player_data(username, api_key):
    header = {
        "Authorization": api_key,
        "Accept": "application/vnd.api+json"
    }

    url = f'https://api.pubg.com/shards/kakao/players?filter[playerNames]={username}'
    response = requests.get(url, headers=header)
    player_json_data = response.json()

    # matche_ids를 추출하고 검색한 user_name으로 새로운 열을 만들어 dataframe에 저장하고 반환하는 함수
    user_matches_ids_df = pd.DataFrame(player_json_data['data'][0]['relationships']['matches']['data'])
    user_matches_ids_df['user_name'] = username

    return user_matches_ids_df

# 불러온 player_match_ids데이터로 만든 데이터 프레임을 MySQL DB에 저장하는 함수
def save_data_to_database(df, host, user_name, password, db):
    database_connection = create_engine(f'mysql+pymysql://{user_name}:{password}@{host}/{db}')
    df.to_sql('pubg_db_test', con=database_connection, if_exists='append', index=False)

# DB에서 검색한 username에 해당하는 데이터(players_matche_ids)를 가져오는 함수
def get_player_match_ids(username, host, user_name, password, db):
    database_connection = create_engine(f'mysql+pymysql://{user_name}:{password}@{host}/{db}')
    sql = f"SELECT DISTINCT id, user_name FROM pubg_db_test where user_name = '{username}'"
    player_match_ids_df = pd.read_sql(sql, con=database_connection)

    return player_match_ids_df

# players_id 정보를 통해 matches정보를 불러온 후 matches안에 있는 url 정보를 추출하고 반환하는 함수
# url정보를 통해 telemetries api를 불러올수 있다
def get_match_telemetries(player_match_ids_df, api_key):
    header = {
        "Authorization": api_key,
        "Accept": "application/vnd.api+json"
    }

    url_list = []

    for index in range(len(player_match_ids_df)):
        match_url = f'https://api.pubg.com/shards/kakao/matches/{player_match_ids_df["id"][index]}'
        match_response = requests.get(match_url, headers=header)
        match = match_response.json()
        # url하나의 정보는 한경기에 해당하는 정보이기 때문에 전 경기를 불러오기 위해선 
        # 불러온 경기 수 만큼 url이 필요하기 때문에 경기 수 만큼 존재하는 url을 url_list에 담아준다
        print(match)
    #     for item in range(len(match['included'])):
    #         if match['included'][item]['type'] == "asset":
    #             url_list.append(match['included'][item]['attributes']['URL'])

    # return url_list

# telemetries api를 불러온 후 telemetries api가 가지고 있는 player의 이동경로 좌표 및 자기장의 중심 좌표,
# 반지름의 크기 좌표등을 활용해 맵 위에 선을 그리는 함수
# 한경기 마다 하나의 그림을 출력한다.
def get_positions_draw(username, url_list):
    # range(len(url_list))을 하게 되면 불러온 모든 경기를 출력하게 된다. 현재는 test로 3경기만 불러온다
    for index in range(5):#range(len(url_list)):
        sub_positions = []
        map_sub_positions = []
        safety_Zone_Radius_list = []
        response = requests.get(url_list[index])
        telemetry_json = response.json()
        map_image_path = "C:/Users/Admin/Desktop/pubg_maps/"

        for event in telemetry_json:
            if event["_T"] == "LogMatchStart":
                map_name = event["mapName"]
                map_dict = {
                    "Baltic_Main": "Erangel_Main_High_Res.png",
                    "Erangel_Main": "Erangel_Main_High_Res.png",
                    "Chimera_Main": "Paramo_Main_High_Res.png",
                    "DihorOtok_Main": "Vikendi_Main_High_Res.png",
                    "Heaven_Main": "Haven_Main_High_Res.png",
                    "Kiki_Main": "Deston_Main_High_Res.png", 
                    # Desert_Main에 맞는 맵 이미지가 뭔지 모름(공식 문서에 안 나옴)
                    # 임시로 Kiki_Main과 같은 맵 이미지를 넣어둠(지도 이동 경로상 유력)
                    "Desert_Main": "Deston_Main_High_Res.png",
                    "Range_Main": "Camp_Jackal_Main_High_Res.png",
                    "Savage_Main": "Sanhok_Main_High_Res.png",
                    "Summerland_Main": "Karakin_Main_High_Res.png",
                    "Tiger_Main": "Taego_Main_High_Res.png"
                }
                # map의 이름을 제목으로 사용하기 위해 첫번째 _ 뒤로 제거하는 코드
                plt_map_name = map_dict.get(map_name).split("_")[0]
                
                # map이미지 경로를 추출하는 코드
                map_image_path += map_dict.get(map_name, map_name)
            
            # 낙하경로를 추출하기 위해 작성한 코드
            # 라인을 그릴때 매개변수 로 활용된다
            if event["_T"] in ("LogPlayerPosition", "LogParachuteLanding"):
                if event["character"]["name"] == username:
                        if event['common']['isGame'] > 0 and  event['common']['isGame'] <0.11:
                            sub_positions.append({
                                "player_name": event["character"]["name"],
                                "location_x": event["character"]["location"]["x"],
                                "location_y": event["character"]["location"]["y"],
                            })
                                
            # 지상 이동 경로 추출
            if event["_T"] in ("LogPlayerPosition", "LogParachuteLanding"):
                if event["character"]["name"] == username:
                        if event['common']['isGame'] > 0.2:
                                map_sub_positions.append({
                                    "player_name": event["character"]["name"],
                                    "map_location_x": event["character"]["location"]["x"],
                                    "map_location_y": event["character"]["location"]["y"],
                                })
                                
            # 자기장 원을 추출하기 위해 작성한 코드
            # 자기장 원을 그릴때 매개변수 로 활용된다
            if event["_T"] == 'LogGameStatePeriodic':
                if type(event['common']['isGame']) == int:
                    safety_Zone_Radius_list.append({
                        'safetyZoneRadius' : event['gameState']['safetyZoneRadius'],
                        'location_x' : event['gameState']['safetyZonePosition']['x'],
                        'location_y' : event['gameState']['safetyZonePosition']['y'],
                        'isgame' : event['common']['isGame']})
        
        # 맵과 비율을 맞추기 위해 곱할 수
        scale_factor = 0.01

        # 반지름의 크기 정보의 중복을 제거하는 코드
        converted_list = [tuple(item.items()) for item in safety_Zone_Radius_list]
        unique_list = list(set(converted_list))
        unique_list_of_dicts = [dict(item) for item in unique_list]
        unique_list_of_dicts = sorted(unique_list_of_dicts, key=lambda item: item["safetyZoneRadius"],reverse=True)
        
        # 이미디가 있는 경로를 통해 이미지를 가져오는 코드
        map_image = cv2.imread(map_image_path)

        # 자기장을 그리는 코드
        for Radius_lists in unique_list_of_dicts:
            x = Radius_lists['location_x'] * scale_factor
            y = Radius_lists['location_y'] * scale_factor
            radius = Radius_lists['safetyZoneRadius'] * scale_factor
            
            cv2.circle(map_image, (int(x), int(y)), int(radius), (255, 255, 255), 50)

        # 이동경로를 그리는 코드
        for position_index in range(len(sub_positions) - 1):
            # 비행기 경로 추출
            lin_function_x1 = int(sub_positions[0]["location_x"] * scale_factor)
            lin_function_y1 = int(sub_positions[0]["location_y"] * scale_factor)
            lin_function_x2 = int(sub_positions[1]["location_x"] * scale_factor)
            lin_function_y2 = int(sub_positions[1]["location_y"] * scale_factor)
            # 낙하산 경로 추출
            x = int(sub_positions[position_index]["location_x"] * scale_factor)
            y = int(sub_positions[position_index]["location_y"] * scale_factor)
            x1 = int(sub_positions[position_index + 1]["location_x"] * scale_factor)
            y1 = int(sub_positions[position_index + 1]["location_y"] * scale_factor)
            
            cv2.line(map_image, (x, y), (x1, y1), (0, 125, 250), 20) # 낙하산 경로
            
            
        for map_position_index in range(len(map_sub_positions) -1):
            # 지상 이동경로 추출
            map_x = int(map_sub_positions[map_position_index]["map_location_x"] * scale_factor)
            map_y = int(map_sub_positions[map_position_index]["map_location_y"] * scale_factor)
            map_x1 = int(map_sub_positions[map_position_index + 1]["map_location_x"] * scale_factor)
            map_y1 = int(map_sub_positions[map_position_index + 1]["map_location_y"] * scale_factor)
            
            cv2.line(map_image, (map_x, map_y), (map_x1, map_y1), (175, 175, 0), 50) # 지상 이동경로
        
        a = (lin_function_y2 - lin_function_y1) / (lin_function_x2 - lin_function_x1) # 기울기
        b = (lin_function_x2*lin_function_y1 - lin_function_x1*lin_function_y2) / (lin_function_x2 - lin_function_x1) # 상수
        
        cv2.line(map_image, (0,int(b)), (int(map_image.shape[1]), int(a*map_image.shape[1] + b)), (0, 0, 250), 80,cv2.LINE_4) # 비행기 결로

        plt.figure(figsize=(9, 9))
        plt.title(plt_map_name)
        plt.imshow(cv2.cvtColor(map_image, cv2.COLOR_BGR2RGB))
        plt.show()


def main():
    username = 'breakthebalance'
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628"
    host = 'localhost'
    user_name = 'root'
    password = 'wkarma135'
    db = 'test_db'

    player_data = get_player_data(username, api_key)
    save_data_to_database(player_data, host, user_name, password, db)
    player_match_ids = get_player_match_ids(username, host, user_name, password, db)
    match_telemetries = get_match_telemetries(player_match_ids, api_key)
    get_positions_draw(username, match_telemetries)


if __name__ == "__main__":
    main() 