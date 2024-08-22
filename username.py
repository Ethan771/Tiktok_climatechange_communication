import requests
import sqlite3
from datetime import datetime, timedelta
import sys

def process_data(data):
    cursor_var = data.get('data', {}).get('cursor', 0)
    search_id_var = data.get('data', {}).get('search_id', '')
    has_more = data.get('data', {}).get('has_more', False)
    return cursor_var, search_id_var, has_more

def make_api_request(headers, data, url):
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
        if e.response.status_code == 429:
            print("Quota exceeded, stopping program.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error during requests to {url} : {str(e)}")
        sys.exit(1)

def create_database(username):
    db_name = f"data/{username}_2021.db"
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
    return conn, cursor

def insert_data(cursor, videos):
    if not videos:
        print("No videos to insert.")
        return
    print(f"Attempting to insert {len(videos)} videos.")
    for video in videos:
        try:
            print(f"Processing video ID: {video['id']}")  # Debug: 输出处理的视频ID
            cursor.execute("""INSERT OR IGNORE INTO videos (
                id, username, create_time, region_code, video_description, music_id,
                like_count, comment_count, share_count, view_count, effect_ids,
                hashtag_names, playlist_id, voice_to_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    video['id'], video.get('username'), video.get('create_time'),
                    video.get('region_code'), video.get('video_description'),
                    video.get('music_id'), video.get('like_count'), video.get('comment_count'),
                    video.get('share_count'), video.get('view_count'),
                    ','.join(video.get('effect_ids', [])),
                    ','.join(video.get('hashtag_names', [])),
                    video.get('playlist_id'), video.get('voice_to_text')
                ))
            print(f"Inserted video ID: {video['id']}")  # Debug: 输出已插入的视频ID
        except sqlite3.Error as e:
            print(f"SQLite Error while inserting video ID {video['id']}: {e}")
    cursor.connection.commit()


def main():
    headers = {
        'Authorization': 'Bearer clt.2.kCfmhxU5hZTb3iTeXB4gBYxbMFyIgBAYNwjTuL3JSI2D_VNWPToZL9A9_wXcQkOnn97sBHzDMMXQ1rdNWn15JA*2',
        'Content-Type': 'application/json'
    }
    url = 'https://open.tiktokapis.com/v2/research/video/query/?fields=id,create_time,username,region_code,video_description,music_id,like_count,comment_count,share_count,view_count,effect_ids,hashtag_names,playlist_id,voice_to_text'

    usernames = ["tanyaplibersek", "chrisbowenmp", "edhusic"]
    start_date_str = "20210101"
    end_date_str = "20221231"

    for username in usernames:
        conn, cursor = create_database(username)
        current_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")

        while current_date <= end_date:
            date_str = current_date.strftime("%Y%m%d")
            data = {
                "query": {
                    "and": [
                        {
                            "operation": "EQ",
                            "field_name": "username",
                            "field_values": [username],
                        }
                    ],
                },
                "max_count": 10,
                "cursor": 0,
                "start_date": date_str,
                "end_date": date_str
            }

            response_data = make_api_request(headers, data, url)
            if response_data and 'data' in response_data and 'videos' in response_data['data']:
                videos = response_data['data']['videos']
                if videos:
                    print(f"Processing {len(videos)} videos for date {date_str}")
                    cursor_var, search_id_var, has_more = process_data(response_data)
                    print(f"Cursor: {cursor_var}, Search ID: {search_id_var}, Has More: {has_more}")
                    insert_data(cursor, videos)
                else:
                    print("No videos to process for this date.")
            else:
                print("No videos found in the response for this date.")

            current_date += timedelta(days=1)

        conn.close()
        print(f"Completed data scraping for {username}.")

if __name__ == "__main__":
    main()
