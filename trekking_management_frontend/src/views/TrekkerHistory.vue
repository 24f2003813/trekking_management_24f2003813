<template>
  <div class="trekker-history">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Welcome, {{ trekkerName }}!</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/logout" class="nav-link text-light">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="d-flex">
      <!-- Sidebar -->
      <div class="sidebar bg-light p-3">
        <ul class="nav flex-column">
          <li class="nav-item"><router-link to="/trekker/dashboard" class="nav-link">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/trekker/history" class="nav-link">History</router-link></li>
          <li class="nav-item"><router-link to="/trekker/profile" class="nav-link">Profile</router-link></li>
          <li class="nav-item"><router-link to="/trekker/trek" class="nav-link">Treks</router-link></li>
          <li class="nav-item"><router-link to="/trekker/badge" class="nav-link">Badge</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <h3 class="mb-3">Trekking History</h3>
        <div v-if="history.length === 0" class="alert alert-secondary">
          No trekking history yet.
        </div>
        <table v-else class="table table-striped table-bordered">
          <thead class="table-light">
            <tr>
              <th>Trek</th>
              <th>Status</th>
              <th>Booking Date</th>
              <th>Trek Date</th>
              <th>Payement</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="h in history" :key="h.booking_id">
              <td>{{ h.trek_name }}</td>
              <td>{{ h.status }}</td>
              <td>{{ h.booking_date }}</td>
              <td>{{ h.trek_date }}</td>
              <td>
              <button v-if="h.payment_flag === 'pending'" 
                      class="btn btn-warning btn-sm" 
                      @click="payBooking(h.booking_id)">Pay</button>
              <span v-else>{{ h.payment_flag }}</span>
            </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TrekkerHistory",
  data() {
    return {
      trekkerName: "",
      history: []
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/api/user/history", {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.history = res.data;
      this.trekkerName = localStorage.getItem("trekkerName") || "Trekker";
    } catch (err) {
      alert(err.response?.data?.error || "Failed to load history");
    }
  },
  methods: {
  async payBooking(bookingId) {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.put(
        `http://localhost:5000/api/bookings/${bookingId}/pay`,
        { payment_flag: "paid" },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert(res.data.message);
      this.loadHistory(); // reload after payment
    } catch (err) {
      alert(err.response?.data?.error || "Payment failed");
    }
  }
}

};
</script>

<style scoped>
.trekker-history {
  min-height: 100vh;
}
.sidebar {
  width: 220px;
  border-right: 1px solid #ddd;
}
.sidebar .nav-link {
  color: #8B5E3C; /* brown theme */
  font-weight: 500;
  margin-bottom: 10px;
}
.sidebar .nav-link:hover {
  background-color: #F3E5AB; /* light beige hover */
  border-radius: 5px;
}
</style>
