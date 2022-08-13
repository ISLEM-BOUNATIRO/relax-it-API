from app import app,jsonify,request
from model import *

@app.route('/api/devices')
def get_devices():
    devices = Device.query.all()
    device_schema = DeviceSchema(many=True)
    output = device_schema.dump(devices)
    return jsonify(output)

@app.route('/api/devices',methods=['POST'])
def add_device():
    SUCCESS="1"
    device = Device(ip = request.json['ip'],
    firmware_version = request.json['firmware_version'],
    model = request.json['model'],
    serial_number = request.json['serial_number'],
    type = request.json['type'],
    vendor = request.json['vendor']
    )
    db.session.add(device)
    db.session.commit()
    return {"result":SUCCESS}

@app.route('/api/devices/delete',methods=['POST'])
def delete_device():
    SUCCESS="2"
    ip = request.json['ip']
    device=Device.query.filter_by(ip=ip).first()
    db.session.delete(device)
    db.session.commit()
    return {"result":SUCCESS}



@app.route('/api/devices/edit',methods=['POST'])
def edit_device():
    SUCCESS="3"
    newDevice = Device(ip = request.json['ip'],
    firmware_version = request.json['firmware_version'],
    model = request.json['model'],
    serial_number = request.json['serial_number'],
    type = request.json['type'],
    vendor = request.json['vendor']
    )
    
    device=Device.query.filter_by(ip=newDevice.ip).first()
    db.session.delete(device)
    db.session.commit()
    db.session.add(newDevice)
    db.session.commit()
    return {"result":SUCCESS}
