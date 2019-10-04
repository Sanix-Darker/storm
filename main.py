# coding: utf-8
from flask import Flask, jsonify, request, render_template
# importing the requests library
import requests
import base64
import configparser as ConfigParser
import json
from os import listdir, system, path as ospath
from threading import Thread
import magic
from pathlib import Path

# Configs parameters configParser.get('your-config', 'path1')
configParser = ConfigParser.RawConfigParser()
configFilePath = r'config.txt'
configParser.read(configFilePath)

# Secrets parameters
Host = configParser.get('storm-config', 'Host')
Password = configParser.get('storm-config', 'Password')

# Let's link some dir
print("Linking dirs....")
system("ln -s '/home/darker/Downloads/Telegram Desktop/' /home/darker/ACTUALC/vagrant/PYTHON/STORM/static/videos/")

# api-endpoint
URL = Host

app = Flask(__name__)
app.config['Secret'] = "Secret"

@app.route('/', methods=['GET']) # To prevent Cors issues
def index():
    return render_template("index.html")

def check_is_video(file_path):
    # if ospath.isfile(file_path):
    #     mime = magic.Magic(mime=True)
    #     filename = mime.from_file(file_path)
    #     if filename.find('video') != -1:
    #         return True
    #     else:
    #         return False
    # else:
    #     return False
    for ext in [".mp4", ".flv", ".mkv", ".avi", ".3gp"]:
        if ext in file_path or ext.upper() in file_path:
            return True
        else:
            return False

@app.route('/getall', methods=['GET']) # To prevent Cors issues
def index2():
    # Sent in GET requests
    try:
        vids = listdir("./static/videos/")
        video_list = []
        for pathh in vids:
            pathh = "./static/videos/"+pathh
            print(">pathh: ", pathh)
            if(ospath.isfile(pathh)):
                print("Is File")
                if check_is_video(pathh):
                    video_list.append(pathh)
            else:
                print("Is Dir")
                if(ospath.isdir(pathh)):
                    print("Loop...")
                    for path in Path(pathh).glob('**/*'):
                        # because path is object not string
                        # encrypt or decrypt if it's only a file
                        if check_is_video(str(path)):
                            video_list.append(str(path))
                else:
                    if check_is_video(pathh):
                        video_list.append(pathh)

        video_list = [(request.url+"/"+(x)).replace("/getall", "") for x in video_list]

        response = jsonify({ 'status':'success', 'videos': video_list })
    except Exception as es:
        print(es)
        response = jsonify({ 'status':'error', 'message': 'Something went Wrong!' })

    # Let's allow all Origin requests
    response.headers.add('Access-Control-Allow-Origin', '*') # To prevent Cors issues
    return response


# @app.route('/logs', methods=['GET']) # To prevent Cors issues
# def index3():
#     try:
#         # Sent in GET requests
#         container = request.args.get('container')
#         # sending get request and saving the response as response object 
#         r = requests.get(url = URL+"/getlogs?container="+str(container)+"&password="+Password) 
#         jsonMessage = json.loads(str(r.content).replace("\\n", "").replace("b'", "").replace("'", ""))

#         # Build the response
#         response = jsonify({ 'status':'success', 'message': _base64.DECODE(jsonMessage['message'])[-50000:] })
#     except:
#         response = jsonify({ 'status':'error', 'message': 'Something went Wrong!' })

#     # Let's allow all Origin requests
#     response.headers.add('Access-Control-Allow-Origin', '*') # To prevent Cors issues
#     return response


# def ltunnel_process():
#     print("Starting ltunnel...")
#     os.system("lt --subdomain storm --port 1113")


if __name__ == "__main__":
    # Starting the ltunnel thread
    # Thread(target = ltunnel_process).start()

    # Starting the app
    app.run(host='0.0.0.0', debug=True, port=1113)
