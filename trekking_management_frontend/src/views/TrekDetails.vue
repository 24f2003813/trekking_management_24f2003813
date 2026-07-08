<template>
  <div class="trek-details">
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
      <div class="sidebar bg-light p-3">
        <ul class="nav flex-column">
          <li class="nav-item"><router-link to="/trekker/dashboard" class="nav-link">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/trekker/history" class="nav-link">History</router-link></li>
          <li class="nav-item"><router-link to="/trekker/profile" class="nav-link">Profile</router-link></li>
          <li class="nav-item"><router-link to="/trekker/treks" class="nav-link">Treks</router-link></li>
          <li class="nav-item"><router-link to="/trekker/badge" class="nav-link">Badge</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4" v-if="trek">
        <h3>{{ trek.name }}</h3>
        <p><strong>Location:</strong> {{ trek.location }}</p>
        <p><strong>Difficulty:</strong> {{ trek.difficulty }}</p>
        <p><strong>Description:</strong> {{ trek.description }}</p>
        <p><strong>Dates:</strong> {{ trek.start_date }} to {{ trek.end_date }}</p>
        <p><strong>Price:</strong> {{ trek.price }}</p>
        <p><strong>Slots Available:</strong> {{ trek.slots_available }}</p>
        <button class="btn btn-success" @click="bookTrek">Book Trek</button>
        <button v-if="booking && booking.payment_flag === 'pending'" 
          class="btn btn-warning ms-2" 
          @click="payBooking(booking.id)">Pay Now</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TrekDetails",
  data() {
    return { trek: null, trekkerName: "" ,booking:null};
  },
  async mounted() {
    const token = localStorage.getItem("token");
    const res = await axios.get(`http://localhost:5000/api/trekker/treks/${this.$route.params.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    this.trek = res.data;
    this.trekkerName = localStorage.getItem("trekkerName") || "Trekker";
  },
  methods: {
    async bookTrek() {
      const token = localStorage.getItem("token");
      const res = await axios.post(
        `http://localhost:5000/api/trekker/treks/${this.trek.id}/book`,
        {},
        { headers: { Authorization: `Bearer ${token}`} }
      );
      alert(res.data.message);
      this.booking = { id: res.data.booking_id, payment_flag: "pending" };
    },
    async payBooking(bookingId) {
      const token = localStorage.getItem("token");
      const res = await axios.put(
        `http://localhost:5000/api/bookings/${bookingId}/pay`,
        { payment_flag: "paid" },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert(res.data.message);
      this.booking.payment_flag = "paid";
    }
  }
};
</script>
<style scoped>
.trekker-treks,
.trek-details {
  min-height: 100vh;
}

.sidebar {
  width: 220px;
  border-right: 1px solid #ddd;
  background-color: #f9f9f9;
}

.sidebar .nav-link {
  color: #8B5E3C;
  font-weight: 500;
  margin-bottom: 10px;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.2s ease, color 0.2s ease;
}

.sidebar .nav-link:hover {
  background-color: #F3E5AB;
  color: #5a3a22; 
  text-decoration: none;
}

.sidebar .router-link-active {
  background-color: #8B5E3C;
  color: #fff !important;
}
</style>
