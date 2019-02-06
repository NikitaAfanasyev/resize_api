from PIL import Image
import psycopg2
from dbLogin import dbLogin
from celery import Celery
import os


UPLOAD_FOLDER = './images'
app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def cropImage(w, h, imgName, id):
    conn = psycopg2.connect(dbLogin)
    cursor = conn.cursor()
    try:
        path=os.path.join(UPLOAD_FOLDER, imgName)
        img = Image.open(path)
        img = img.resize((w,h), Image.BICUBIC)
        img.save(path)
        status='success'
    except Exception as e:
        print(e)
        status='error'
    cursor.execute(f"UPDATE resizeJobs SET status='{status}' where jobID='{id}'")
    conn.commit()
    return 0