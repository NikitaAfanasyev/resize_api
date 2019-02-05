from flask import Flask, request, jsonify, abort,  make_response
import psycopg2
import os
from dbLogin import dbLogin
from tasks import cropImage


UPLOAD_FOLDER = './images'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])
conn = psycopg2.connect(dbLogin)
cursor = conn.cursor()

print(cursor.execute(f"select status from resizejobs where jobID={jobID}"))

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate(h, w, i):
    if (type(h) is not int) or (type(w) is not int) or (type(i) is not str):
        return (False)
    if not(1<=h<=9999) or not(1<=w<=9999):
        return (False)
    if not(i.endswith('.png')) and not(i.endswith('.jpg')):
        return (False)
    return True



@app.route('/imageUpload', methods=[ 'POST'])
def imageUpload():
    if 'file' not in request.files:
        return abort(make_response(jsonify(message="файл не загружен"), 400))
    file = request.files['file']
    if file.filename == '':
        return abort(make_response(jsonify(message="файл не загружен"), 400))
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return (jsonify({
        "success": True
    }))


@app.route("/resize", methods=['POST'])
def resize():
    try:
        height=request.get_json()['height']
        width=request.get_json()['width']
        imageName=request.get_json()['imageName']
    except:
        return abort(make_response(jsonify(message="не все параметры переданы"), 400))
    if validate(height, width, imageName) is not True:
        return abort(make_response(jsonify(message="некорректные параметры"), 400))
    cursor.execute(f"insert into resizeJobs (status, height, width, imageName) values ('added', {height}, {width}, '{imageName}') RETURNING jobID;")
    jobID = cursor.fetchone()[0]
    if jobID is None:
        return abort(500)
    conn.commit()
    cropImage.delay(width, height, os.path.join(app.config['UPLOAD_FOLDER'], imageName))
    return (jsonify({
        "jobID": jobID
    }))



@app.route("/getStatus", methods=['GET'])
def getStatus():
    try:
        jobID = int(request.args.get('jobID'))
    except:
        return abort(make_response(jsonify(message="некорректный ID задачи"), 400))
    cursor.execute(f"select status from resizeJobs where jobID={jobID}")
    status=cursor.fetchone()
    if status is None:
        return abort(make_response(jsonify(message="задача не найдена"), 404))
    status = status[0]
    return (jsonify({
        "status": status
    }))

app.run(port='5000')
