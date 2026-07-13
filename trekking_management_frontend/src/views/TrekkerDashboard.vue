<template>
  <div class="trekker-dashboard">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Welcome, {{ trekkerName }}!</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <span class="navbar-brand text-light fw-bold">{{ TrekkerBadge }}</span>
            <li class="nav-item"><router-link to="/logout" class="nav-link text-light">Logout</router-link></li>
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
          <li class="nav-item"><router-link to="/trekker/trek" class="nav-link">Treks</router-link></li>
          <li class="nav-item"><router-link to="/trekker/badge" class="nav-link">Badge</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <h3 class="mb-3">Available Treks</h3>
        <div class="row mb-3">
          <div class="col-md-4">
            <input type="text" v-model="filters.name" class="form-control" placeholder="Search by trek name">
          </div>
          <div class="col-md-4">
            <input type="text" v-model="filters.location" class="form-control" placeholder="Search by location">
          </div>
          <div class="col-md-4">
            <select v-model="filters.difficulty" class="form-select">
              <option value="">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
        </div>
        <button class="btn btn-success mb-3" @click="fetchTreks">Apply Filters</button>

        <div v-if="availableTreks.length === 0" class="alert alert-info">
          No treks match your filters.
        </div>
        <div class="row">
          <div class="col-md-4 mb-3" v-for="trek in availableTreks" :key="trek.id">
            <div class="card shadow-sm p-3">
              <h5>{{ trek.name }}</h5>
              <p><strong>Location:</strong> {{ trek.location }}</p>
              <p><strong>Difficulty:</strong> {{ trek.difficulty }}</p>
              <p><strong>Slots Left:</strong> {{ trek.slots_available }}</p>
              <button class="btn btn-primary btn-sm" 
                      :disabled="trek.slots_available === 0"
                      @click="bookTrek(trek.id)">
                {{ trek.slots_available > 0 ? 'Book Now' : 'Not Available' }}
              </button>
            </div>
          </div>
        </div>

        <h3 class="mt-4">My Bookings</h3>
        <div v-if="bookedTreks.length === 0" class="alert alert-warning">
          You have no active bookings.
        </div>
        <table v-else class="table table-striped table-bordered">
          <thead class="table-light">
            <tr>
              <th>Booking ID</th>
              <th>Trek Name</th>
              <th>Status</th>
              <th>Booking Date</th>
              <th>Payment</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in bookedTreks" :key="b.Booking_id">
              <td>{{ b.Booking_id }}</td>
              <td>{{ b.trek_name }}</td>
              <td>{{ b.status }}</td>
              <td>{{ b.booking_date }}</td>
              <td>{{ b.payment_flag }}</td>
              <td>
                <button v-if="b.payment_flag !== 'paid'" class="btn btn-success btn-sm" @click="payBooking(b.Booking_id)">
                  Pay Now
                </button>
                <button class="btn btn-danger btn-sm" @click="cancelBooking(b.Booking_id)">
                  Cancel
                </button>
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
import TrekkerBadge from "./TrekkerBadge.vue";
export default {
  name: "TrekkerDashboard",
  data() {
    return {
      trekkerName: "",
      TrekkerBadge: "" ,
      availableTreks: [],
      bookedTreks: [],
      filters: { name: "", location: "", difficulty: "" }
    };
  },
  async mounted() {
    await this.fetchTreks();
    await this.fetchBadge();
  },
  methods: {
    async fetchTreks() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://localhost:5000/api/user/dashboard", {
          headers: { Authorization: `Bearer ${token}` },
          params: this.filters 
        });
        this.availableTreks = res.data.available_treks;
        this.bookedTreks = res.data.booked_treks;
        this.trekkerName = localStorage.getItem("trekkerName") || "Trekker";
      } catch (err) {
        alert(err.response?.data?.error || "Failed to load dashboard");
      }
    },
    async fetchBadge() {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.get("http://localhost:5000/api/user/badges", {
          headers: { Authorization: `Bearer ${token}` }
        });

        const earned = res.data.filter(b => b.progress >= b.criteria);
        if (earned.length > 0) {
          const latestBadge = earned[earned.length - 1];
          this.TrekkerBadge = `${latestBadge.name} 🏅`;
        } else {
          this.TrekkerBadge = "";
        }
      } catch (err) {
        console.error("Failed to load badges", err);
      }
    },
    async payBooking(bookingId) {
      try {
        const token = localStorage.getItem("token");
        const res = await axios.put(
          `http://localhost:5000/api/bookings/${bookingId}/pay`,
          { payment_flag: "paid" },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert(res.data.message);
        this.fetchTreks(); // refresh dashboard
      } catch (err) {
        alert(err.response?.data?.error || "Payment failed");
      }
    },
    async bookTrek(trekId) {
      try {
        const token = localStorage.getItem("token");
        await axios.post(`http://localhost:5000/api/trekker/treks/${trekId}/book`, 
          { trek_id: trekId },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert("Trek booked successfully");
        location.reload();
      } catch (err) {
        alert(err.response?.data?.error || "Failed to book trek");
      }
    },
    async cancelBooking(bookingId) {
      try {
        const token = localStorage.getItem("token");
        await axios.put(`http://localhost:5000/api/user/booking_cancel/${bookingId}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Booking cancelled successfully");
        location.reload();
      } catch (err) {
        alert(err.response?.data?.error || "Failed to cancel booking");
      }
    }
  }
};
</script>

<style scoped>
.trekker-dashboard {
  min-height: 100vh;
}
.sidebar {
  width: 220px;
  border-right: 1px solid #ddd;
}
.sidebar .nav-link {
  color:#8B5E3C;
  font-weight: 500;
  margin-bottom: 10px;
}
.sidebar .nav-link:hover {
  background-color: #F5F5DC;
  border-radius: 5px;
}
.card {
  min-height: 200px;
}
</style>
