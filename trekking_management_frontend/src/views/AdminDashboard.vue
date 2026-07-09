<template>
  <div class="admin-dashboard">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Admin Dashboard</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link text-light">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/logout" class="nav-link text-light">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="d-flex">
      <div class="sidebar bg-light p-3">
        <ul class="nav flex-column">
          <li class="nav-item"><router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/admin/treks" class="nav-link">Treks</router-link></li>
          <li class="nav-item"><router-link to="/admin/bookings" class="nav-link">Bookings</router-link></li>
          <li class="nav-item"><router-link to="/admin/trekkers" class="nav-link">Trekkers</router-link></li>
          <li class="nav-item"><router-link to="/admin/staff" class="nav-link">Staff</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <div class="row g-4">
          <div class="col-md-3" v-for="card in summaryCards" :key="card.title">
            <div class="card text-center shadow-sm summary-card">
              <div class="card-body">
                <h5 class="card-title">{{ card.title }}</h5>
                <p class="card-text display-6 fw-bold">{{ card.value }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-5">
          <h4 class="mb-3">Recent Bookings</h4>
          <table class="table table-striped table-bordered">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Trek Name</th>
                <th>User Name</th>
                <th>Status</th>
                <th>Payment</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in recentBooking" :key="b.id">
                <td>{{ b.id }}</td>
                <td>{{ b.trek_name }}</td>
                <td>{{ b.user_name }}</td>
                <td>{{ b.status }}</td>
                <td>{{ b.payment_flag }}</td>
                <td>{{ b.booking_date }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AdminDashboard",

  data() {
    return {
      summaryCards: [],
      recentBooking: []
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get(
        "http://localhost:5000/api/admin/dashboard",
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      this.summaryCards = [
        { title: "Total Treks", value: res.data.summary.total_treks },
        { title: "Total Trekkers", value: res.data.summary.total_users },
        { title: "Total Trekking Staff", value: res.data.summary.total_staff },
        { title: "Total Bookings", value: res.data.summary.total_bookings }
      ];

      this.recentBooking = res.data.recent_bookings;

    } catch (err) {
      console.error(err);
      if (err.response) {
        alert(err.response.data.error || "Something went wrong");
      } else {
        alert("Unable to connect to the server.");
      }
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.sidebar {
  width: 220px;
  border-right: 1px solid #ddd;
}
.sidebar .nav-link {
  color: #8B5E3C;
  font-weight: 500;
  margin-bottom: 10px;
}
.sidebar .nav-link:hover {
  background-color: #F5F5DC;
  border-radius: 5px;
}

.summary-card {
  background-color: #F5F5DC;
  border: none;
}
.summary-card .card-title {
  color: #8B5E3C;
  font-weight: 600;
}
.summary-card .card-text {
  color: #5C4033;
}
</style>
