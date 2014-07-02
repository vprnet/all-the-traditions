from index import app
from flask import render_template, request
from query import get_concerts
from config import BASE_URL


@app.route('/performances')
def playlist():
    """ Generates an iframe of concert listings to be used on the All The
    Traditions program page: http://digital.vpr.net/programs/all-traditions

    Concerts come from a Google Sheet: https://docs.google.com/spreadsheet/ccc?key=0AtWnpcGxoF0xdFZNYWFmekVkMnBWb0tyaXV3amdkUXc&usp=sharing"""

    page_url = BASE_URL + request.path
    page_title = "All The Tradition's Performance Calendar"
    concerts = get_concerts()

    return render_template('iframe.html',
        page_title=page_title,
        concerts=concerts,
        page_url=page_url)
