from flask import Flask, render_template, session, redirect, request, url_for,jsonify
from flask.ext.mobility import Mobility
from flask.ext.mobility.decorators import mobile_template
import json 
import requests
from forms import MoodForm
import indicoio
import random
import os 

app = Flask(__name__)
Mobility(app)

app.secret_key = os.environ.get('MOODMUSICKEY')

###ROUTING###
@app.route('/', methods = ['GET', 'POST'])
def index():
    form = MoodForm(request.form)
    if request.method == 'POST' and form.validate():
        result = sentiment(form.entry.data)
        mood = result[0]
        spot = spotify(result[1])
        return render_template('results.html', mood=mood, spot=spot)
    return render_template('index.html', form=form)

def sentiment(text_input):

    #song lists created using radio billboard list and indicoio algorithm on song lyrics

    list1 = ["Sorry", "What do you mean", "Same Old Love", "Here", "Hit The Quan", "Good For You"]
    list2 = ["Focus", "Where Ya At", "Hello", "Locked Away", "Lean On", "Confident"]
    list3 = ["Jumpman", "Trap Queen", "Renegades", "White Iverson", "Shut Up and Dance", "Hotline Bling"]
    list4 = ["Drag Me Down", "Downtown", "Perfect", "Again", "Stitches", "679"] 
    list5 = ["My Way", "Ex's & Oh's", "Antidote", "Like I'm gonna lose you", "Tennessee Whiskey", "See You Again", "Watch Me", "On My Mind", "I'll Show You",
    "Cheerleader", "The Hills", "Uptown Funk!", "Die a Happy Man", "How Deep Is Your Love", "Photograph", "Can't feel my face"]

    indicoio.config.api_key = os.environ.get('INDICO')
    #text_input = raw_input('Tell me about your day: ') #raw_input for python 2.7
    sentiment = indicoio.sentiment_hq(text_input)
    songTitle = ""
    dayDescription = ""
    print(sentiment)
    #0<SUPERSAD<.25<SAD<.45<NEUTRAL<.6<HAPPY<.8<SUPERHAPPY<1
    if sentiment < .15:
        dayDescription = ("awful")
        songTitle = (list1[(int)(random.random()*len(list1))])
    else:
        if sentiment < .35:
            dayDescription = ("bad")
            songTitle = (list2[(int)(random.random()*len(list2))])
        else:
            if sentiment < .65:
                dayDescription = ("ok")
                songTitle = (list3[(int)(random.random()*len(list3))])
            else:
                if sentiment <.9:
                    dayDescription = ("good")
                    songTitle = (list4[(int)(random.random()*len(list4))])
                else:
                    dayDescription = ("awesome")
                    songTitle = (list5[(int)(random.random()*len(list5))])
    values = [dayDescription, songTitle]
    return values

def spotify(song_name):
    temp = ''
    for i in range(len(song_name)):
        if song_name[i] == ' ':
			temp += '+'
        else:
			temp += song_name[i]
    r = requests.get('https://api.spotify.com/v1/search?query=' + temp + '&type=track')
    json_object = json.loads(r.text)
    return 'https://embed.spotify.com/?uri=https://open.spotify.com/track/' + json_object["tracks"]["items"][0]["id"]

if __name__ == "__main__":
    app.run(debug=True)