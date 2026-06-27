## Hi there 👋

<!--
**24f2003813/24f2003813** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
🔑 Auth Routes
POST /api/auth/register → Register a new trekker (users only, staff created by admin).
POST /api/auth/login → Login for Admin, Staff, or User (returns JWT).

👑 Admin Routes
Dashboard
GET /api/admin/dashboard → Summary counts (treks, users, staff, bookings, recent bookings).

Manage Treks
GET /api/admin/treks → List all treks.
POST /api/admin/treks → Add new trek.
PUT /api/admin/treks/<trek_id> → Update trek details/status.
DELETE /api/admin/treks/<trek_id> → Delete trek.

Manage Staff
GET /api/admin/staff → List trekking staff.
POST /api/admin/staff → Create new staff (with email, specialization, etc.).
PUT /api/admin/staff/<staff_id> → Update staff details/status.
DELETE /api/admin/staff/<staff_id> → Blacklist/remove staff.

Manage Users (Trekkers)
GET /api/admin/users → List trekkers.
PUT /api/admin/users/<user_id> → Update user status (active/blocked).
DELETE /api/admin/users/<user_id> → Blacklist/remove user.

Manage Bookings
GET /api/admin/bookings → View all bookings.
PUT /api/admin/bookings/<booking_id> → Update booking status (cancelled, completed).

🧑‍🤝‍🧑 Staff Routes
GET /api/staff/treks → View assigned treks.
GET /api/staff/treks/<trek_id>/participants → View participants for a trek.
PUT /api/staff/treks/<trek_id> → Update trek status (open, closed, completed).
PUT /api/staff/treks/<trek_id>/complete → Mark trek as completed.

🥾 User (Trekker) Routes
GET /api/treks → Browse available treks (filter by difficulty/location).
GET /api/treks/<trek_id> → View trek details.
POST /api/bookings → Book a trek.
GET /api/bookings → View user’s bookings.
PUT /api/bookings/<booking_id> → Cancel booking.
GET /api/history → View completed/cancelled trek history.
GET /api/profile → View user profile.
PUT /api/profile → Update user profile.

🏅 Badge Routes (Optional Gamification)
GET /api/badges → List all badges.
GET /api/user/<user_id>/badges → View badges earned by a user.