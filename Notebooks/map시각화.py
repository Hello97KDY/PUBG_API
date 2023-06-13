from chicken_dinner.pubgapi import PUBGCore

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628"
pubgcore = PUBGCore(api_key, "kakao")
shroud = pubgcore.players("player_names", "breakthebalance")
# print(shroud)
"""
{'data': [{'type': 'player', 'id': 'account.204ab94bfaa742da9496a969cf94575d', 'attributes': {'stats': None, 'titleId': 'pubg', 'shardId': 'kakao', 'patchVersion': '', 'banType': 'Innocent', 'clanId': 'clan.bf0067bea89f47ae8d38668112f6edcd', 'name': 'breakthebalance'}, 'relationships': {'assets': {'data': []}, 'matches': {'data': 
[{'type': 'match', 'id': '48991abf-c498-4fa4-aef3-dcb179d1da1e'}, {'type': 'match', 'id': '26e08044-1daa-408a-8ef2-66fa7bf792cd'}, {'type': 'match', 'id': 'f73318aa-70e6-4776-8b76-044f5081743b'}, {'type': 'match', 'id': '604145bb-ea9e-44e6-ba04-f95907a500b2'}, {'type': 'match', 'id': '2b374d8e-d6db-4a75-9586-5b0b5f6ee1ad'}, {'type': 'match', 'id': '5f8fd2fc-1f71-46c3-9970-d2491e57886c'}, {'type': 'match', 'id': 
'd42a5fed-cfd5-438c-8a73-b84eae9b75e3'}, {'type': 'match', 'id': 'a6910131-33af-4181-a8dc-701e3fd4f2f5'}, {'type': 'match', 'id': '21aadfe8-151e-474a-8cc0-837c974ea12f'}, {'type': 'match', 'id': '9a56f037-f349-473d-8e70-dc88617f131f'}, {'type': 'match', 'id': '5da67ae1-0d93-4b6d-a91b-c33c836ab003'}, {'type': 'match', 'id': 'a09c5409-b98e-472c-a2a9-43eded72cd95'}, {'type': 'match', 'id': '8fcd7d54-7f82-4fe6-a9d2-5cf75d75072b'}, {'type': 'match', 'id': '4b878545-930c-4921-b893-c44df763d786'}, {'type': 'match', 'id': '38ab8706-cd24-4eaf-ac66-cc6ef5bf98b5'}, {'type': 'match', 'id': '4c88832b-9982-4316-ba0d-c9cdda6bb727'}, {'type': 'match', 'id': 'b438f062-26cd-44af-b48d-1fa7faf42279'}, {'type': 'match', 'id': '4e6c513f-a97e-4e35-a9f6-f860114c2b87'}, {'type': 'match', 'id': 'c9a49df7-d2d2-454d-92a7-00506673bc34'}, {'type': 
'match', 'id': 'ccee28fc-48e0-4a45-b76e-394c144dfbc5'}, {'type': 'match', 'id': 'b43fdbdc-5c99-45ee-b4e0-d7b62b76f017'}, {'type': 'match', 'id': 'bb0f8191-a13d-464d-b9e7-2651f4bde8ab'}, {'type': 'match', 'id': 'af8b408b-dd5d-4356-9b9d-2dd3364344fb'}, {'type': 'match', 'id': 'e0031fd4-4573-431d-a2e7-98f8ee430486'}, {'type': 'match', 'id': 'd28142c4-dd74-49c9-a868-5ff4f2f41d16'}, {'type': 'match', 'id': 'c6c0affc-fd0c-49a6-8e9a-3745f3a9bacd'}, {'type': 'match', 'id': '77818518-62d3-4b79-bf86-c8384c0d4526'}, {'type': 'match', 'id': '3ed19375-8ae3-4ac6-a40e-be53693ee224'}, {'type': 'match', 'id': 'd6399dc4-6166-4623-b03f-f5dd0f944700'}, {'type': 'match', 'id': '63d6c951-0c64-4b29-8b33-9a70f401c5f4'}, {'type': 'match', 'id': 'c09e53e6-a8cf-4c32-8944-6fde43058952'}, {'type': 'match', 'id': '8d33c63d-b62e-4603-9d5f-99db2515fdc5'}, {'type': 'match', 'id': '5f322f63-e1a5-4ea7-a60b-79dc0761346a'}, {'type': 'match', 'id': '9bfa3145-d953-458d-a3e0-bc1913f9d56d'}, {'type': 'match', 'id': 'c43543ca-cc94-4122-bf28-f14fcac004d7'}, {'type': 'match', 'id': '9dd3320d-66d4-4538-bca7-9d192cad7fae'}, {'type': 'match', 'id': '4dcb9a93-61d8-44be-8b80-337a449dc9fe'}, {'type': 'match', 'id': 'ff2153d3-9a98-45c8-abf3-db0a4d5d6777'}, {'type': 'match', 'id': '0edca4d5-be7c-489d-828b-574b844baf0a'}, {'type': 'match', 'id': '74a4d082-736e-4393-b49a-9f4c377538da'}, {'type': 'match', 'id': '5a36222a-0e73-4946-895b-8da36b9d7d26'}, {'type': 'match', 'id': '60fe38a3-b1f1-42cb-a410-530526878c6e'}, {'type': 'match', 'id': '0820d4e3-d35e-4284-b844-0ac2ef1d7d7c'}, {'type': 'match', 'id': 'f82bacf7-c5a6-4d25-bd0c-6de6fea44b6e'}, {'type': 'match', 'id': 'f2d6906a-d4aa-4a88-8c42-0e97bd7f5b8b'}, {'type': 'match', 'id': 'c0354fbd-16fa-4891-b438-d4085c2712ca'}, {'type': 'match', 'id': '30e2df94-1c6f-40ff-9b00-eefc5571d8f7'}, {'type': 'match', 'id': 'd55f27e4-5025-456b-9de4-6ed0d989aca3'}, {'type': 'match', 'id': '8a715599-9e9a-43da-a38e-d4c0779648df'}, {'type': 'match', 'id': '3df0b78f-a064-47b7-8497-ad383bab66f6'}, {'type': 'match', 'id': '62a2b634-716d-427e-9ce3-4d1d4bdae8fc'}, {'type': 'match', 'id': '2e0e2cfb-3817-4c52-9a39-37b15dbb175f'}, {'type': 'match', 'id': '6f17e1dd-9317-42f7-acd8-b109f0e664ee'}, {'type': 'match', 'id': '6a42b262-85f0-413b-8449-2404f442b42c'}, {'type': 'match', 'id': '1bd655ea-ee60-4a14-a52f-333657e193f9'}, {'type': 'match', 'id': 'deabb670-de36-4fa3-9744-c690b5960147'}, {'type': 'match', 'id': '47014c11-0664-4d6c-8873-5ec38a4e6e02'}, {'type': 'match', 'id': '4f8022ed-81d0-4b54-9b0a-784f965876ff'}, {'type': 'match', 'id': 'efdd99e3-c5ee-4b6d-ae12-e70bcb984165'}]}}, 'links': {'self': 'https://api.pubg.com/shards/kakao/players/account.204ab94bfaa742da9496a969cf94575d', 'schema': ''}}], 'links': {'self': 'https://api.playbattlegrounds.com/shards/kakao/players?filter[playerNames]=breakthebalance'}, 'meta': {}}
"""

from chicken_dinner.pubgapi import PUBG

# api_key = "your_api_key"
pubg = PUBG(api_key, "kakao")
shroud = pubg.players_from_names("breakthebalance")[0]
shroud_season = shroud.get_current_season()
squad_fpp_stats = shroud_season.game_mode_stats('squad')
# print(squad_fpp_stats)
"""
{'squad': {'assists': 2, 'boosts': 9, 'dbnos': 13, 'daily_kills': 0, 'daily_wins': 
0, 'damage_dealt': 1807.647, 'days': 5, 'headshot_kills': 3, 'heals': 8, 'kill_points': 0, 'kills': 16, 'longest_kill': 30.880165, 'longest_time_survived': 797, 'losses': 7, 'max_kill_streaks': 4, 'most_survival_time': 797, 'rank_points': 0, 'rank_points_title': '', 'revives': 0, 'ride_distance': 1366.3369, 'road_kills': 0, 'round_most_kills': 8, 'rounds_played': 7, 'suicides': 0, 'swim_distance': 0, 'team_kills': 2, 'time_survived': 2179, 'top_10s': 0, 'vehicle_destroys': 0, 'walk_distance': 
2256.8335, 'weapons_acquired': 24, 'weekly_kills': 0, 'weekly_wins': 0, 'win_points': 0, 'wins': 0}}
"""

from chicken_dinner.pubgapi import PUBG

import os
import matplotlib

ffmpeg_path = "C:/Users/Admin/Desktop/ffmpeg-6.0-essentials_build/bin/ffmpeg.exe"  # ffmpeg 설치 경로에 따라 경로를 수정하세요.
matplotlib.rcParams['animation.ffmpeg_path'] = ffmpeg_path
# api_key = "your_api_key"
# pubg = PUBG(api_key, "pc-na")

shroud = pubg.players_from_names("breakthebalance")[0]
recent_match_id = shroud.match_ids[1]
recent_match = pubg.match(recent_match_id)
recent_match_telemetry = recent_match.get_telemetry()
recent_match_telemetry.playback_animation("recent_match2.html")


