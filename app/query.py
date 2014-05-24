#!/usr/bin/python
import json
import requests
import Image
import ImageOps
import urllib
import os
from google_spreadsheet.api import SpreadsheetAPI
from datetime import datetime
from config import GOOGLE_SPREADSHEET, NPR_API_KEY, ABSOLUTE_PATH
from cStringIO import StringIO


def list_sheets():
    """The API sheet_key is not the same as the key in the URL. This function
    just prints out all sheet keys"""
    api = SpreadsheetAPI(GOOGLE_SPREADSHEET['USER'],
        GOOGLE_SPREADSHEET['PASSWORD'],
        GOOGLE_SPREADSHEET['SOURCE'])
    spreadsheets = api.list_spreadsheets()
    for sheet in spreadsheets:
        print sheet


def get_google_sheet(sheet_key=False, sheet_id='od6'):
    """Uses python_google_spreadsheet API to interact with sheet"""
    api = SpreadsheetAPI(GOOGLE_SPREADSHEET['USER'],
        GOOGLE_SPREADSHEET['PASSWORD'],
        GOOGLE_SPREADSHEET['SOURCE'])
    sheet = api.get_worksheet(sheet_key, sheet_id)
    sheet_object = sheet.get_rows()
    return sheet_object


def get_concerts():
    """Get all concerts from the Google Drive doc"""
    concerts = get_google_sheet('tVMaafzEd2pVoKriuwjgdQw')
    for concert in concerts:
        date = datetime.strptime(concert['date'], '%m/%d/%Y')
        time = datetime.strptime(concert['time'], '%H:%M:%S')
        concert['date'] = date.strftime('%m/%d').lstrip('0')
        concert['day_of_week'] = date.strftime('%a')
        concert['time'] = time.strftime('%I:%M').lstrip('0')

    return concerts


def api_feed(tag, numResults=1, char_limit=140, thumbnail=False, sidebar=False):
    """Query the NPR API using given tag ID, return dictionary of results"""

    stories = query_api(tag, numResults)

    story_list = []
    for story in stories:
        link = story['link'][0]['$text']
        date = convert_date(story['storyDate']['$text'])
        title = story['title']['$text'].strip()

        byline = {}
        try:
            byline['name'] = story['byline'][0]['name']['$text']
            byline['url'] = story['byline'][0]['link'][0]['$text']
        except KeyError:
            byline = False
            continue

        if byline['name'] != 'Robert Resnik':
            continue

        try:  # if there's an image, determine orientation and define boundary
            story_image = story['image'][0]['crop'][0]
            image = story_image['src']
            width = int(story_image['width'])
            height = int(story_image['height'])
            if int(width) > int(height):
                landscape = True
                if width > 728:  # biggest size for landscape photos
                    width = 728
            else:
                landscape = False
                if width > 223:  # biggest size for portrait photos
                    width = 223
        except KeyError:
            image = False  # set equal to url string for default image
            landscape = False

        full_text = [i['$text'] for i in story['text']['paragraph'] if len(i) > 1]
        # if len(i) > 1 ignores pars w/ no text, i.e. when images or audio

        char_count = 0
        paragraphs_needed = 0
        par_count = len(full_text)
        while char_count < char_limit and paragraphs_needed < par_count:
            paragraph = full_text[paragraphs_needed]
            char_count += len(paragraph)
            paragraphs_needed += 1

        text = full_text[:paragraphs_needed]

        if thumbnail:
            try:
                image_url = story['image'][0]['crop'][0]['src']
                if sidebar:
                    image = generate_thumbnail(image_url, preserve_ratio=True, size=(326, 326))
                else:
                    image = generate_thumbnail(image_url, preserve_ratio=True, size=(width, height))
            except KeyError:
                image = False

        story_list.append({
            'title': title,
            'date': date,
            'link': link,
            'image': image,
            'text': text,
            'byline': byline,
            'landscape': landscape
        })

    return story_list


def query_api(tag, numResults=10):
    """Hits the NPR API, returns JSON story list"""

    id_string = ','.join([str(s) for s in tag])
    query = ('http://api.npr.org/query?orgid=692' +
        '&fields=title,byline,storyDate,image,text,audio' +
        '&sort=dateDesc' +
        '&action=Or' +
        '&output=JSON' +
        '&numResults=%d' +
        '&id=%s' +
        '&apiKey=%s') % (numResults, id_string, NPR_API_KEY)

    r = requests.get(query)
    j = json.loads(r.text)
    stories = j['list']['story']

    return stories


def generate_thumbnail(image_url, preserve_ratio=False, size=(220, 165)):
    """Take an image src, generate a thumbnail, return new path"""

    filename = image_url.rsplit('/', 1)[1]
    if "?" in filename:
        filename = filename.rsplit("?", 1)[0]
    path_to_read = 'img/thumbnails/' + filename
    path_to_save = ABSOLUTE_PATH + 'static/' + path_to_read

    if not os.path.isfile(path_to_save):
        img_file = urllib.urlopen(image_url)
        img = StringIO(img_file.read())
        image = Image.open(img)
        if preserve_ratio:
            width = image.size[0]
            height = image.size[1]
            new_height = size[0] * height / width
            size = (size[0], new_height)
        im = ImageOps.fit(image, size, Image.ANTIALIAS)
        im.save(path_to_save)

    return path_to_read


def convert_date(timestamp):
    """Converts API timestamp to publication-ready dateline"""

    day = timestamp[5:7]
    month = datetime.strptime(timestamp[8:11], '%b').strftime('%B')
    year = timestamp[12:16]
    date = month + ' ' + day + ", " + year
    return date
