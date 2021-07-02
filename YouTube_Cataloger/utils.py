#!/usr/bin/env python3

# YouTube Cataloger API

from googleapiclient.discovery import build
import config
import json
import re

youtube_api = build('youtube', 'v3', developerKey=config.YT_API_KEY)

def compare_identities(channel_id, username):
    if channel_id == None and username == None:
        raise ValueError("A Channel ID or Username must be specified!")

# Return all channel statistics (Including superfluous information)
def get_all_channel_statistics(channel_id=None, username=None):
    compare_identities(channel_id, username)
    request = youtube_api.channels().list(
        part='statistics',
        id=channel_id,
        forUsername=username
    )
    response = request.execute()

    return response

# Return necessary channel statistics (Channel ID, View Count, Subscriber Count, Video Count)
def get_channel_statistics(channel_id=None, username=None):
    compare_identities(channel_id, username)
    data = get_all_channel_statistics(channel_id, username)['items'][0]
    data_statistics = data['statistics']

    organized_data = {
        'channel_id': data['id'],
        'statistics': {
            'viewCount': data_statistics['viewCount'],
            'subscriberCount': data_statistics['subscriberCount'],
            'videoCount': data_statistics['videoCount']
        }
    }

    return organized_data

def get_channel_id(yt_username):
    return get_channel_statistics(username=yt_username)['channel_id']

def get_channel_content_details(channel_id):
    request = youtube_api.channels().list(
        part='contentDetails',
        id=channel_id
    )
    response = request.execute()

    return response

def get_playlist_id(channel_id):
    data = get_channel_content_details(channel_id)
    return data['items'][0]['contentDetails']['relatedPlaylists']['uploads']

def catalog_all_videos(channel_id):
    playlist_id = get_playlist_id(channel_id)

    videos = []
    next_page_token = None

    # Append all video data
    while True:
        request = youtube_api.playlistItems().list(
            playlistId=playlist_id,
            part='snippet',
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        videos.append(response)

        try:
            next_page_token = response['nextPageToken']
        except:
            break

    organized_videos = []

    # Organize all video data by title, description, publish_data and video ID
    for json_object in videos:
        for video in json_object['items']:
            details = video['snippet']

            video_data = {
                'title': details['title'],
                'description': details['description'],
                'publishedAt': details['publishedAt'],
                'videoId': details['resourceId']['videoId']
            }

            organized_videos.append(video_data)

        data = {'videos': organized_videos}
    return data

# Timestamp videos from description
def timestamp_videos(video_data):
    video_data = video_data['videos']

    timestamped_videos = []
    for video in video_data:
        try:
            timestamps = {}

            regex_result = re.findall(r"[0-9]?[0-9]?:?[0-9]?[0-9]:[0-9][0-9].*", video['description'])

            for timestamp in regex_result:
                    time = re.findall(r"[0-9]?[0-9]?:?[0-9]?[0-9]:[0-9][0-9]", timestamp)[0].split(':')

                    # Calculate time in seconds
                    if len(time) == 2:
                        seconds = (int(time[0]) * 60) + int(time[1])
                    else:
                        seconds = (int(time[0]) * 60 * 60) + (int(time[1]) * 60) + int(time[2])
                    timestamps[timestamp] = seconds

                    if len(timestamps) == 0:
                        raise ValueError("No timestamps found in description")
                    else:
                        video['timestamps'] = timestamps
        except:
            pass
        timestamped_videos.append(video)

    return {'videos': timestamped_videos}

def catalog_all_timestamped_videos(channel_id):
    videos = catalog_all_videos(channel_id)
    videos = timestamp_videos(videos)
    return videos

def get_recent_activity(channel_id, published_before=None, published_after=None):
    request = youtube_api.activities().list(
        part='snippet',
        channelId=channel_id,
        maxResults=50,
        publishedBefore=published_before,
        publishedAfter=published_after
    )
    response = request.execute()
    return response