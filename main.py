#!/usr/bin/env python3

import math

from youtube_data_api_client import YoutubeDataApiClient

YOUTUBE_DATA_CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_DATA_API_CLIENT_SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly']


def main():
    youtube = YoutubeDataApiClient(
        YOUTUBE_DATA_CLIENT_SECRETS_FILE, YOUTUBE_DATA_API_CLIENT_SCOPES)

    channel = youtube.get_my_channel()
    video_ids = youtube.get_my_video_ids()
    videos = youtube.get_videos(video_ids)

    total = {
        'duration': 0,
        'like_count': 0,
        'dislike_count': 0
    }
    for video in videos:
        total['duration'] += video['duration']
        total['like_count'] += video['like_count']
        total['dislike_count'] += video['dislike_count']

    total_hours = total['duration'] / 60 / 60

    print(channel['title'])
    print('配信回数:', channel['video_count'])
    print('総視聴回数:', channel['view_count'])
    print('チャンネル登録者数', channel['subscriber_count'])
    print('総高評価数', total['like_count'])
    print('総低評価数', total['dislike_count'])
    print('総配信時間', math.floor(total_hours))


if __name__ == '__main__':
    main()
