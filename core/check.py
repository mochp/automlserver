import json


def checkdata(jsondata):
    new = {"data":[],"info":"right format"}
    try:
        result = jsondata
        data = result["data"]
        for _,obj in enumerate(data):
            res = {"input": obj,
                   "output": {"status": "success",
                              "info": "",
                              "token": ""}}
            try:
                assert obj["url"]
                assert obj["modelId"]
                assert obj["type"] in ["pdf","jpg"]
            except Exception as e:
                res["output"]["status"]="failure"
                res["output"]["info"]=e
            finally:
                new["data"].append(res)
    except Exception as e:
        new["info"] = "wrong format"
        return new
    return new


