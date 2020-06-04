from flask import Flask, jsonify
from flask import make_response
from flask import request, render_template
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import requests
import json
import socket

artists = [
    {
        'id': 1001,
        'name': 'Rain on me ',
        'artists': 'Lady Gaga & Ariana Grande',
        'external_urls': 'https://open.spotify.com/track/24ySl2hOPGCDcxBxFIqWBu?si=-8vcFSrcTwCFUdIHaZQG1Q '
        
      },
    { 
        'id': 1002,
        'name': 'Sweather Weather',
        'artists': 'The neighbourhood',
        'external_urls': 'https://open.spotify.com/track/2QjOHCTQ1Jl3zawyYOpxh6?si=aOMFmrlLSSqgS1tAPitfGQ '
      
     },
    {   
        'id': 1003,
        'name': 'Mercy on me',
        'artists': 'Christina Aguilera',
        'external_urls': 'https://open.spotify.com/track/47iIsNGLOQzzvjdSsVsScP?si=aAaeSfdDTZ-xt6P5OjHJTQ '
        
    }
]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def form():
    return render_template('index.html')

@app.route('/api/products', methods=['GET'])
def get_products():
    return jsonify({'artists': artists})

@app.route('/api/spo', methods = ['GET'])
def spoti():
 urn = '6S2OmqARrzebs0tKUEyXyp'
 sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
 response = sp.artist_top_tracks(urn)
 with open('data.txt','w') as outfile:
   json.dump(response,outfile)
 with open('data.txt') as file:
   data = json.load(file)
   for d in data['tracks']:
       obj= {'id': 5597, 'name' : d['name'], 'artists' : d['artists'] , 'external_urls' : d['external_urls']}
       headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
       r= requests.post("http://127.0.0.1:5000/api/products",data=json.dumps(obj),headers=headers) 
       print ("uhuuuu",r.status_code,r.reason)
 return ("Done. Go to api/products")
  
@app.route('/api/products', methods=['POST'])
def create_product():
    newProduct = {
        'id': artists[-1]['id'] + 1,
        'name': request.json['name'],
        'artists': request.json['artists'], 
        'external_urls': request.json['external_urls'],
       }
    artists.append(newProduct)
    return jsonify({'artists': newProduct}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(
        jsonify({'HTTP 404 Error': 'The content you looks for does not exist. Please check your request.'}), 404)


if __name__ == '__main__':
   app.run()
 
