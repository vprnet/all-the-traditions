from index import app
from flask import render_template, request
from query import get_concerts, api_feed
from config import BASE_URL


@app.route('/')
def index():
    page_url = BASE_URL + request.path
    page_title = 'All The Traditions'
    concerts = get_concerts()
    stories = api_feed([188696616], numResults=15, thumbnail=True)
    if len(stories) > 5:
        stories = stories[:5]

    social = {
        'title': "All The Traditions",
        'subtitle': "Folk and World Music with host Robert Resnik",
        'img': "static/img/robert_resnik_tophat_300x450.jpg",
        'description': "Each week, host Robert Resnik plays music from bands and artists performing in the area. Find out where they're playing here.",
        'twitter_text': "Folk and World Music with host Robert Resnik",
        'twitter_hashtag': ""
    }

    return render_template('content.html',
        page_title=page_title,
        social=social,
        concerts=concerts,
        stories=stories,
        page_url=page_url)


@app.route('/playlist')
def playlist():
    page_url = BASE_URL + request.path
    page_title = 'All The Traditions Playlist'

    social = {
        'title': "All The Traditions Playlist",
        'subtitle': "Local Concerts From Artists On All The Traditions",
        'img': "",
        'description': "Each week, host Robert Resnik plays music from bands and artists performing in the area. Find out where they're playing here.",
        'twitter_text': "",
        'twitter_hashtag': ""
    }

    return render_template('iframe.html',
        page_title=page_title,
        social=social,
        page_url=page_url)
