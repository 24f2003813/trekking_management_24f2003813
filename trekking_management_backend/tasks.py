from extensions import app, db,celery
from models import Booking, Trek, User
from datetime import datetime,timedelta
from sqlalchemy import func
import requests
import io
import csv
from email.mime.text import MIMEText
import pytz,os
import smtplib

@celery.task
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

def send_email(to_email,subject,body,html=False):
    if html:
        msg = MIMEText(body, "html")
    else:
        msg = MIMEText(body, "plain")  

    msg["Subject"] = subject
    msg["From"] = "trekkingbuddy744@gmail.com"
    msg["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com",587) as server:
        server.starttls()
        server.login("trekkingbuddy744@gmail.com", "aokekqdgtpatplsn")
        server.send_message(msg)

@celery.task
def mark_completed_treks():
    with app.app_context():
        today = datetime.utcnow().date()
        treks = Trek.query.filter(Trek.status == "open").all()
        for trek in treks:
            if trek.start_date.date() < today:
                trek.status = "completed"
        db.session.commit()


def generate_monthly_report():
    with app.app_context():
        ist=pytz.timezone("Asia/Kolkata")
        today=datetime.now(ist).date()
        first_day_last_month = (today.replace(day=1)-timedelta(days=1)).replace(day=1)
        last_day_last_month=today.replace(day=1)-timedelta(days=1)

        treks_count = (
            db.session.query(func.count(Trek.id)).filter(
                func.date(Trek.start_date) >= first_day_last_month,
                func.date(Trek.end_date) <= last_day_last_month
            ).scalar()
        )

        TrekkerCount=(
            db.session.query(func.count(Booking.id)).join(Trek)
            .join(User,Booking.user_id == User.id)
            .filter(
                Booking.status == 'booked',
                Booking.payment_flag == 'paid',
                func.date(Trek.start_date) >= first_day_last_month,
                func.date(Trek.start_date) <= last_day_last_month,
                User.role == 'trekker'
            ).scalar()
        )

        popular_treks = (
            db.session.query(
                Trek.name, func.count(Booking.id).label("participants")
            )
            .join(Booking)
            .join(User, Booking.user_id == User.id)
            .filter(
                Booking.status == 'booked',
                Booking.payment_flag == 'paid',
                func.date(Trek.start_date) >= first_day_last_month,
                func.date(Trek.start_date) <= last_day_last_month,
                User.role == 'trekker'
            )
            .group_by(Trek.name)
            .order_by(func.count(Booking.id).desc())
            .limit(3)
            .all()
        )

        return treks_count, TrekkerCount, popular_treks

def build_report(treks_count, users_count, popular_treks):
    with app.app_context():
        popular_html = "".join(
            f"<li>{name} ({count} participants)</li>" for name, count in popular_treks
        )
        html = f"""
            <html>
            <body>
                <h2>Monthly Trekking Activity Report</h2>
                <p><b>Treks conducted:</b> {treks_count}</p>
                <p><b>Users participated:</b> {users_count}</p>
                <p><b>Popular treks:</b></p>
                <ul>{popular_html}</ul>
                <p>Generated on {datetime.utcnow().strftime('%Y-%m-%d')}</p>
            </body>
            </html>
        """
        return html

@celery.task
def send_monthly_report():
    with app.app_context():
        TrekCount,TrekkerCount,PopularTrek = generate_monthly_report()
        html_report = build_report(TrekCount,TrekkerCount,PopularTrek)

        send_email(
            "24f2003813@ds.study.iitm.ac.in", 
            "Monthly Trekking Activity Report",
            html_report,
            html=True
        )

@celery.task
def export_booking_history(user_id, user_email):
    with app.app_context():
        bookings = (
            db.session.query(Booking, Trek)
            .join(Trek, Booking.trek_id == Trek.id)
            .filter(Booking.user_id == user_id)
            .all()
        )
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["User ID", "Trek Name", "Location", 
                         "Booking Status", "Start Date", "End Date"])
        for booking, trek in bookings:
            writer.writerow([
                booking.user_id,
                trek.name,
                trek.location,
                booking.status,
                trek.start_date.strftime("%Y-%m-%d"),
                trek.end_date.strftime("%Y-%m-%d")
            ])

        csv_data = output.getvalue()
        output.close()

        filename = f"booking_history_{user_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
        os.makedirs("exports", exist_ok=True)
        filepath = f"exports/{filename}"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(csv_data)

        send_email(
            user_email,
            "Your Trekking Booking History Export",
            f"Hello,\n\nYour booking history has been exported.\nYou can download it here: {filepath}\n\nBest,\nTrekking Management System",
            html=False
        )
send_daily_reminders.delay()
send_email("varshneysaanjhi@gmail.com", "Test Reminder", "This is a test reminder email.")
mark_completed_treks.delay()