import requests
import pandas as pd
import cv2
import matplotlib.pyplot as plt


def get_img(username, api_key, header):
    url = f'https://api.pubg.com/shards/kakao/players?filter[playerNames]={username}'
    response = requests.get(url, headers=header)
    json_data = response.json()
    player_match_ids_df = pd.DataFrame(json_data['data'][0]['relationships']['matches']['data'])

    url_list = []

    for index in range(len(player_match_ids_df)):
        match_url = f'https://api.pubg.com/shards/kakao/matches/{player_match_ids_df["id"][index]}'
        match_response = requests.get(match_url, headers=header)
        match = match_response.json()

        for item in range(len(match['included'])):
            if match['included'][item]['type'] == "asset":
                url_list.append(match['included'][item]['attributes']['URL'])

    positions = []

    for index in range(len(url_list)):#range(3):
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


if __name__ == "__main__":
    username = 'breakthebalance'# input("user name를 입력하세요: ") #'breakthebalance'
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628"
    header = {
        "Authorization": api_key,
        "Accept": "application/vnd.api+json"
    }

    get_img(username, api_key, header)