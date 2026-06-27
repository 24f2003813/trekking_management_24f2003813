from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from werkzeug.security import generate_password_hash,check_password_hash
import config
from models import db,User,Trek,Booking,Badge,User_Badge
from datetime import datetime

app=Flask(__name__)

app.config['SECRET_KEY']=config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']=config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config['DEBUG'] = config.DEBUG

db.init_app(app)
CORS(app)
jwt=JWTManager(app)
    
with app.app_context():
    db.create_all()
    if not User.query.filter_by(role='admin').first():
        admin=User(
            name="Admin1",
            email="admin@TrekkingManagement.com",
            password=generate_password_hash("admin2005"),
            role="admin",
            contact_number="7078954646"
        )
        db.session.add(admin)
        db.session.commit()

@app.route('/api/auth/register',methods=['POST'])
def register():
    data=request.get_json()
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error":"Name,email,password are required"}),400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error":"Email already registered"}),400
    
    if len(data['password'])<6:
        return jsonify({"error":"password must be atleast 6 charachters"}),400
    
    pass_hashed=generate_password_hash(data['password'])

    new_trekker=User(
        name=data['name'],
        email=data['email'],
        password=pass_hashed,
        contact_number=data.get('contact_number','None')
    )

    db.session.add(new_trekker)
    db.session.commit()

    return jsonify({
        "message":"Registration Done!! Escape the concrete. Explore the wild.",
        "notification":f"Welcome {new_trekker.name}!! Let's turn maps into memories." 
    }),201

@app.route('/api/auth/login',methods=['POST'])
def login():
    data= request.get_json()
    trekker=User.query.filter_by(email=data['email']).first()

    if not trekker or not check_password_hash(trekker.password,data['password']):
        return jsonify({"error":"Please enter Valid email or password"}),401
    
    jwt_token=create_access_token(identity={"id":trekker.id,"role":trekker.role})

    return jsonify({
        "token":jwt_token,
        "role":trekker.role,
        "notification": f"Logged In {trekker.name}!! Welcome back TrailBuddy"
    }),200

@app.route('/api/admin/treks',methods=['POST','GET'])
@jwt_required()
def map_and_add_trek():
    present_sessioner=get_jwt_identity()
    if present_sessioner['role'] != 'admin':
        return jsonify({"error":"Sorry you cannot access"}),403
    
    if request.method == 'GET':
        treks=Trek.query.all()
        treks_mapping=[
            {'id': trek.id,'name':trek.name,'location':trek.location,'difficulty':trek.difficulty,'status':trek.status}
            for trek in treks
        ]
        return jsonify(treks_mapping),200
    
    if request.method == 'POST':
        data = request.get_json()
        if not data.get('name') or not data.get('location') or not data.get('difficulty'):
            return jsonify({"error":"Name,location and difficulty are required to mention for best results"}),400

        new_trek_route=Trek(
            name=data['name'],
            location=data['location'],
            difficulty=data['difficulty'],
            status="open"
        )
        db.session.add(new_trek_route)
        db.session.commit()

        return jsonify({"message":"Trek added successfully admin!!",
                        "notification":f"Trek for {new_trek_route.location} added to the trek list"}),201

@app.route('/api/admin/treks/<int:trek_id>',methods=['PUT','DELETE'])
@jwt_required()
def update_delete_trek(trek_id):
    present_sessioner=get_jwt_identity()
    if present_sessioner['role'] != 'admin':
        return jsonify({"error":"Sorry you cannot access this page"}),403
    
    trek=Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error":"Sorry No trek found"}),404
    
    if request.method == 'PUT':
        data=request.get_json()
        trek.name=data.get('name',trek.name)
        trek.location=data.get('location',trek.location)
        trek.difficulty=data.get('difficulty',trek.difficulty)
        trek.status=data.get('status',trek.status)

        db.session.commit()
        return jsonify({"message":"Trek details are updated successfully"}),200

    if request.method=='DELETE':
        db.session.delete(trek)
        db.session.commit()
        return jsonify({"error":"Trek is deleted"}),200




if __name__ == "__main__":
    app.run()
