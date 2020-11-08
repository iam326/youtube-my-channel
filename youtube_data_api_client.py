#!/usr/bin/env python3

import os

import httplib2
import isodate

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0
To make this sample run you will need to populate the client_secrets.json file
found at:
   %s
with information from the API Console
https://console.developers.google.com/
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
"""


class YoutubeDataApiClient():

    def __init__(self, client_secrets_file, scopes):
        self.__client = self.get_youtube_data_api_client(
            client_secrets_file, scopes)

    def get_youtube_data_api_client(self, client_secrets_file, scopes):
        message = MISSING_CLIENT_SECRETS_MESSAGE % os.path.abspath(
            os.path.join(os.path.dirname(__file__), client_secrets_file))
        flow = flow_from_clientsecrets(client_secrets_file,
                                       scope=scopes,
                                       message=message)

        storage = Storage('youtube-oauth2.json')
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))

    def get_my_channel(self):
        channels = self.__client.channels().list(
            part='snippet,statistics',
            mine=True,
            fields='items(id,snippet(title,description),statistics(videoCount,viewCount,subscriberCount))'
        ).execute()
        channel = channels['items'][0]
        snippet = channel['snippet']
        statistics = channel['statistics']
        return {
            'id': channel['id'],
            'title': snippet['title'],
            'description': snippet['description'],
            'video_count': statistics['videoCount'],
            'view_count': statistics['viewCount'],
            'subscriber_count': statistics['subscriberCount'],
        }

    def get_my_videos(self):
        search_list_request = self.__client.search().list(
            part='id',
            forMine=True,
            type='video',
            order='date',
            maxResults=50,
            fields='nextPageToken,items(id(videoId))'
        )

        video_ids = []
        while search_list_request:
            search_list_response = search_list_request.execute()

            for video in search_list_response['items']:
                video_ids.append(video['id']['videoId'])

            search_list_request = self.__client.search().list_next(
                previous_request=search_list_request,
                previous_response=search_list_response)

        videos = []
        for ids in self.__chunks(video_ids, 50):
            videos_list = self.__client.videos().list(
                id=','.join(ids),
                part='snippet,contentDetails,statistics',
                fields='items(id,snippet(title,description,publishedAt),contentDetails(duration),statistics(viewCount,likeCount,dislikeCount,commentCount))'
            ).execute()
            for item in videos_list['items']:
                snippet = item['snippet']
                details = item['contentDetails']
                statistics = item['statistics']

                # https://stackoverflow.com/a/16743442
                duration = isodate.parse_duration(details['duration'])

                videos.append({
                    'id': item['id'],
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'published_at': snippet['publishedAt'],
                    'duration': int(duration.total_seconds()),
                    'view_count': statistics['viewCount'],
                    'like_count': statistics['likeCount'],
                    'dislike_count': statistics['dislikeCount'],
                    'comment_count': statistics['commentCount']
                })

        return videos

    def __chunks(self, l, n):
        # https://stackoverflow.com/a/312464
        for i in range(0, len(l), n):
            yield l[i:i + n]
