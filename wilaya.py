from app import app,jsonify,request
from model import *

@app.route('/api/wilayas')
def get_wilayas():
    wilayas = Wilaya.query.all()
    wilaya_schema = WilayaSchema(many=True)
    output = wilaya_schema.dump(wilayas)
    return jsonify(output)

@app.route('/api/wilaya',methods=['POST'])
def get_wilaya():
    name = request.json['name']
    wilaya = Wilaya.query.filter_by(name=name).first()
    wilaya_schema = WilayaSchema()
    output = wilaya_schema.dump(wilaya)
    return jsonify(output)