from pymongo import MongoClient
import requests
import pandas as pd
import cv2
import matplotlib.pyplot as plt

def insert_player_data(db, header, user_name):
    url = f'https://api.pubg.com/shards/kakao/players?filter[playerNames]={user_name}'
    response = requests.get(url, headers=header)
    player_json_data = response.json()
    db.player_json.insert_one(player_json_data)

def get_player_data(db):
    return db['player_json'].find()

def get_player_match_ids(player_data):
    for index in player_data:
        return pd.DataFrame(index['data'][0]['relationships']['matches']['data'])

def get_match_urls(player_match_ids_df, header):
    url_list = []
    for index in range(len(player_match_ids_df)):
            match_url = f'https://api.pubg.com/shards/kakao/matches/{player_match_ids_df["id"][index]}'
            match_response = requests.get(match_url, headers=header)
            match = match_response.json()

            for item in range(len(match['included'])):
                if match['included'][item]['type'] == "asset":
                    url_list.append(match['included'][item]['attributes']['URL'])
    return url_list

def get_positions(url_list, username):
    positions = []

    for index in range(3):  # range(len(url_list)):
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
                    "Desert_Main": "Deston_Main_High_Res.png",
                    "Range_Main": "Camp_Jackal_Main_High_Res.png",
                    "Savage_Main": "Sanhok_Main_High_Res.png",
                    "Summerland_Main": "Karakin_Main_High_Res.png",
                    "Tiger_Main": "Taego_Main_High_Res.png"
                }
                map_image_path += map_dict.get(map_name, map_name)
                plt_map_name = map_dict.get(map_name).split("_")[0]

            if event["_T"] in ("LogPlayerPosition", "LogParachuteLanding"):
                if event["character"]["name"] == username:
                    sub_positions.append({
                        "player_name": event["character"]["name"],
                        "location_x": event["character"]["location"]["x"],
                        "location_y": event["character"]["location"]["y"],
                    })

        positions.append(sub_positions)
    return positions, plt_map_name, map_image_path

def visualize_positions(positions, plt_map_name, map_image_path):
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

client = MongoClient("mongodb://localhost:27017/")
db = client['pubg_test']
username = 'zpdldptmxlsw'
api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628"
header = {
    "Authorization": api_key,
    "Accept": "application/vnd.api+json"
}

insert_player_data(db, header, username)
player_data = get_player_data(db)
player_match_ids_df = get_player_match_ids(player_data)
url_list = get_match_urls(player_match_ids_df, header)
positions, plt_map_name, map_image_path = get_positions(url_list, username)
visualize_positions(positions, plt_map_name, map_image_path)


# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")

# db = client['pubg_test'] # pubg_test라는 이름의 데이터베이스에 접속

# print(client.list_database_names())

# dpInsert = db.posts.insert_one()