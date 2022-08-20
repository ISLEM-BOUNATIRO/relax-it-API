from app import *
from model import *
import json

def wilayas(jsonFile):
    try:
        wilayas = Wilaya.query.delete()
        db.session.commit()
        f = open(jsonFile)
        data = json.load(f)

        for i in data['data']:
            fill_in_wilaya(i['name'],
            i['num'])
        f.close()
    except Exception:
        return {"error":"An error has occured"}

def fill_in_wilaya(name,num):
    try:
        row = Wilaya(name=name, num=num)
        db.session.add(row)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session.rollback()
        return {"error":"An error has occured"}
    except Exception:
        return {"error":"An error has occured"}

wilayas("json_files/wilayas.json")