#!/usr/bin/env python3

from youtube_data_api_client import YoutubeDataApiClient

YOUTUBE_DATA_CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_DATA_API_CLIENT_SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly']


def main():
    youtube = YoutubeDataApiClient(
        YOUTUBE_DATA_CLIENT_SECRETS_FILE, YOUTUBE_DATA_API_CLIENT_SCOPES)

    channel = youtube.get_my_channel()
    videos = youtube.get_my_videos()

    total_seconds = 0
    for video in videos:
        total_seconds += video['duration']

    print(total_seconds / 60 / 60)


if __name__ == '__main__':
    main()
