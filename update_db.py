from netmiko import ConnectHandler
import regex as re
from app import app,request
from group import *
from device import *


@app.route('/api/populate',methods=['POST'])
def populate():
    ip=request.json['ip']
    group=request.json['group']
    group=Group.query.filter_by(name=group).first()
    if(ip!=""):
        group=Group(members=ip)
    result=""
    if(group):
        hosts=members_to_list(group.members)
    # loop all ip addresses in ip_list
        for ip in hosts:          
            d=get_device_info(ip)
            if d is None:
                result=result+" "+ip+" is unreachable,"

            try:
                db.session.add(d)
                db.session.commit() 
                result=result+" "+ip+" got added\n"
            except Exception as e :
                db.session.rollback()
                if("UNIQUE constraint failed" in str(e)):
                    result=result+" "+ip+" have already been added,"
                else:
                    print(e)

    else:
        return {"error":"group not found"}
    result=result[:-1]
    return {"result":result}

def get_device_info(ipsec):
    cisco = {
                'device_type': 'cisco_ios',
                'ip': ipsec,
                'username': 'islem',  # ssh username
                'password': 'islem',  # ssh password
            }
    try:
        net_connect = ConnectHandler(**cisco)

        # execute show version on router and save output to output object
        output = net_connect.send_command('show version')
        net_connect.disconnect()
        # finding hostname in output using regular expressions
        regex_hostname = re.compile(r'(\S+)\suptime')
        hostname = regex_hostname.findall(output)

        # finding uptime in output using regular expressions
        regex_uptime = re.compile(r'\S+\suptime\sis\s(.+)')
        uptime = regex_uptime.findall(output)

        # finding version in output using regular expressions
        regex_version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)')
        version = regex_version.findall(output)

        # finding serial in output using regular expressions
        regex_serial = re.compile(r'Processor\sboard\sID\s(\S+)')
        serial = regex_serial.findall(output)

        # finding ios image in output using regular expressions
        regex_ios = re.compile(r'System image file is "[^"]*"')
        ios = regex_ios.findall(output)
        ios[0] = ios[0].replace("System image file is ", '')
        ios[0] = ios[0].replace('"', '')

        # finding model in output using regular expressions
        regex_model = re.compile(r'[Cc]isco\s(\S+).*memory.')
        model = regex_model.findall(output)


        device = Device(ip = ipsec,
        firmware_version = version[0],
        model =model[0],
        serial_number = serial[0],
        type = "router or switch",
        vendor = "cisco")
        return device
    except Exception as e:
        if("Common causes of this problem are:" in str(e)):
            print(ipsec+" is unreachable")
        else:
            print(e+" catched in showversion.py line 84")
