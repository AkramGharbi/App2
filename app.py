from __future__ import print_function
from flask import Flask, jsonify, render_template, request
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from googleapiclient.http import MediaFileUpload
import pickle
import os,io
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import auth

flags = tools.argparser.parse_args(args=[])
app = Flask(__name__)
flags = None
serv=[]
@app.route('/')
def Home():
    return render_template('page.html')

@app.route('/Back_Auth')
def BackAuthentication():
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Drive API Python Quickstart'
    authInst = auth.auth(SCOPES,CLIENT_SECRET_FILE,APPLICATION_NAME)
    credentials = authInst.getCredentials()
    http = credentials.authorize(httplib2.Http())
    global serv
    serv = discovery.build('drive', 'v3', http=http)
    return True



def Upload_file(service,file_name,folder_id):
    file_names=[file_name]
    mime_types=['audio/mpeg']
    for i,j in zip(file_names, mime_types):
        file_metadata={
            'name': i,
            'parents': [folder_id]
            }
        media = MediaFileUpload('./{0}'.format(i),mimetype=j)
        service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()



@app.route('/record', methods=['GET','POST'])
def record(folder_id='1bVMs_yWr4MKOUM2w8DL9LTiS_rF7fCXO'):
    freq=16000 
    duration=5
    recording=sd.rec(int(duration * freq),samplerate=freq, channels=2)
    sd.wait()
    name='recording.mp3'
    write(name, freq, recording)
    res=BackAuthentication()
    Upload_file(serv,name,folder_id)

    return render_template('page.html',res=res)


@app.route('/folder')
def Create_Folder(service,name):
    nt_parks=[name]
    try: 
        for i in nt_parks:
            file_={'name': i, 'mimeType': 'application/vnd.google-apps.folder',}
            service.files().create(body=file_).execute()
    except:
        return False
    return True

if __name__== "__main__"
    app.run(debug=False,host='0.0.0.0')