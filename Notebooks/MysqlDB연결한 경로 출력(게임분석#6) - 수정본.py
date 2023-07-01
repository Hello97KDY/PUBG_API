import cv2
import matplotlib.pyplot as plt
import pandas as pd
import requests
from sqlalchemy import create_engine


def get_player_data(username, api_key):
    header = {
        "Authorization": api_key,
        "Accept": "application/vnd.api+json"
    }

    url = f'https://api.pubg.com/shards/kakao/players?filter[playerNames]={username}'
    response = requests.get(url, headers=header)
    player_json_data = response.json()

    df = pd.DataFrame(player_json_data['data'][0]['relationships']['matches']['data'])
    df['user_name'] = username

    return df


def save_data_to_database(df, host, user_name, password, db):
    database_connection = create_engine(f'mysql+pymysql://{user_name}:{password}@{host}/{db}')
    df.to_sql('pubg_db_test', con=database_connection, if_exists='append', index=False)


def get_player_match_ids(username, host, user_name, password, db):
    # database_connection = pymysql.connect(host=host, port=3306, user=user_name, passwd=password, db=db, charset='utf8')
    database_connection = create_engine(f'mysql+pymysql://{user_name}:{password}@{host}/{db}')
    sql = f"SELECT DISTINCT id, user_name FROM pubg_db_test where user_name = '{username}'"
    player_match_ids_df = pd.read_sql(sql, con=database_connection)

    return player_match_ids_df


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

        for item in range(len(match['included'])):
            if match['included'][item]['type'] == "asset":
                url_list.append(match['included'][item]['attributes']['URL'])

    return url_list


def get_positions_draw(username, url_list):
    
    positions = []

    for index in range(3):#range(len(url_list)):
        sub_positions = []
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
                plt_map_name = map_dict.get(map_name).split("_")[0]
                
                map_image_path += map_dict.get(map_name, map_name)

            if event["_T"] in ("LogPlayerPosition", "LogParachuteLanding"):
                if event["character"]["name"] == username:
                    sub_positions.append({
                        "player_name": event["character"]["name"],
                        "location_x": event["character"]["location"]["x"],
                        "location_y": event["character"]["location"]["y"],
                    })

        positions.append(sub_positions)
        scale_factor = 0.01        

        for position in positions:
            map_image = cv2.imread(map_image_path)
            for index in range(len(position) - 1):
                x = int(position[index]["location_x"] * scale_factor)
                y = int(position[index]["location_y"] * scale_factor)
                x1 = int(position[index + 1]["location_x"] * scale_factor)
                y1 = int(position[index + 1]["location_y"] * scale_factor)

                cv2.line(map_image, (x, y), (x1, y1), (255, 0, 0), 50)

        plt.figure(figsize=(8, 8))
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