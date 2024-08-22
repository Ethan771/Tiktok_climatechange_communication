import requests
import sqlite3
from datetime import datetime, timedelta
import sys
import time

def process_data(data):
    cursor_var = 0
    search_id_var = ''

    if data.get('data', {}).get('has_more', False):
        cursor_var = data['data'].get('cursor', 0)
        search_id_var = data['data'].get('search_id', '')

    return cursor_var, search_id_var

def make_api_request(start_date, end_date, cursor=0, search_id='', error_count=0):
    additional_terms=["climate_change","ClimateChange","climatechange", "cliamtechanges",
    "greentrees", "cleanwater", "ecosystem", 
    "protecttheenvironment", "protectenvironment", "protectthetrees",  
    "globalwarming", "savetheearth", "savetheplanet", "climateaction", 
    "climatechangeisreal", "saveouroceans", "ecology", "ecofriendly", 
    "zerowaste", "pollution", "pollutions", "pollutionawareness", 
    "pollutionsolution", "waterpollution", "oceanpollution", "airpollution", 
    "lightpollution", "plasticpollution", "flood", "flashflood", 
    "climatechangefacts", "climatechangeactivities", "climate", 
    "climatecrisis", "environment", "severeweather", "clima", 
    "weirdweather", "naturedisasters", "fossilfuels", "greenenergy", 
    "extremeweather", "climateemergency", "biodiversity", "climatetech", 
     "climatechangescam", "carbonemissions", "climatejustice", 
    "forclimate", "climateadaption", "climateanxiety", "climatestrike", 
    "climatecontrol", "climateclock", "climatescience", "climatesolutions", 
    "climategrief", "climatedoom", "climatetokers", "climateprotest", 
    "climaterio", "extremeclimate", "climatizacao", "climatisation", 
    "climatechangekills", "actionforclimate", "stopclimatechange", 
    "fightingclimatechange", "environmentchallenge", "environmenttok", 
    "environmental", "environmentalism", "environmentfriendly", 
    "environmentalawareness", "environmentalprotection", 
    "EnvironmentallyFriendly", "environnement", "worldenvironmentday", 
    "savetheenvironment", "cleanenvironment", "toxicenvironment", 
     "EarthDay", "saveearth", "earthmonth", 
    "motherearth", "lettheearthbreathe", "wildlifeplanet", "sustainability",
    "climateeducation", "greentech", "climateactivist", "parisagreement ", 
    "climatechallenge", "climateactivism", "climateprotest", "climatepolicy", 
    "climateactionnow", "climatedenial", "actonclimate", "climateresilience", 
    "climatechangematters", "goodclimatenews", "climatechangekills", "climateproblem", 
    "climateadvocacy", "climateoptimism"] 
    url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,create_time,username,region_code,video_description,music_id,like_count,comment_count,share_count,view_count,effect_ids,hashtag_names,playlist_id,voice_to_text'
    headers = {
        'Authorization': f'Bearer clt.2.lev1mrD-pgZETwDphWB04ps02TqBeOTuxg53wNhZVs8hVFZD2CFwelnouevF_l6pAX1_ySR0_4GO-15kIFQKfQ*1',
        'Content-Type': 'application/json'
    }

    data = {
        "query": {
            "and": [
                {
                    "operation": "IN",
                    "field_name": "region_code",
                    "field_values": ['FR', 'TH', 'MM', 'BD', 'IT']  # (省略其他代码)
                },
                {
                    "operation": "IN",
                    "field_name": "hashtag_name",
                    "field_values": additional_terms,
                }
            ],
        },
        "max_count": 100,
        "cursor": cursor,
        "search_id": search_id,
        "start_date": start_date,
        "end_date": end_date
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            new_data = response.json()
            new_cursor, search_id = process_data(new_data)
            print("Update Cursor:", new_cursor)
            return new_data, new_cursor, search_id, 0  # 重置error_count
        
        elif response.status_code == 429:
            print("Error with TikTok API request: 429 Daily quota limit exceeded. Stopping the program.")
            print("search ID: ", search_id)
            sys.exit(1)
        else:
            print("Error with TikTok API request:", response.status_code, response.text)
            return None, cursor, search_id, error_count + 1

    except Exception as e:
        print("Error with TikTok API request:", e)
        return None, cursor, search_id, error_count + 1
    
def get_dates_for_query(days_back):
    
    end_date = datetime.now()- timedelta(days=days_back)
    start_date = end_date 

    start_date_str = start_date.strftime('%Y%m%d')
    end_date_str = end_date.strftime('%Y%m%d')

    return start_date_str, end_date_str

def create_database(start_date):
    db_name = f"data/{start_date}.db"  
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        username TEXT,
        create_time TEXT,
        region_code TEXT,
        video_description TEXT,
        music_id INTEGER,
        like_count INTEGER,
        comment_count INTEGER,
        share_count INTEGER,
        view_count INTEGER,
        effect_ids TEXT,
        hashtag_names TEXT,
        playlist_id INTEGER,
        voice_to_text TEXT          
    )
''')
    conn.commit()
    return conn

def insert_data(conn, videos):
    cursor = conn.cursor()
    for video in videos:
        video_id = video['id']
        username = video.get('username', None)
        create_time = video.get('create_time', None)
        region_code = video.get('region_code', None)
        video_description = video.get('video_description', None)
        music_id = video.get('music_id', None)
        like_count = video.get('like_count', None)
        comment_count = video.get('comment_count', None)
        share_count = video.get('share_count', None)
        view_count = video.get('view_count', None)
        effect_ids = video.get('effect_ids', [])
        effect_ids_str = ','.join(effect_ids) if effect_ids else None
        hashtag_names = video.get('hashtag_names', [])
        hashtag_names_str = ','.join(hashtag_names) if hashtag_names else None
        playlist_id = video.get('playlist_id', None)
        voice_to_text = video.get('voice_to_text', None)
        

        cursor.execute("""
            INSERT OR IGNORE INTO videos (
                id, username, create_time, region_code, video_description, music_id, 
                like_count, comment_count, share_count, view_count, effect_ids, 
                hashtag_names, playlist_id, voice_to_text
            ) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            video_id, username, create_time, region_code, video_description, music_id, 
            like_count, comment_count, share_count, view_count, effect_ids_str, 
            hashtag_names_str, playlist_id, voice_to_text
        ))

    conn.commit()

def main():
    for i in range(20230424, 20230431):
        start_date, end_date = datetime.strptime(str(i), '%Y%m%d').strftime('%Y%m%d'), datetime.strptime(str(i), '%Y%m%d').strftime('%Y%m%d')
        conn = create_database(start_date)

        cursor = 0
        search_id = ''
        error_count = 0
        last_successful_cursor = 0  # 保存最后一个成功的光标
        
        while True:
            api_response, new_cursor, search_id, error_count = make_api_request(start_date, end_date, cursor, search_id, error_count)
            
            if api_response and 'data' in api_response and 'videos' in api_response['data']:
                video_list = api_response['data']['videos']
                insert_data(conn, video_list)

                last_successful_cursor = new_cursor  # 更新最后一个成功的光标
                cursor = new_cursor if new_cursor != 0 else last_successful_cursor  # 确保cursor不会变成0

                if not api_response['data'].get('has_more', False):
                    break

            else:
                if error_count >= 5:
                    print(f"连续错误5次，返回到上一个成功的光标位置: {last_successful_cursor}")
                    cursor = last_successful_cursor  # 返回到最后一个成功的光标位置
                    error_count = 0  # 重置错误计数器
                else:
                    print(f"错误次数增加到 {error_count}，重试...")
                time.sleep(5)  # 等待5秒后重试

        conn.close()

if __name__ == "__main__":
    main()
