import flask
from waitress import serve
import werkzeug
import pytesseract
from DL import ids
from flask.json import jsonify
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
def tesseractfunc(img):
    return pytesseract.image_to_string(img)


app = flask.Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def handle_request():
    imagefile = flask.request.files["img"]
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    #print("\nReceived image File name : " + imagefile.filename)
    imagefile.save(filename)
    imagefilex= cv2.imread(filename)
    #print("This is what text is present in the file")
    hImg, wImg, _ =  imagefilex.shape
    boxes= pytesseract.image_to_data(imagefilex)
    for a, b in enumerate(boxes.splitlines()):
        if a!=0:
            b= b.split()
            print(b)
            if len(b)==12:
                a,y,w,h= int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv2.rectangle(imagefilex, (a,y), (w+a, h+y), (0,0,255), 3)
                cv2.putText(imagefilex, b[11], (a, hImg-y-5), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
                # imagefilex.save("\\changed.png")
                # img2show= cv2.imread("changed.png")
    # while True:            
    #     cv2.imshow("\\changed image",imagefilex)
    #     c = cv2.waitKey(7) % 0x100
    #     if c == 27 or c == 10:
    #         break
                # if not cv2.imwrite("D:\DrivingLicense","changed.png"):
                #     raise Exception("Could not write image")
                # cv2.imwrite("D:\\DrivingLicense","\\changed.png")
    #print(x)

    print("Now the program is starting")
    x=tesseractfunc(filename)
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