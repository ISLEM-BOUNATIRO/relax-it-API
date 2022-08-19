from app import app,jsonify,request
from model import *

@app.route('/api/groups')
def get_groups():
    groups = Group.query.all()
    group_schema = GroupSchema(many=True)
    output = group_schema.dump(groups)
    return jsonify(output)

@app.route('/api/group',methods=['POST'])
def get_group():
    name = request.json['name']
    group = Group.query.filter_by(name=name).first()
    group_schema = GroupSchema()
    output = group_schema.dump(group)
    return jsonify(output)

@app.route('/api/groups',methods=['POST'])
def add_group():
    SUCCESS="1"
    group = Group(name = request.json['name'],
    description = request.json['description'],
    )
    db.session.add(group)
    db.session.commit()
    return {"result":SUCCESS}


@app.route('/api/groups/delete',methods=['POST'])
def delete_group():
    SUCCESS="2"
    name = request.json['name']
    group=Group.query.filter_by(name=name).first()
    db.session.delete(group)
    db.session.commit()
    return {"result":SUCCESS}

@app.route('/api/groups/edit2',methods=['POST'])
def edit_group2():
    SUCCESS="3"
    new_group = Group(name = request.json['name'],
    description = request.json['description'],
    )
    group=Group.query.filter_by(name=new_group.name).first()
    db.session.delete(group)
    db.session.commit()
    db.session.add(new_group)
    db.session.commit()
    return {"result":SUCCESS}

@app.route('/api/groups/edit',methods=['POST'])
def edit_group():
    SUCCESS="3"
    group=Group.query.filter_by(name=request.json['name']).first()
    group.description = request.json['description']
    db.session.commit()
    return {"result":SUCCESS}

@app.route('/api/groups/addmembers',methods=['POST'])
def add_members():
    SUCCESS="4"
    name = request.json['name']
    new_members = request.json['members']
    group=Group.query.filter_by(name=name).first()
    list1=members_to_list(group.members)
    if(group.members==""):
        list1=[]
    list2=members_to_list(new_members)
    all_members=list_to_members(list_union(list1,list2))
    group.members=all_members
    db.session.commit()
    return {"result":SUCCESS,"members":group.members}

@app.route('/api/groups/deletemembers',methods=['POST'])
def delete_members():
    SUCCESS="5"
    name = request.json['name']
    delete_members = request.json['members']
    group=Group.query.filter_by(name=name).first()
    list1=members_to_list(group.members)

    list2=members_to_list(delete_members)
    all_members=list_to_members(list_substraction(list1,list2))
    
    group.members=all_members
    db.session.commit()
    return {"result":SUCCESS}

@app.route('/api/groups/members',methods=['GET'])
def get_members():
    SUCCESS="6"
    name = request.json['name']
    group=Group.query.filter_by(name=name).first()
    return {"result":SUCCESS,"members":group.members}
def members_to_list(members):
    return members.split(",")
    
def list_to_members(list):
    return ",".join(list)

def list_union(list1, list2):
    return list(set(list1) | set(list2))

def list_substraction(list1,list2):
    return list(set(list1) - set(list2))
