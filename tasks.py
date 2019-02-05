from PIL import Image
import psycopg2
from dbLogin import dbLogin
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379/0')


@app.task
def cropImage(w, h, path):
    try:
        conn = psycopg2.connect(dbLogin)
        cursor = conn.cursor()
        img = Image.open(path)
        img.thumbnail((w,h), Image.BICUBIC)
        img.save(path)
        status='success'
    except:
        status='error'
    cursor.execute(f"UPDATE resizeJobs SET status={status}")
    conn.commit()