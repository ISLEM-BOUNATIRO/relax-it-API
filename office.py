from app import app,jsonify,request
from model import *

@app.route('/api/offices')
def get_offices():
    offices = Office.query.all()
    office_schema = OfficeSchema(many=True)
    output = office_schema.dump(offices)
    return jsonify(output)

@app.route('/api/office',methods=['POST'])
def get_office():
    name = request.json['name']
    office = Office.query.filter_by(name=name).first()
    office_schema = OfficeSchema()
    output = office_schema.dump(office)
    return jsonify(output)

@app.route('/api/offices',methods=['POST'])
def add_office_api():
    SUCCESS="1"
    office = Office(name = request.json['name'],
    office_subnet= request.json['office_subnet'],
    office_class = request.json['office_class'],
    postal_code = request.json['postal_code'],
    wilaya = request.json['wilaya'],
    )
    add_office(office)
    db.session.commit()
    return {"result":SUCCESS}
def add_office(office):
    result=""
    try:
        db.session.add(office)
        db.session.commit()
        result="1"
    except Exception as e :
        db.session.rollback()
        if("UNIQUE constraint failed" in str(e)):
            result=office.office_subnet+" already exists in the database"
        else:
            result="an exception has occured"
            print(e)
    return {"result":result}    


@app.route('/api/offices/delete',methods=['POST'])
def delete_office():
    SUCCESS="2"
    name = request.json['name']
    office=Office.query.filter_by(name=name).first()
    db.session.delete(office)
    db.session.commit()
    return {"result":SUCCESS}

@app.route('/api/offices/edit2',methods=['POST'])
def edit_office2():
    SUCCESS="3"
    new_office = Office(name = request.json['name'],
    office_class = request.json['office_class'],
    postal_code = request.json['postal_code'],
    wilaya = request.json['wilaya'],
    )
    office=Office.query.filter_by(name=new_office.name).first()
    db.session.delete(office)
    db.session.commit()
    db.session.add(new_office)
    db.session.commit()
    return {"result":SUCCESS}

@app.route('/api/offices/edit',methods=['POST'])
def edit_office():
    SUCCESS="3"
    office=Office.query.filter_by(name=request.json['name']).first()
    office.office_class = request.json['office_class']
    office.postal_code = request.json['postal_code']
    office.wilaya = request.json['wilaya']
    db.session.commit()
    return {"result":SUCCESS}

