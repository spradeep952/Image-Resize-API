import requests, shutil, os
from flask import Flask, jsonify, request, render_template
from convertImageScript import convertImage


app = Flask(__name__)


@app.route('/')
def home():
    welcomeObject = {"message":"Hello World","code":200}
    return welcomeObject

@app.route('/getimage')
def getImage():
    image_url = request.json['image_url']

    if os.path.exists('./downloadedImages'):
        file_name = './downloadedImages/downloaded image.jpeg'
    else:
        os.makedirs('./downloadedImages')
        file_name = './downloadedImages/downloaded image.jpeg'
    res = requests.get(image_url, stream = True)

    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')

    image_converted = False

    if convertImage(file_name):
        image_converted = True
        print("Image converted successfully")
    else:
        print("Something wrong happened.")

    res_object = {"image_url":image_url, "filename":file_name, "image_converted":image_converted}
    return jsonify(res_object)


if __name__ == '__main__':
    app.run()
