# import requests
# import pandas as pd

# # player의 게임당 id를 api에서 받아와 Dataframe으로 만드는 함수
# def get_stats_dataframe(url, header): 
#     r = requests.get(url, headers=header)
#     match_data_json = r.json()
#     match_data_df = pd.DataFrame(match_data_json['data'][0]['relationships']['matches']['data'])
#     return match_data_df

# def get_user_stats(user_name, url, header):
#     # API를 통해 플레이어의 게임당 통계 데이터 가져오기
#     player_data_df = get_stats_dataframe(url, header)

#     ilist, rank_list = [], []
#     dataframes, rankframes = {},{}
#     # 각 경기의 통계 데이터를 가져와 리스트에 추가
#     for i in range(5): #range(len(player_data_df)):
#         match_url = f'https://api.pubg.com/shards/kakao/matches/{player_data_df["id"][i]}'
#         match_r = requests.get(match_url, headers=header)
#         match_data = match_r.json()
        
#         line = []
#         rankx =[]
#         print(f"\n\n---------------{i+1}번째 판---------------\n")
        
#         for entry in match_data['included']:
#             # 'participant' 타입이면 'id' 정보를 아이템에 담아 'ilist' 리스트에 추가합니다.
#             if entry['type'] == 'participant':
#                 line.append({'id': entry['id'], **entry['attributes']['stats']})
                
#             elif entry['type'] == 'roster': # rank 추출
#                 for k in range(len(entry['relationships']['participants']['data'])):
#                     rankx.append({"rank": #entry['relationships']['participants']['data'][k]['rankx'],
#                                   entry['attributes']['stats']['rank'],
#                                   "id": entry['relationships']['participants']['data'][k]['id']})
                
                
#         ilist.append(line)
#         rank_list.append(rankx)
#         rankframes[f'rank_df_{i}'] =pd.DataFrame(rank_list[i])
#         dataframes[f'df_{i}'] =pd.DataFrame(ilist[i])
#         one_game_df = pd.merge(left = dataframes[f'df_{i}'] ,right = rankframes[f'rank_df_{i}'] ,how = 'inner',on = 'id')
#         # print(one_game_df)
        
        
#         # rank별로 그룹화
#         grouped_df = one_game_df.groupby('rank')
#         group_kiil_df = one_game_df.groupby('rank')['kills'].sum()
#         group_assists_df = one_game_df.groupby('rank')['assists'].sum()
    
#         # rank별 이름 킬 수 출력
#         for rank, group in grouped_df:
#             names = ', '.join(group['name'])
#             total_kills = group['kills'].sum()
#             print(f"{rank}등: {names}\n킬 수: {total_kills}")
       
#         # last_df = pd.merge(left = group_kiil_df,right = group_assists_df ,how = 'inner',on = 'rank')
        
#         # name_df = one_game_df[['rank','name']]
#         # last_name_df = pd.merge(left = last_df,right = name_df ,how = 'inner',on = 'rank')
#         # print(last_name_df)
        
#     return 0  
    

# if __name__ == "__main__":
#     user_name = 'breakthebalance' #input("user name를 입력하세요: ")

#     url1 = 'https://api.pubg.com/shards/kakao/players?filter[playerNames]='
#     url = url1 + user_name

#     header = {
#         "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628",
#         "Accept": "application/vnd.api+json"
#     }

# get_user_stats(user_name,url, header)





import requests
import pandas as pd

# 함수 정의: API 응답 데이터를 데이터프레임으로 변환
def get_dataframe(url, header):
    response = requests.get(url, headers=header)
    json_data = response.json()
    return pd.DataFrame(json_data['data'][0]['relationships']['matches']['data'])

# 함수 정의: 플레이어 PUBG 경기 통계 정보 획득
def get_statistics(username, url, header):
    player_df = get_dataframe(url, header)

    
    for index in range(len(player_df)):
        match_url = f'https://api.pubg.com/shards/kakao/matches/{player_df["id"][index]}'
        match_response = requests.get(match_url, headers=header)
        match_json = match_response.json()

        participant_list, rank_list = [], [] # 참가자 및 순위 리스트 생성
        
        print(f"\n\n---------------{username}님의 {index+1}번째 판---------------\n")
        
        for entry in match_json['included']:
            if entry['type'] == 'participant': # 게임내 데이터를 불러와 리스트안에 dirt형식으로 저장
                participant_list.append({'id': entry['id'], **entry['attributes']['stats']})
            elif entry['type'] == 'roster':
                rank = entry['attributes']['stats']['rank']
                data_list = entry['relationships']['participants']['data']
                rank_list.extend({'rankx': rank, **data} for data in data_list)
                
        # 데이터프레임 생성 및 병합
        participant_df = pd.DataFrame(participant_list)
        rank_df = pd.DataFrame(rank_list)
        game_result_df = pd.merge(left=participant_df, right=rank_df, how='inner', on='id')

        # 순위별 팀원 이름 및 통계 출력
        grouped_df = game_result_df.groupby('rankx')
        for rank, group in grouped_df:
            names = ', '.join(group['name'])
            total_kills = group['kills'].sum()
            total_assists = group['assists'].sum()
            print(f"{rank}등: {names}\n\t총 킬 수: {total_kills}\t총 어시스트 수: {total_assists}")

# 메인: 플레이어 이름 및 API 정보 설정 후 통계 함수 호출
if __name__ == "__main__":
    username = 'breakthebalance' #input("user name를 입력하세요: ") #
    url = f'https://api.pubg.com/shards/kakao/players?filter[playerNames]={username}'
    header = {
        "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJlNDc4M2VkMC1jMDc5LTAxM2ItNzJhYS0yNjgwMDVjNzgxYzMiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjgxODY1MzM4LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6Ii05ZTZiMmJmMi02MmZkLTRjYmItYTE5Yi1lZjk2NTVhZmUzZDkifQ.kdD8DEO8nWROgcsbswLtTgOz7KgjYmd-IzEbv-De628",
        "Accept": "application/vnd.api+json"
    }
 
    get_statistics(username, url, header)