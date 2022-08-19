from app import app,jsonify,request
from model import *

@app.route('/api/user',methods=['POST'])
def get_user():
    username = request.json['username']
    user=User.query.filter_by(username=username).first()
    user_schema = UserSchema()
    output = user_schema.dump(user)
    return jsonify(output)

@app.route('/api/users')
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    output = user_schema.dump(users)
    return jsonify(output)

@app.route('/api/users',methods=['POST'])
def add_user():
    ADDED_SUCCESFULLY="1"
    user = User(username = request.json['username'],
    email = request.json['email'],
    password = request.json['password'],
    
    )
    db.session.add(user)
    db.session.commit()
    return {"result":ADDED_SUCCESFULLY}

@app.route('/api/users/edit',methods=['POST'])
def edit_user():
    EDITTED_SUCCESFULLY="1"
    newUser = User(username = request.json['username'],
    email = request.json['email'],
    password = request.json['password'],
    )
    username = request.json['username']
    user=User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    db.session.add(newUser)
    db.session.commit()
    return {"result":EDITTED_SUCCESFULLY}

@app.route('/api/users/delete',methods=['POST'])
def delete_user():
    try:
        DELETED_SUCCESFULLY="2"
        DELETE_ERROR="22"
        username = request.json['username']
        user=User.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
        return {"result":DELETED_SUCCESFULLY}
    except NameError:
        print(NameError)
        return {"result":DELETE_ERROR}

@app.route('/login',methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user=User.query.filter_by(username=username,password=password).first()
    if(user):
        return jsonify({"ok":"1"})
    else:
        return jsonify({"ok":"0"})