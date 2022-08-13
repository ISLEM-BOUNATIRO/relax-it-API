from app import app,jsonify,request
from model import *

@app.route('/api/scripts')
def get_scripts():
    scripts = Script.query.all()
    script_schema = ScriptSchema(many=True)
    output = script_schema.dump(scripts)
    return jsonify(output)
@app.route('/api/script',methods=['POST'])
def get_script():
    name = request.json['name']
    script = Script.query.filter_by(name=name).first()
    script_schema = ScriptSchema()
    output = script_schema.dump(script)
    return jsonify(output)

@app.route('/api/scripts',methods=['POST'])
def add_script():
    SUCCESS="1"
    script = Script(name = request.json['name'],
    content = request.json['content'],
    description = request.json['description'],
    )
    db.session.add(script)
    db.session.commit()
    return {"Result":SUCCESS}


@app.route('/api/scripts/delete',methods=['POST'])
def delete_script():
    SUCCESS="2"
    name = request.json['name']
    script=Script.query.filter_by(name=name).first()
    db.session.delete(script)
    db.session.commit()
    return {"Result":SUCCESS}

@app.route('/api/scripts/edit',methods=['POST'])
def edit_script():
    SUCCESS="3"
    new_script = Script(name = request.json['name'],
    content = request.json['content'],
    description = request.json['description'],
    )
    script=Script.query.filter_by(name=new_script.name).first()
    db.session.delete(script)
    db.session.commit()
    db.session.add(new_script)
    db.session.commit()
    return {"Result":SUCCESS}