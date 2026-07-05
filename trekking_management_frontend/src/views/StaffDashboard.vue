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