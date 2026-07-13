# Trekking Management System

## Project Overview

The Trekking Management System is a web-based application designed to simplify the management of trekking activities for both trekkers and administrators. The application is developed using Flask for the backend, Vue.js for the frontend, and SQLAlchemy with SQLite for database management. It provides secure role-based access using JWT authentication, ensuring that administrators and trekkers can access features relevant to their roles.

The platform allows trekkers to explore available treks, make bookings, complete payments, view booking history, manage their profiles, and earn badges based on completed treks. Administrators can create and manage treks, assign guides, monitor bookings, update trek statuses, and manage user accounts. The system also incorporates Redis, Celery, and Celery Beat to execute background tasks such as sending reminder emails, generating monthly activity reports, exporting booking history as CSV files, and automatically updating trek statuses. Overall, the application streamlines trek management by improving organization, automation, and user experience.

---

## Technology Stack

### Backend
- Flask
- SQLAlchemy
- Flask-JWT-Extended
- Flask-Mail
- Flask-Caching

### Frontend
- Vue.js 3
- Vue Router
- Axios
- Bootstrap 5

### Database
- SQLite

### Background Services
- Redis
- Celery
- Celery Beat

### Documentation
- OpenAPI (YAML)

---

## Features

### Authentication
- Secure user registration and login
- JWT-based authentication
- Role-based access control

### Trek Management
- Create, update, and delete treks
- Manage trek details and available slots
- Assign guides to treks

### Booking Management
- Browse available treks
- Book treks
- Prevent duplicate bookings
- Track booking and payment status

### User Profile
- Update personal information
- Store emergency contact details
- View trekking experience

### Booking History
- View complete booking history
- Export booking history as CSV

### Badge System
- Automatic badge allocation based on completed treks
- Display earned badges

### Email Notifications
- Daily trek reminders
- Monthly activity reports
- Booking history export notifications

### Background Tasks
- Automated reminder emails
- Monthly report generation
- Trek status updates
- CSV export generation using Celery

### REST API
- RESTful APIs for frontend communication
- API documentation using OpenAPI (YAML)

---

## Project Structure

```text
24f2003813_Trekking_Management_System/
├── README.md
├── trekking_management_backend
│   ├── api.yaml
│   ├── app.py
│   ├── config.py
│   ├── dump.rdb
│   ├── exports
│   │   ├── booking_history_4_20260711213132.csv
│   │   ├── booking_history_7_20260711212610.csv
│   │   └── booking_history_7_20260712124150.csv
│   ├── extensions.py
│   ├── instance
│   │   └── database.db
│   ├── models.py
│   ├── requirements.txt
│   └── tasks.py
└── trekking_management_frontend
    ├── README.md
    ├── index.html
    ├── jsconfig.json
    ├── package-lock.json
    ├── package.json
    ├── public
    │   └── favicon.ico
    ├── src
    │   ├── App.vue
    │   ├── assets
    │   ├── components
    │   ├── main.js
    │   ├── router
    │   │   └── index.js
    │   └── views
    │       ├── AdminBooking.vue
    │       ├── AdminDashboard.vue
    │       ├── AdminStaff.vue
    │       ├── AdminStaffAdd.vue
    │       ├── AdminTrekAdd.vue
    │       ├── AdminTrekEdit.vue
    │       ├── AdminTrekker.vue
    │       ├── AdminTreks.vue
    │       ├── LandingView.vue
    │       ├── Login.vue
    │       ├── Logout.vue
    │       ├── Register.vue
    │       ├── StaffDashboard.vue
    │       ├── StaffParticipants.vue
    │       ├── StaffProfile.vue
    │       ├── StaffTrek.vue
    │       ├── TrekDetails.vue
    │       ├── TrekkerBadge.vue
    │       ├── TrekkerDashboard.vue
    │       ├── TrekkerHistory.vue
    │       ├── TrekkerProfile.vue
    │       └── TrekkerTrek.vue
    └── vite.config.js
```

---

## Installation

### Clone the Repository

```bash
git clone <repository_url>
cd trekking_management_system
```

### Backend Setup

```bash
cd trekking_management_backend

python -m venv env

source env/bin/activate

pip install -r requirements.txt
```

### Frontend Setup

```bash
cd trekking_management_frontend

npm install
```

---

## Running the Application

### Start Redis

```bash
redis-server
```

### Start Flask Backend

```bash
flask run
```

### Start Celery Worker

```bash
celery -A extensions.celery worker --loglevel=info
```

### Start Celery Beat

```bash
celery -A extensions.celery beat --loglevel=info
```

### Start Vue Frontend

```powershell
npm run dev
```

---

## API Documentation

The API documentation is available in the `api.yaml` file and can be viewed using Swagger Editor, Swagger UI, or any OpenAPI-compatible tool.

---

## Future Enhancements

- Online payment gateway integration
- Google Maps integration
- Weather forecasting for treks
- Mobile application
- Push notifications
- Advanced analytics dashboard

---

## Author

**Saanjhi Varshney**

IIT Madras BS Degree Programme

