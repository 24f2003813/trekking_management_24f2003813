from celery import shared_task
from datetime import datetime,timedelta
from models import db, Booking,Trek,User
from sqlalchemy import func
from app import app
import requests
import pytz
import smtplib

@shared_task
def send_daily_reminders():
    with app.app_context():
        ist=pytz.timezone("Asia/Kolkata")
        today=datetime.now(ist).date()

        bookings=(
            db.session.query(Booking).join(Trek).filter(
                Booking.status=='booked',
                Booking.payment_flag == 'paid',
                func.date(Trek.start_date )<= today + timedelta(days=3),
                func.date(Trek.start_date )> today
            ).all()
        )
        print(f"Found {len(bookings)} bookings for reminders on {today}")
        for b in bookings:
            trekker=User.query.get(b.user_id)
            trek=Trek.query.get(b.trek_id)
            print(f"Matched trek '{trek.name}' ({trek.start_date}) for {trekker.name} <{trekker.email}>")
            message = (f"Hello {trekker.name},\n\n"
                        f"This is a reminder that your trek '{trek.name}' "
                        f"starts on {trek.start_date.strftime('%A, %d %B %Y at %I:%M %p')}.\n\n"
                        "Please be prepared and arrive on time.\n\n"
                        "Best regards,\nTrekking Management System")
            send_email(trekker.email, "Trek Reminder", message)
            print(f"Reminder sent to: {trekker.name} <{trekker.email}> for trek '{trek.name}'")

def send_email(to_email,subject,body):
    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login("trekkingbuddy744@gmail.com", "aokekqdgtpatplsn")
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("trekkingbuddy744@gmail.com", to_email, msg)

@shared_task
def mark_completed_treks():
    with app.app_context():
        today = datetime.utcnow().date()
        treks = Trek.query.filter(Trek.status == "open").all()
        for trek in treks:
            if trek.start_date.date() < today:
                trek.status = "completed"
        db.session.commit()

# send_daily_reminders.delay()
# send_email("varshneysaanjhi@gmail.com", "Test Reminder", "This is a test reminder email.")

# mark_completed_treks.delay()

