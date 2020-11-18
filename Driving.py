import flask
import numpy as np
import cv2
from waitress import serve
import werkzeug
import pytesseract
from DL import ids
from flask.json import jsonify
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
def tesseractfunc(img):
    return pytesseract.image_to_string(img)


app = flask.Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    # imagefile = flask.request.files["img"]
    # filename = werkzeug.utils.secure_filename(imagefile.filename)
    # #print("\nReceived image File name : " + imagefile.filename)
    # imagefile.save(filename)
    #print("This is what text is present in the file")
    filestr =  flask.request.files["img"].read()
    npimg  = np.frombuffer(filestr, np.uint8)
    imagefile = cv2.imdecode(npimg , cv2.IMREAD_COLOR)

    x=tesseractfunc(imagefile)

    #print(x)

    k=""
    y= x.split("\n")

    #print("this is after splitting the things up",y)

    for i in y:
        if ("license" in i.lower() or "licence" in i.lower()):
            k=i
    
    k=str(k.split(" ")[-1]) # Driving LIcense: 9461811765592
    #k=int(k)
    #print("printing k here", k)

    if k in ids:
        #print("This is the id that we're searching for", i)
        result= "Valid License"
    else:
        result= "Invalid License"
    #print("Just printing whatever information I needed is there or not", k)
    # print(type(k))
    # print(ids, k)
    print(result)
    return jsonify({"result":result})

app.run(host="127.0.0.1" , port=5000, debug=True)