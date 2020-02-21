from tasks import celery_download, celery_cutpdf
from celery import group, chain
from core import check
import json

def respon(jsondata):
    res = check.checkdata(jsondata)
    if res["info"] == "right format":
        new = {"data":[],"info":"right format"}
        parse = res["data"]
        for i,obj in enumerate(parse):
            if obj["output"]["status"] == "success":
                token = chain(celery_download.s(obj) | celery_cutpdf.s())()
                obj["output"]["token"] = token.id
            new["data"].append(obj)
    return res

    

with open("docs/downtask/new.json","r") as f:
    jsondata = json.load(f)

res = respon(jsondata)
# with open("docs/downtask/res.json","w") as f:
#     json.dump(res,f)
