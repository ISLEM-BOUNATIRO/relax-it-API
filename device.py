from app import app,jsonify,request
from model import *
from scan import reachable,get_cisco_device_info,get_device_type,get_fortinet_info
#FORTICLIENT
#Username islem.bounatiro
#Password j2t$vTbq
# ssh -o KexAlgorithms=diffie-hellman-group1-sha1 -o Ciphers=aes256-cbc admin@10.117.5.253   
@app.route('/api/get_device_info',methods=['POST'])
def get_device_info():
    ip=request.json['ip']
    #username=request.json['username']
    #password=request.json['password']
    username='admin'
    password='admin'
    ip=request.json['ip']
    if not reachable(ip): # PINGING THE ADDRESS
        return {"result": "error " +ip+" is unreachable"}
    elif(get_device_type(ip)=="Firewall" ):
        device=get_fortinet_info(ip)
        device_schema = DeviceSchema()
        output = device_schema.dump(device)
        return jsonify(output)
    elif(get_device_type(ip)=="Router" or get_device_type(ip)=="Switch"):
        device=get_cisco_device_info(ip,username,password)
        device_schema = DeviceSchema()
        output = device_schema.dump(device)
        return jsonify(output)
    
        
@app.route('/api/devices')
def get_devices():
    devices = Device.query.all()
    device_schema = DeviceSchema(many=True)
    output = device_schema.dump(devices)
    return jsonify(output)

@app.route('/api/device',methods=['POST'])
def get_device():
    ip = request.json['ip']
    device = Device.query.filter_by(ip=ip).first()
    device_schema = DeviceSchema()
    output = device_schema.dump(device)
    return jsonify(output)

@app.route('/api/devicelist',methods=['POST'])
def get_devicelist():
    iplist = request.json['iplist']
    devices = Device.query.all()
    devicelist=[]
    for d in devices :
        if (d.ip in iplist):
            devicelist.append(d)
    device_schema = DeviceSchema(many=True)
    output = device_schema.dump(devicelist)
    return jsonify(output)

@app.route('/api/devices',methods=['POST'])
def api_add_device():
    device = Device(ip = request.json['ip'],
    type = request.json['type'],
    hostname = request.json['hostname'],
    model = request.json['model'],
    vendor = request.json['vendor'],
    serial_number = request.json['serial_number'],
    firmware_version = request.json['firmware_version'])
    return add_device(device)
def add_device(device:Device):
        result=""
        try:
            db.session.add(device)
            db.session.commit()
            result="1"
        except Exception as e :
            db.session.rollback()
            if("UNIQUE constraint failed" in str(e)):
                result=device.ip+" already exists in the database"
            else:
                result="an exception has occured"
                print(e)

        return {"result":result}
    
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
    device=Device.query.filter_by(ip=request.json['ip']).first()
    device.type = request.json['type'],
    device.model = request.json['model'],
    device.vendor = request.json['vendor'],
    device.serial_number = request.json['serial_number'],
    device.firmware_version = request.json['firmware_version']
    db.session.commit()
    return {"result":SUCCESS}
