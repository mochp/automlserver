import time

from main import app
from core import download,cutpdf
from conf import config

@app.task
def celery_download(jsons):
    jpgpath = config.PATH_PIC_DOWN
    pdfpath = config.PATH_PDF_DOWN
    res = download.download(jsons,jpgpath,pdfpath)
    return res

@app.task
def celery_cutpdf(jsons):
    res = cutpdf.cutpdf(jsons,config.PATH_PDF_CUT)
    return res

@app.task
def mul(x, y):
    # time.sleep(3)
    return x * y

@app.task
def xsum(numbers):
    # time.sleep(1)
    return sum(numbers)

