<template>
  <div class="user-dashboard">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Trekker Dashboard</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><router-link to="/" class="nav-link text-light">Home</router-link></li>
            <li class="nav-item"><router-link to="/logout" class="nav-link text-light">Logout</router-link></li>
            <li class="nav-item"><router-link to="/profile" class="nav-link text-light">Profile</router-link></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <h2 style="color:#8B5E3C;">Welcome, Trekker!</h2>

      <!-- Search Treks -->
      <div class="input-group mb-3">
        <input type="text" class="form-control" placeholder="Search treks..." v-model="searchQuery">
        <button class="btn btn-brown" @click="fetchTreks">Search</button>
      </div>

      <!-- Available Treks -->
      <h4 class="mt-4">Available Treks</h4>
      <div class="row">
        <div class="col-md-4 mb-3" v-for="trek in treks" :key="trek.id">
          <div class="card shadow-sm trek-card">
            <div class="card-body">
              <h5 class="card-title">{{ trek.name }}</h5>
              <p class="card-text">
                Location: {{ trek.location }} <br>
                Difficulty: {{ trek.difficulty }} <br>
                Slots Available: {{ trek.slots_available }} / {{ trek.max_trekker }} <br>
                Status: <span :class="statusClass(trek.status)" class="badge">{{ trek.status }}</span>
              </p>
              <button class="btn btn-success btn-sm" @click="bookTrek(trek.id)" :disabled="trek.status !== 'open' || trek.slots_available <= 0">
                Book Trek
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Booked Treks -->
      <h4 class="mt-4">My Bookings</h4>
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Trek</th>
            <th>Status</th>
            <th class="text-end">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in bookings" :key="booking.id">
            <td>{{ booking.trek_name }}</td>
            <td><span :class="statusClass(booking.status)" class="badge">{{ booking.status }}</span></td>
            <td class="text-end">
              <button v-if="booking.status === 'booked'" class="btn btn-danger btn-sm" @click="cancelBooking(booking.id)">Cancel</button>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Trekking History -->
      <h4 class="mt-4">Trekking History</h4>
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Trek</th>
            <th>Status</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="history in trekHistory" :key="history.id">
            <td>{{ history.trek_name }}</td>
            <td><span :class="statusClass(history.status)" class="badge">{{ history.status }}</span></td>
            <td>{{ history.booking_date }}</td>
          </tr>
        </tbody>
      </table>

      <!-- Message -->
      <div v-if="message" class="alert alert-info mt-3 text-center">
        {{ message }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "UserDashboard",
  data() {
    return {
      treks: [],
      bookings: [],
      trekHistory: [],
      searchQuery: '',
      message: ''
    }
  },
  methods: {
    async fetchTreks() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:5000/api/treks', {
          headers: { Authorization: `Bearer ${token}` },
          params: { search: this.searchQuery }
        })
        this.treks = res.data
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to load treks"
      }
    },
    async fetchBookings() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:5000/api/bookings', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.bookings = res.data
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to load bookings"
      }
    },
    async fetchHistory() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:5000/api/history', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.trekHistory = res.data
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to load history"
      }
    },
    async bookTrek(trekId) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.post('http://localhost:5000/api/bookings', 
          { trek_id: trekId },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchTreks()
        this.fetchBookings()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to book trek"
      }
    },
    async cancelBooking(bookingId) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:5000/api/bookings/${bookingId}`, 
          { status: 'cancelled' },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchTreks()
        this.fetchBookings()
        this.fetchHistory()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to cancel booking"
      }
    },
    statusClass(status) {
      switch(status) {
        case 'open': return 'bg-success'
        case 'booked': return 'bg-primary'
        case 'completed': return 'bg-info'
        case 'cancelled': return 'bg-danger'
        default: return 'bg-secondary'
      }
    }
  },
  mounted() {
    this.fetchTreks()
    this.fetchBookings()
    this.fetchHistory()
  }
}
</script>

<style scoped>
.btn-brown {
  background-color: #8B5E3C;
  color: #fff;
}
.btn-brown:hover {
  background-color: #5C4033;
}
.trek-card {
  background-color: #F5F5DC;
}
.trek-card .card-title {
  color: #8B5E3C;
}
.badge {
  font-size: 0.9em;
}
</style>
