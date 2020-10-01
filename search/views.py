from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import inputForm
from isodate import parse_date, parse_duration
import requests
from django.conf import settings


def searchView(request):
    dict = {}
    videos = []
    form = inputForm()
    if request.method == 'POST':
        form = inputForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        vidoe_ids = []

        search_params = {
            'part': 'snippet',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'q': query,
            'maxResults': 45,
            'type': 'video',
        }
        r = requests.get(search_url, params=search_params)
        search_results = r.json()['items']

        for result in search_results:
            vidoe_ids.append(result['id']['videoId'])

        vidoe_params = {
            'part': 'snippet, contentDetails',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'id': ','.join(vidoe_ids),
            'maxResults': 45,
        }
        v = requests.get(video_url, params=vidoe_params)
        video_results = v.json()['items']

        for res in video_results:
            video = {
                'id': res['id'],
                'url': f'https://www.youtube.com/watch?v={res["id"]}',
                'thumbnails': res['snippet']['thumbnails']['high']['url'],
                'title': res['snippet']['title'],
                'duration': parse_duration(res['contentDetails']['duration']).total_seconds() // 60,
                'channelTitle': res['snippet']['channelTitle'],
                'channelUrl': f'https://www.youtube.com/channel/{res["snippet"]["channelId"]}',
                'publishedAt': parse_date(res['snippet']['publishedAt']).isoformat(),
            }
            videos.append(video)

    dict.update({'form': form})
    dict.update({'videos': videos})
    return render(request, 'ind.html', context=dict)


def playViedeo(request, str):
    dict = {}
# For getting the selected video and its information...........................
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    vidoe_params = {
        'part': 'snippet, contentDetails',
        'key': settings.YOUTUBE_DATA_API_KEY,
        'id': str,
    }
    v = requests.get(video_url, params=vidoe_params)
    res = v.json()['items']
    video = {
        'video_url': f'https://www.youtube.com/embed/{res[0]["id"]}',
        'title': res[0]['snippet']['title'],
        'publishedAt': parse_date(res[0]['snippet']['publishedAt']).isoformat(),
        'channelTitle': res[0]['snippet']['channelTitle'],
        'description': res[0]['snippet']['description'],
    }

#  Related videos............................
    related_videos = []
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    search_params = {
        'part': 'snippet',
        'key': settings.YOUTUBE_DATA_API_KEY,
        'type': 'video',
        'relatedToVideoId': str,
        'maxResults': 10,
    }
    r = requests.get(search_url, search_params)
    # print(r.text)
    related_results = r.json()['items']

    for item in related_results:
        tmp_video = {
            'id': item['id']['videoId'],
            'thumbnails': item['snippet']['thumbnails']['high']['url'],
            'title': item['snippet']['title'],
            'channelTitle': item['snippet']['channelTitle'],
            'channelUrl': f'https://www.youtube.com/channel/{item["snippet"]["channelId"]}',
            'publishedAt': parse_date(item['snippet']['publishedAt']).isoformat(),
        }
        related_videos.append(tmp_video)


# Comment..........................
    comment_url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    comnt_params = {
        'part': 'snippet, replies',
        'key': settings.YOUTUBE_DATA_API_KEY,
        'videoId': str,
    }
    c = requests.get(comment_url, comnt_params)
    print(c.text)

    dict.update({'video': video})
    dict.update({'related_videos': related_videos})

    return render(request, 'play_video.html', context=dict)
