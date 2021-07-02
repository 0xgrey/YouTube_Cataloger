#!/usr/bin/env python3

import config
from utils import *

# Test utils.py API
# Proof of Concept: John Hammond's YouTube Channel (https://www.youtube.com/user/RootOfTheNull)
# John Hammond's YouTube Username: RootOfTheNull


# Get Channel ID
channel_id = get_channel_id('RootOfTheNull')

# Get All Channel Statistics (Includes superfluous information)
# all_channel_stats = get_all_channel_statistics(channel_id)

# Get Channel Statistics
# channel_stats = get_channel_statistics(channel_id)

# Get Channel Content Details
# channel_content_details = get_channel_content_details(channel_id)

# Get Playlist ID
# playlist_id = get_playlist_id(channel_id)

# Catalog All Videos
# all_videos = catalog_all_videos(channel_id)

# Timestamp Returned Videos
# all_videos_timestamped = timestamp_videos(all_videos)

# Catalog All Videos Timestamped
# all_cataloged_videos_timestamped = catalog_all_timestamped_videos(channel_id)

# Get Recent Activity
recent_activity = get_recent_activity(channel_id)




# Print Output

# Channel ID
# print(channel_id)

# All Channel Statistics
# print(all_channel_stats)

# Channel Statistics
# TODO: print relevant info (ie sub count, # of videos)
# print(channel_stats)

# Content Details
# print(channel_content_details)

# Playlist ID
# print(playlist_id)


# Catalog All Videos
# print(json.dumps(all_videos, indent=4))

# Timestamp Returned Videos
# print(json.dumps(all_videos_timestamped, indent=4))

# Catalog All Videos Timestamped
# print(json.dumps(all_videos_timestamped, indent=4))

# Recent Channel Activity
print(json.dumps(recent_activity, indent=4))




# datetime.utcnow().isoformat()[:-3] + 'Z'
