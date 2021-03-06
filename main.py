# coding: utf-8
from flask import Flask, jsonify, request, render_template
# importing the requests library
import json
from os import listdir, system, path as ospath
from threading import Thread
from pathlib import Path


import configparser as ConfigParser

# Configs parameters configParser.get('your-config', 'path1')
configParser = ConfigParser.RawConfigParser()   
configFilePath = r'config.txt'
configParser.read(configFilePath)

# Secrets parameters
VideoDir = configParser.get('storm-config', 'VideoDir')


# Let's link some dir
with open("path_dirs.json", "r") as frr:
    json_ = json.loads(frr.read())
    for dir_ in json_:
        print("Linking dirs : "+dir_["path_dir"]+"...")
        system("ln -s '"+dir_["path_dir"]+"' '"+VideoDir+"'")


app = Flask(__name__)
app.config['Secret'] = "Secret"

@app.route('/', methods=['GET']) # To prevent Cors issues
def index():
    return render_template("index.html")

def check_is_video(file_path):
    file_path = file_path.replace(" ", "")
    for ext in [".mp4", ".flv", ".mkv", ".avi", ".3gp", "720p", "480p", "1080p"]:
        if ext in file_path or ext.upper() in file_path:
            return True
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


if __name__ == "__main__":
    # Starting the ltunnel thread
    # Thread(target = ltunnel_process).start()

    # Starting the app
    app.run(host='0.0.0.0', debug=True, port=1113)
