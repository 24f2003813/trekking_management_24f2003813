from celery import shared_task
from datetime import datetime,timedelta
from models import db, Booking,Trek,User
import requests
import smtplib

@shared_task
def send_daily_reminder():
    today=datetime.utcnow().date()
    tomorrow=today+ timedelta(day=1)

    bookings=(
        db.session.query(Booking).join(Trek).filter(
            Booking.status=='booked',
            Booking.payment_flag == 'paid',
            Trek.start_date.in_([today,tomorrow])
        ).all()
    )

    for b in bookings:
        trekker=User.query.get(b.user_id)
        trek=Trek.query.get(b.trek_id)
        message = f"Hello {trekker.name}, your trek '{trek.name}' starts on {trek.start_date}. "
        send_email(trekker.email, "Trek Reminder" , message)

def send_email(to_email,subject,body):
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login("your_email@gmail.com", "your_password")
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("your_email@gmail.com", to_email, msg)