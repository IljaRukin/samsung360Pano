#!/usr/bin/env python

import requests
import shutil
import time
import sys

class ApiError(Exception):
    print('ApiError: {}'.format(Exception))

def requestCamGet(url, data):
    resp = requests.get(url, json=data)
    if resp.status_code != 200:
        raise ApiError('status code = {}'.format(resp.status_code))
    return resp

def requestCamPost(url, data):
    resp = requests.post(url, json=data)
    if resp.status_code != 200:
        raise ApiError('status code = {}'.format(resp.status_code))
    return resp

BASEURL = 'http://192.168.107.1'
#['/osc/info', '/osc/state', '/osc/checkForUpdates', '/osc/commands/execute', '/osc/commands/status']}

data = {}
content = requestCamGet(BASEURL+'/osc/info', data).json()
print(content)

# get sessionId

data = {"name": "camera.startSession", "parameters": {}}
content = requestCamPost(BASEURL+'/osc/commands/execute', data).json()
print(content)

sessionId = content["results"]["sessionId"]
print ('SessionId: {}'.format(sessionId))

# take image

data = {"name": "camera.takePicture", "parameters": { "sessionId": sessionId} }
content = requestCamPost(BASEURL+'/osc/commands/execute', data).json()
print(content)

pictureId = content["id"]
print ('pictureId: {}'.format(pictureId))

# wait untill image is ready

sys.stdout.write('Waiting for image processing')
sys.stdout.flush()
for x in range(1, 30):
    sys.stdout.write('.')
    sys.stdout.flush()
    #data = {"id": pictureId } 
    #content = requestCamPost(BASEURL+'/osc/commands/status', data).json()
    data = {"name": "camera.listImages", "parameters": { "entryCount": 1} }
    content = requestCamPost(BASEURL+'/osc/commands/execute', data).json()
    if format(content["state"])=='done':
        sys.stdout.write('\n')
        break
    time.sleep(0.5)

#uri = content["results"]["fileUri"]
uri = content["results"]["entries"][0]["uri"]
print ('uri: {}'.format(uri))

# get image

data = {"name": "camera.getImage", "parameters": { "fileUri": uri} }
content = requestCamPost(BASEURL+'/osc/commands/execute', data)
#print(content.json())

# save image

#content.raw.decode_content = True
name="OSC_"+pictureId+".JPG"
with open(name,'wb') as ff:
    for chunk in content.iter_content(chunk_size=512):
        ff.write(chunk)
        
print ('Image stored as: {}'.format(name))



