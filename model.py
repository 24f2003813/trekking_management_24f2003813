

class user(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(70), nullable=False)
    role = db.Column(db.String(50), default='trekker' , nullable=False) #Default role is 'trekker', can be 'admin' or 'trekker'
    status = db.Column(db.String(50), default='active' , nullable=False) # Default status is 'active', can be 'blocked'
    created_at = db.Column(db.DateTime, default=datetime.utcnow , nullable=False)
    contact_number = db.Column(db.String(20) , nullable=False)
    experience = db.Column(db.Integer, nullable=True)
    specialization = db.Column(db.String(100), nullable=True) #"mountain" , "river", "desert" , "forest" 
    emergency_contact_number = db.Column(db.String(20), nullable=True)

class trek(db.Model):
    __tablename__ = 'trek'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text , nullable=False)
    duration = db.Column(db.Integer, nullable=False) 
    difficulty = db.Column(db.String(50), nullable=False) #Difficulty level of the trek, e.g., "easy", "moderate", "hard"
    price = db.Column(db.Float, nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow , nullable=False)
    slots_available = db.Column(db.Integer , nullable=False)
    start_date = db.Column(db.DateTime , nullable=False)
    end_date = db.Column(db.DateTime , nullable=False)
    status = db.Column(db.String(50), default='open' , nullable=False) # can be open , closed , completed, pending ,approved.
    assigned_guide_id = db.Column(db.Integer , db.ForeignKey('user.id')) #Name of the assigned guide for the trek

    staff_assigned=db.relationship('user', backref='treks')
    
class booking(db.Model):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow , nullable=False)
    status = db.Column(db.String(50), default='booked' , nullable=False) #Default booking status is 'booked', can be 'cancelled' or 'completed'
    payment_standing= db.Column(db.String(50), default='pending' , nullable=False) #Default payment status is 'pending', can be 'paid' or 'failed'

    trek_customer=db.relationship('user', backref='bookings', lazy=True)
    trek_booked=db.relationship('trek', backref='bookings'  , lazy=True)

    __table_args__ = (db.UniqueConstraint('user_id', 'trek_id', name='unique_booking'),)

class Badge(db.Model):
    __tablename__ = 'badge'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    criteria_treks = db.Column(db.Integer) #Number of treks required to earn the badge

class user_badge(db.Model):
    __tablename__ = 'user_badge'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    earning_date = db.Column(db.DateTime, default=datetime.utcnow)

    user=db.relationship('user', backref='user_badges' , lazy=True)
    badge=db.relationship('badge', backref='user_badges' , lazy=True)


