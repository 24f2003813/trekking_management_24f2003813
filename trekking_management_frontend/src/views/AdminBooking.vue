<template>
  <div class="admin-dashboard">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Admin Bookings</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><router-link to="/" class="nav-link text-light">Home</router-link></li>
            <li class="nav-item"><router-link to="/logout" class="nav-link text-light">Logout</router-link></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="d-flex">
      <!-- Sidebar -->
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
        <h2 class="mb-4" style="color:#8B5E3C;">Manage Bookings</h2>

        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="Search booking..." v-model="searchQuery">
          <button class="btn btn-brown" @click="fetchBookings">Search</button>
        </div>

        <table class="table table-striped table-bordered">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Trek</th>
              <th>Trekker</th>
              <th>Payment_Status</th>
              <th>Status</th>
              <th>Created At</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in bookings" :key="booking.id">
              <td>{{ booking.id }}</td>
              <td>{{ booking.trek_name }}</td>
              <td>{{ booking.user_name }}</td>
              <td>
                <span :class="paymentClass(booking.payment_flag)" class="badge">
                  {{ booking.payment_flag || 'pending' }}
                </span>
              </td>
              <td>
                <span :class="statusClass(booking.status)" class="badge">
                  {{ booking.status }}
                </span>
              </td>
              <td>{{ booking.booking_date }}</td>
              <td class="text-end">
                <select v-model="booking.status" @change="updateBookingStatus(booking.id, booking.status)" class="form-select form-select-sm w-auto d-inline-block me-2">
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
                <button class="btn btn-danger btn-sm" @click="deleteBooking(booking.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="message" class="alert alert-info mt-3 text-center">
          {{ message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "AdminBookings",
  data() {
    return {
      bookings: [],
      searchQuery: '',
      message: ''
    }
  },
  methods: {
    async fetchBookings() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:5000/api/admin/bookings', {
          headers: { Authorization: `Bearer ${token}` },
          params: { search: this.searchQuery }
        })
        this.bookings = res.data
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to load bookings"
      }
    },
    async updateBookingStatus(id, status) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:5000/api/admin/bookings/${id}/status`, 
          { status }, 
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchBookings()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to update booking status"
      }
    },
    async deleteBooking(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.delete(`http://localhost:5000/api/admin/bookings/${id}/status`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.message = res.data.message
        this.fetchBookings()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to delete booking"
      }
    },
    statusClass(status) {
      switch(status) {
        case 'completed': return 'bg-success'
        case 'cancelled': return 'bg-danger'
        default: return 'bg-secondary'
      }
    }
  },
  mounted() {
    this.fetchBookings()
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
.badge {
  font-size: 0.9em;
}
</style>
