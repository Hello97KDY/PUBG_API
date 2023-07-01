import requests
import pandas as pd
from collections import Counter

# player의 게임당 id를 api에서 받아와 Dataframe으로 만드는 함수
def get_stats_dataframe(url, header): 
    r = requests.get(url, headers=header)
    match_data_json = r.json()
    match_data_df = pd.DataFrame(match_data_json['data'][0]['relationships']['matches']['data'])
    return match_data_df

# 게임 모드 리스트와 player의 게임 플레이 데이터를 각각 list와 Datafreame으로 만드는 함수
def get_user_stats(user_name, url, header):
    # API를 통해 플레이어의 게임당 통계 데이터 가져오기
    player_data_df = get_stats_dataframe(url, header)

    ilist, id_list, game_modes = [], [], []

    # 각 경기의 통계 데이터를 가져와 리스트에 추가
    for i in range(len(player_data_df)):
        match_url = f'https://api.pubg.com/shards/kakao/matches/{player_data_df["id"][i]}'
        match_r = requests.get(match_url, headers=header)
        match_data = match_r.json()

        # 경기 모드 추가
        game_modes.append(match_data['data']['attributes']['gameMode'])

        for entry in match_data['included']:
            # 'participant' 타입이면 'id' 정보를 아이템에 담아 'ilist' 리스트에 추가합니다.
            if entry['type'] == 'participant':
                ilist.append({'id': entry['id'], **entry['attributes']['stats']})
            # 'roster' 타입이면 포함된 'data' 객체에 'rankx' 정보를 추가하며 'id_list'에 추가합니다.
            elif entry['type'] == 'roster':
                rank = entry['attributes']['stats']['rank']
                data_list = entry['relationships']['participants']['data']
                id_list.extend({'rankx': rank, **data} for data in data_list)

    # 플레이어와 관련된 통계 데이터를 데이터프레임으로 변환
    participant_id_df = pd.DataFrame(id_list)
    matches_df = pd.DataFrame(ilist)
    merged_df = pd.merge(left=matches_df, right=participant_id_df, how='inner', on='id')
    
    # 사용자 이름과 일치하는 데이터 필터링
    mask = merged_df['name'] == user_name
    one_user_data = merged_df[mask]

    return one_user_data, game_modes

def print_user_stats(one_user_data, game_modes, user_name):
    # 플레이어 통계 출력
    avg_kills = round(one_user_data['kills'].mean())
    win_rate = round(len(one_user_data[one_user_data['rankx'] == 1]) / len(one_user_data) * 100)
    max_kill_distance = round(one_user_data['longestKill'].max())
    avg_rank = round(one_user_data['rankx'].mean())
    death_count = len(one_user_data['deathType'] != 'alive')
    kill_sum = one_user_data['kills'].sum()
    assists_sum = one_user_data['assists'].sum()
    total_kda = round((kill_sum + assists_sum) / death_count)
    most_kill = one_user_data['kills'].max()
    lowest_kill = one_user_data['kills'].min()
    avg_time_survived = round(one_user_data['timeSurvived'].mean() / 60)
    avg_damage_dealt = round(one_user_data['damageDealt'].mean())
    game_count = len(one_user_data)

    print(f"------------ {user_name}님의 통계 ------------")
    print(f"게임 수 : {game_count}게임")
    print(f"평균 킬 수: {avg_kills}킬")
    print(f"승률: {win_rate}%")
    print(f"최대 거리 킬: {max_kill_distance}m")
    print(f"평균 등수: {avg_rank}등")
    print(f"전체 KDA: {total_kda}")
    print(f"최다 킬: {most_kill}")
    print(f"최저 킬: {lowest_kill}킬")
    print(f"평균 생존 시간: {avg_time_survived}분")
    print(f"평균 딜량: {avg_damage_dealt}")
    print(f"가장 많이 플레이한 게임 모드: {Counter(game_modes).most_common(n=1)[0][0]}")
    
        
if __name__ == "__main__":
    user_name = 'breakthebalance'#input("user name를 입력하세요: ")

    url1 = 'https://api.pubg.com/shards/kakao/players?filter[playerNames]='
    url = url1 + user_name

    header = {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628",
        "Accept": "application/vnd.api+json"
    }


one_user_data, game_modes = get_user_stats(user_name, url, header)
get_user_stats(user_name, url, header)
print_user_stats(one_user_data, game_modes, user_name)