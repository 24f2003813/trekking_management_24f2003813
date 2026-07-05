from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from werkzeug.security import generate_password_hash,check_password_hash
import config
from models import db,User,Trek,Booking,Badge,User_Badge
from datetime import datetime

app=Flask(__name__)
CORS(app)

app.config['SECRET_KEY']=config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI']=config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config.JWT_ACCESS_TOKEN_EXPIRES
app.config['DEBUG'] = config.DEBUG

db.init_app(app)

jwt=JWTManager(app)


if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()

        badges = [
        {"name": "Trailblazer", "description": "Complete your first trek", "criteria_treks": 1},
        {"name": "Explorer", "description": "Complete 5 treks", "criteria_treks": 5},
        {"name": "Summit Master", "description": "Complete 10 treks", "criteria_treks": 10}
        ]

        for b in badges:
            if not Badge.query.filter_by(name=b["name"]).first():
                db.session.add(Badge(
                    name=b["name"],
                    description=b["description"],
                    criteria_treks=b["criteria_treks"]
                ))
        db.session.commit()
        
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
    app.run(debug=True)

@app.route('/api/auth/register',methods=['POST'])
def register():
    data=request.get_json()
    print(data)
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
        role="trekker",
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
    present_loginer=User.query.filter_by(email=data['email']).first()

    if not present_loginer or not check_password_hash(present_loginer.password,data['password']):
        return jsonify({"error":"Please enter Valid email or password"}),401
    
    jwt_token= create_access_token(identity=str(present_loginer.id))

    return jsonify({
        "token":jwt_token,
        "role":present_loginer.role,
        "notification": f"Logged In {present_loginer.name}!! Welcome back TrailBuddy"
    }),200

@app.route('/api/admin/dashboard',methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = int(get_jwt_identity())
    present_sessioner = User.query.get(user_id)
    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403

    total_trek=Trek.query.count()
    total_trekker=User.query.filter_by(role='trekker').count()
    total_staff=User.query.filter_by(role='staff').count()
    total_booking=Booking.query.count()

    latest_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    recent_list = [
        {
            "id": b.id,
            "trek_name": b.booking_trek.name if b.booking_trek else None,
            "user_name": b.booking_user.name if b.booking_user else None,
            "status": b.status,
            "payment_flag": b.payment_flag,
            "booking_date": b.booking_date.strftime("%Y-%m-%d %H:%M:%S")
        }
        for b in latest_bookings
    ]

    return jsonify({
        "message": "Dashboard summary fetched successfully",
        "summary": {
            "total_treks": total_trek,
            "total_users": total_trekker,
            "total_staff": total_staff,
            "total_bookings": total_booking
        },
        "recent_bookings": recent_list
    }), 200

@app.route('/api/admin/treks',methods=['POST','GET'])
@jwt_required()
def map_and_add_trek():
    user_id = int(get_jwt_identity())

    present_sessioner = User.query.get(user_id)

    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    if request.method == 'GET':
        search=request.args.get('search')
        query=Trek.query
        if search:
            query=Trek.query.filter(
                (Trek.name.ilike(f"%{search}%")) |
                (Trek.location.ilike(f"%{search}%")) |
                (Trek.difficulty.ilike(f"%{search}%"))
            )
        treks=query.all()
        treks_mapping=[
            {'id': trek.id,
             'name':trek.name,
             'location':trek.location,
             'difficulty':trek.difficulty,
             'status':trek.status,
             'description':trek.description,
             'duration':trek.duration,
             'price':trek.price,
             'slots_available':trek.slots_available,
             'start_date': trek.start_date.isoformat(),
             'end_date': trek.end_date.isoformat(),
             'max_trekker': trek.max_trekker,
             'assigned_guide_id': trek.assigned_guide_id}

            for trek in treks
        ]
        return jsonify(treks_mapping),200
    
    if request.method == 'POST':
        data = request.get_json()
        required_fields=['name','location','description','duration','difficulty','price','slots_available','start_date','end_date']

        for field in required_fields:
            if not data.get(field):
                return jsonify({"error":f"{field} is required"}),400

        new_trek_route=Trek(
            name=data['name'],
            location=data['location'],
            description=data['description'],
            duration=data['duration'],
            price=data['price'],
            slots_available=data['slots_available'],
            start_date=datetime.fromisoformat(data['start_date']),
            end_date=datetime.fromisoformat(data['end_date']),
            difficulty=data['difficulty'],
            status=data.get('status','open'),
            max_trekker=data.get('max_trekker',15),
            assigned_guide_id=data.get('assigned_guide_id')
        )
        db.session.add(new_trek_route)
        db.session.commit()

        return jsonify({"message":"Trek added successfully admin!!",
                        "notification":f"Trek for {new_trek_route.location} added to the trek list"}),201

@app.route('/api/admin/treks/<int:trek_id>',methods=['PUT','DELETE'])
@jwt_required()
def update_delete_trek(trek_id):
    user_id = int(get_jwt_identity())

    present_sessioner = User.query.get(user_id)

    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    trek=Trek.query.get(trek_id)
    if not trek:
        return jsonify({"error":"Sorry No trek found"}),404
    
    if request.method == 'PUT':
        data=request.get_json()
        trek.name=data.get('name',trek.name)
        trek.location=data.get('location',trek.location)
        trek.difficulty=data.get('difficulty',trek.difficulty)

        valid_statuses = ["open", "full", "completed", "cancelled"]
        if data.get('status') in valid_statuses:
            trek.status = data['status']

        if 'assigned_guide_id' in data:
            staff=User.query.filter_by(id=data['assigned_guide_id'],role='staff').first()
            if not staff:
                return jsonify({"error":"Invalid staff ID"})
            trek.assigned_guide_id=staff.id

        db.session.commit()
        return jsonify({"message":"Trek details are updated successfully",
                        "notification":f"Trek '{trek.name}' is updated."}),200

    if request.method=='DELETE':
        db.session.delete(trek)
        db.session.commit()
        return jsonify({"message":"Trek is deleted",
                        "notification":f"Trek '{trek.name}' is removed"}),200
    
@app.route('/api/admin/eligible_guides',methods=['GET'])
@jwt_required()
def eligibility_check():
    user_id = int(get_jwt_identity())

    present_sessioner = User.query.get(user_id)

    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    staff_members=User.query.filter_by(role='staff').all()
    eligible=[]

    for staff in staff_members:
        active_treks_count=Trek.query.filter(Trek.assigned_guide_id == staff.id,
            Trek.status.in_(["open","completed"])  # active status
        ).count()

        if active_treks_count <3:
            eligible.append({
                "id":staff.id,
                "name":staff.name,
                "specialization":staff.specialization
            })
    return jsonify(eligible),200


@app.route('/api/admin/treks/<int:trek_id>/assign_guide',methods=['PUT'])
@jwt_required()
def assign_guide(trek_id):
    user_id = int(get_jwt_identity())

    present_sessioner = User.query.get(user_id)

    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    data=request.get_json()
    if not data.get('guide_id'):
        return jsonify({"error":"Guide ID is required"}),400

    trek=Trek.query.get(trek_id)
    guide=User.query.filter_by(id=data['guide_id'],role='staff').first()

    if not trek:
        return jsonify({"error":"Sorry, Trek not found"})
    
    if not guide:
        return jsonify({"error":"Sorry, Staff id not found "})
    
    active_trek_count=Trek.query.filter(
        Trek.assigned_guide_id == guide.id,
        Trek.status.in_(['open','completed'])
    ).count()

    if active_trek_count >=3 and not data.get('force'):
        return jsonify({"error":f"Guide {guide.name} already has 3 active treks"})
    
    if trek.assigned_guide_id and trek.assigned_guide_id != guide.id and not data.get('force'):
        return jsonify({"warning":f"Trek '{trek.name}' already has a guide assigned (ID {trek.assigned_guide_id})."}),409
    
    trek.assigned_guide_id=guide.id
    db.session.commit()

    return jsonify({"message":f"Guide is assigned sucessfully to the {trek.name} trek",
                    "notification":f"Guide '{guide.name}' assigned to the {trek.name}"}),200

@app.route('/api/admin/staff',methods=['GET','POST'])
@jwt_required()
def manage_staff():
    user_id = int(get_jwt_identity())
    present_sessioner = User.query.get(user_id)
    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403

    if request.method == 'GET':
        search = request.args.get('search')  
        query = User.query.filter_by(role='staff')
        if search:
            query = query.filter(
                (User.name.ilike(f"%{search}%")) |
                (User.experience.ilike(f"%{search}%")) |
                (User.specialization.ilike(f"%{search}%"))
            )
        staffs = query.all()
        staff_list=[
            {'id':staff.id,'name':staff.name,'email':staff.email,'specialization':staff.specialization,'status':staff.status}
            for staff in staffs
        ]
        return jsonify(staff_list),200
    
    if request.method == 'POST':
        data= request.get_json()
        print("Received payload:", data) 
        if not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({"error":"Name , email and password are required to mention"}),400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error":"Staff member is already registered"}),400
        
        pass_hashed=generate_password_hash(data['password'])
        new_staff_member= User(
            name=data['name'],
            email=data['email'],
            password=pass_hashed,
            role='staff',
            specialization=data.get('specialization','General'),
            contact_number=data['contact_number'],
            experience=data.get('experience')
        )
        db.session.add(new_staff_member)
        db.session.commit()

        return jsonify({"message":"New helper added to our team",
                       "notification":f"Staff '{new_staff_member.name}' created"
                       }),200

@app.route('/api/admin/staff/<int:staff_id>',methods=['PUT','DELETE'])
@jwt_required()
def alter_staff_detail(staff_id):
    user_id = int(get_jwt_identity())

    present_sessioner = User.query.get(user_id)

    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    staff=User.query.filter_by(id=staff_id,role='staff').first()
    if not staff:
        return jsonify({"error":"This staff member is not found"}),404
    
    if request.method == 'PUT':
        data=request.get_json()
        staff.name=data.get('name',staff.name)
        staff.email =data.get('email',staff.email)
        staff.specialization = data.get('specialization', staff.specialization)
        staff.status = data.get('status', staff.status)

        if staff.status.lower()=='block':
            assigned_trek=Trek.query.filter_by(assigned_guide_id=staff.id).all()
            for trek in assigned_trek:
                trek.assigned_guide_id=None
        db.session.commit()
        return jsonify({"message":"Staff member detail is updated sucessfully",
                        "notification":f"Staff '{staff.name}' details updated"}),200

    if request.method == 'DELETE':

        assigned_treks = Trek.query.filter_by(assigned_guide_id=staff.id).all()
        for trek in assigned_treks:
            trek.assigned_guide_id = None

        db.session.delete(staff)
        db.session.commit()
        return jsonify({
            "message":"Staff Member deleted Sucessfully",
            "notification":f"Staff '{staff.name}' removed"
        }),200
    
@app.route('/api/admin/users',methods=['GET'])
@jwt_required()
def all_users():
    user_id = int(get_jwt_identity())
    present_sessioner = User.query.get(user_id)
    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    search_query=request.args.get('search')
    query=User.query.filter_by(role='trekker')
    if search_query:
        query=query.filter(User.name.ilike(f"%{search_query}%"))

    users=User.query.filter_by(role='trekker').all()
    trekker_list=[
        {'id':trekker.id,'name':trekker.name,'email':trekker.email,'contact_number':trekker.contact_number,'status':trekker.status}
        for trekker in users
    ]
    return jsonify(trekker_list),200

@app.route('/api/admin/users/<int:trekker_id>/status',methods=['PUT','DELETE'])
@jwt_required()
def manage_trekker_status(trekker_id):
    user_id = int(get_jwt_identity())
    present_sessioner = User.query.get(user_id)
    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    trekker=User.query.filter_by(id=trekker_id,role='trekker').first()
    if not trekker:
        return jsonify({"error":"This staff member is not found"}),404
    
    if request.method == 'PUT':
        data= request.get_json()
        if not data.get('status'):
            return jsonify({"error":"Status is required"}),400
        
        trekker.status=data['status']

        if trekker.status.lower() == "blocked":
            active_bookings = Booking.query.filter_by(user_id=trekker.id, status="booked").all()
            for b in active_bookings:
                b.status = "cancelled"

        db.session.commit()
        return jsonify({"message":"Trekker Status is updated sucessfully",
                        "notification":f"Trekker '{trekker.name}' updated status is '{trekker.status}'"}),200
    
    if request.method =='DELETE':

        active_bookings = Booking.query.filter_by(user_id=trekker.id, status="booked").all()
        for b in active_bookings:
            b.status = "cancelled"

        db.session.delete(trekker)
        db.session.commit()
        return jsonify({"message":"Trekker Data is deleted sucessfully",
                        "notification":f"Trekker '{trekker.name}' is deleted"}),200
    

@app.route('/api/admin/bookings',methods=['GET'])
@jwt_required()
def listing_bookings():
    user_id = int(get_jwt_identity())
    present_sessioner = User.query.get(user_id)
    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    bookings=Booking.query.all()
    listing=[
        {
            'id':booking.id,
            'trek_id':booking.trek_id,
            'trek_name':booking.booking_trek.name if booking.booking_trek else None,
            'user_id':booking.user_id,
            'user_name':booking.booking_user.name if booking.booking_user else None,
            'status':booking.status,
            'created_at':booking.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for booking in bookings
    ]
    return jsonify(listing),200

def check_and_assign_badge(user_id):
    completed_trek_count=Booking.query.filter_by(user_id=user_id, status="completed").count()
    badges = Badge.query.all()

    for badge in badges:
        # If user has enough treks for this badge
        if completed_trek_count >= badge.criteria_treks:
            # Check if already earned
            existing = User_Badge.query.filter_by(user_id=user_id, badge_id=badge.id).first()
            if not existing:
                new_badge = User_Badge(user_id=user_id, badge_id=badge.id)
                db.session.add(new_badge)
    db.session.commit()

@app.route('/api/admin/bookings/<int:booking_id>/status',methods=['PUT','DELETE'])
@jwt_required()
def manage_booking(booking_id):
    user_id = int(get_jwt_identity())
    present_sessioner = User.query.get(user_id)
    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    booking=Booking.query.get(booking_id)
    if not booking:
        return jsonify({"error":"Booking not found"})
    
    if request.method=='PUT':
        data=request.get_json()
        if 'status' not in data:
            return jsonify({"error":"Status is required"})
        
        if data['status'] not in ['cancelled','completed',]:
            return jsonify({"error": "Please enter valid status"})
        
        booking.status=data['status']
        db.session.commit()

        if booking.status == 'completed':
            check_and_assign_badge(booking.user_id)

        return jsonify({"message":"Status updated sucessfully ",
                        "notification":f"Booking id {booking.id} marked as {booking.status}"}),200
    
    if request.method=='DELETE':
        db.session.delete(booking)
        db.session.commit()
        return jsonify({
            "message": "Booking deleted successfully",
            "notification": f"Booking {booking.id} removed."
        }), 200

@app.route('/api/bookings/<int:booking_id>/pay',methods=['PUT'])
@jwt_required()
def pay_booking(booking_id):
    user_id = int(get_jwt_identity())
    present_sessioner = User.query.get(user_id)
    if present_sessioner.role != "admin":
        return jsonify({"error": "Sorry you cannot access this page"}), 403
    
    booking=Booking.query.get(booking_id)
    if not booking or booking.user_id != present_sessioner.id:
        return jsonify({"error":"Booking not found"}),404
    
    data=request.get_json()
    if 'payment_flag' not in data or data["payment_flag"] not in ["paid","failed"]:
        return jsonify({"error":"Payment flag must be 'paid' or 'failed'"}),400
    
    booking.payment_flag = data["payment_flag"]
    db.session.commit()

    return jsonify({"message":"Payment status updated",
                    "notification":f"Booking {booking.id} marked as {booking.payment_flag}."}),200


@app.route('/api/staff/dashboard', methods=['GET'])
@jwt_required()
def staff_dashboard():
    user_id = int(get_jwt_identity())
    present_sessioner = User.query.get(user_id)
    if present_sessioner.role != "staff":
        return jsonify({"error": "Sorry you cannot access this page"}), 403

    assigned_treks = Trek.query.filter_by(assigned_guide_id=present_sessioner.id).all()
    trek_count = len(assigned_treks)

    participant_total = sum(
        Booking.query.filter_by(trek_id=trek.id, status="booked").count()
        for trek in assigned_treks
    )

    return jsonify({
        "overview": {
            "treks_assigned": trek_count,
            "participants_total": participant_total
        },
        "trek_details": [
            {
                "trek_id": trek.id,
                "trek_name": trek.name,
                "trek_status": trek.status,
                "participant_count": Booking.query.filter_by(trek_id=trek.id, status="booked").count()
            }
            for trek in assigned_treks
        ]
    }), 200

@app.route('/api/staff/treks/<int:trek_id>/slots_capacity',methods=['PUT'])
@jwt_required()
def update_trek_slots(trek_id):
    staff_id=int(get_jwt_identity())
    staff = User.query.get(staff_id)
    if staff.role != 'staff':
        return jsonify({"error":"Sorry you cannot access this page"}),403
    
    trek=Trek.query.get(trek_id)
    if not trek or trek.assigned_guide_id != staff.id:
        return jsonify({"error":"Trek not found or this trek is not assigned to you"}),404
    
    data=request.get_json()
    if not data.get("max_trekker"):
        return jsonify({"error":"Maximum Trekker limit is required"}),400
    
    trek.max_trekker=data['max_trekker']
    db.session.commit()
    return jsonify({"message":f"Capacity of trek '{trek.name}' to {trek.max_trekker} "})

@app.route('/api/staff/treks/<int:trek_id>/status',methods=['PUT'])
@jwt_required()
def update_status(trek_id):
    staff_id=int(get_jwt_identity())
    staff=User.query.get(staff_id)
    if staff.role != 'staff':
        return jsonify({"error":"Sorry you cannot access the page"}),403
    
    trek=Trek.query.get(trek_id)
    if not trek or trek.assigned_guide_id != staff.id:
        return jsonify({"error":"Trek not found or trek is not assigned to you"}),400
    
    data=request.get_json()
    valid_status=['open','cancelled','full','completed']
    if data.get("status") not in valid_status:
        return jsonify({"error":"Please provide valid status"}),400
    
    trek.status=data['status']
    db.session.commit()
    return jsonify({"message":f"Status updated to '{trek.status}'"})

@app.route('/api/staff/trek/<int:trek_id>/participants',methods=["GET"])
@jwt_required()
def trek_participants(trek_id):
    staff_id=int(get_jwt_identity())
    staff=User.query.get(staff_id)
    if staff.role != 'staff':
        return jsonify({"error":"Sorry you cannot access the page"}),403
    
    trek=Trek.query.get(trek_id)
    if not trek or trek.assigned_guide_id != staff.id:
        return jsonify({"error":"Trek not found or trek is not assigned to you"}),400
    
    participants=Booking.query.filter_by(trek_id=trek.id,status='booked').all()
    participants_list=[
        {
            "id":b.user_id,
            "name":b.booking_user.name,
            "email":b.booking_user.email,
            "contact_number":b.booking_user.contact_number,
            "trek":b.booking_trek.name
        }
        for b in participants
    ]
    return jsonify(participants_list),200

@app.route('/api/user/dashboard',methods=["GET"])
@jwt_required()
def user_dashboard():
    trekker_id=int(get_jwt_identity())
    trekker=User.query.get(trekker_id)
    if not trekker or trekker.role !='trekker':
        return jsonify({"error":"Sorry you cannot access this page"}),403
    
    name_search=request.args.get('name')
    location_search=request.args.get('location')
    difficulty_search=request.args.get('difficulty')
    trek_separation=Trek.query.filter_by(status='open')
    if name_search:
        trek_separation=trek_separation.filter(Trek.name.ilike(f"%{name_search}%"))
    if location_search:
        trek_separation=trek_separation.filter(Trek.location.ilike(f"%{location_search}%"))
    if difficulty_search:
        trek_separation=trek_separation.filter(Trek.difficulty.ilike(f"%{difficulty_search}%"))
    
    available_trek=[]
    treks=Trek.query.filter_by(status='open').all()
    for trek in treks:
        booked_slot_count=Booking.query.filter_by(trek_id=trek.id,status='booked').count()
        slots_available=trek.max_trekker - booked_slot_count
        if slots_available>0:
            available_trek.append({
                "id": trek.id,
                "name": trek.name,
                "location": trek.location,
                "difficulty": trek.difficulty,
                "status": trek.status,
                "max_trekker": trek.max_trekker,
                "slots_available": slots_available
            })

    bookings=Booking.query.filter_by(user_id=trekker.id).all()
    booked_trek=[
        {
            "Booking_id":b.id,
            "trek_id":b.trek_id,
            "trek_name":b.booking_trek.name,
            "status":b.status,
            "booking_date":b.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for b in bookings if b.status=='booked'
    ]

    history=[
        {
            "booking_id": b.id,
            "trek_id": b.trek_id,
            "trek_name": b.booking_trek.name if b.booking_trek else None,
            "status": b.status,
            "booking_date": b.booking_date.strftime("%Y-%m-%d %H:%M:%S")

        }
        for b in bookings if b.status in ['completed','cancelled']
    ]
    return jsonify({
        "available_treks": available_trek,
        "booked_treks": booked_trek,
        "history": history
    }),200

@app.route('/api/user/booking_cancel/<int:booking_id>',methods=['PUT'])
@jwt_required()
def cancel_booking(booking_id):
    trekker_id=int(get_jwt_identity())
    trekker=User.query.get(booking_id)
    if trekker.role != 'trekker':
        return jsonify({"error":"Sorry you cannot access this page"}),403
    
    booking=Booking.query.get(booking_id)
    if not booking or booking.user_id != trekker.id:
        return jsonify({"error": "Booking not found"}), 404

    if booking.status != "booked":
        return jsonify({"error": "Only active bookings can be cancelled"}), 400
    
    booking.status='cancelled'
    db.session.commit()
    return jsonify({"message":"Booking cancelled sucessfully",
                    "notification":f"Booking {booking.booking_trek.name} cancelled sucessfully"}),200

@app.route('/api/user/edit_profile',methods=['GET','PUT'])
@jwt_required()
def edit_profile():
    trekker_id=int(get_jwt_identity())
    trekker=User.query.get(trekker_id)

    if not trekker or trekker.role != 'role':
        return jsonify({"error":"Sorry you cannot access this page"}),403
    
    if request.method == 'GET':
        return jsonify({
            "id": trekker.id,
            "name": trekker.name,
            "email": trekker.email,
            "contact_number": trekker.contact_number,
            "emergency_contact_number": trekker.emergency_contact_number,
            "status": trekker.status
        }),200

    if request.method == 'PUT':
        data = request.get_json()
        trekker.name = data.get("name", trekker.name)
        trekker.email = data.get("email", trekker.email)
        trekker.contact_number = data.get("contact_number", trekker.contact_number)
        trekker.emergency_contact_number = data.get("emergency_contact_number", trekker.emergency_contact_number)

        db.session.commit()
        return jsonify({
            "message":"Profile updated successfully",
            "notification":f"Trekker '{trekker.name}' profile updated"
        }),200
    
@app.route('/api/user/bookings', methods=['POST'])
@jwt_required()
def book_trek():
    trekker_id = int(get_jwt_identity())
    trekker = User.query.get(trekker_id)
    if not trekker or trekker.role != 'trekker':
        return jsonify({"error":"Unauthorized"}),403

    data = request.get_json()
    trek_id = data.get("trek_id")
    trek = Trek.query.get(trek_id)

    if not trek or trek.status != "open":
        return jsonify({"error":"Trek not available for booking"}),400

    existing_booking = Booking.query.filter_by(
        user_id=trekker.id, trek_id=trek.id, status="booked"
    ).first()
    if existing_booking:
        return jsonify({"error":"You have already booked this trek"}),400

    booked_count = Booking.query.filter_by(trek_id=trek.id, status="booked").count()
    if booked_count >= trek.max_trekker:
        return jsonify({"error":"No slots available"}),400

    new_booking = Booking(
        user_id=trekker.id,
        trek_id=trek.id,
        status="booked",
        booking_date=datetime.now()
    )
    db.session.add(new_booking)
    db.session.commit()

    return jsonify({
        "message":"Trek booked successfully",
        "notification":f"Trek '{trek.name}' booked by {trekker.name}"
    }),201
