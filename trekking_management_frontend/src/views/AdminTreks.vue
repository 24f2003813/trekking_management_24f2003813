<template>
  <div class="admin-dashboard">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Admin Treks</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><router-link to="/" class="nav-link text-light">Home</router-link></li>
            <li class="nav-item"><router-link to="/logout" class="nav-link text-light">Logout</router-link></li>
            <li class="nav-item"><router-link to="/admin/treks/add" class="nav-link text-light">Add New Trek</router-link></li>
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

      <!-- Content -->
      <div class="content flex-grow-1 p-4">
        <h2 class="mb-4" style="color:#8B5E3C;">Manage Treks</h2>

        <!-- Search -->
        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="Search trek..." v-model="searchQuery">
          <button class="btn btn-brown" @click="fetchTreks">Search</button>
        </div>

        <!-- Trek Cards -->
        <div class="row">
          <div class="col-md-5 mb-3" v-for="trek in treks" :key="trek.id">
            <div class="card shadow-sm trek-card">
              <div class="card-body">
                <h5 class="card-title">{{ trek.name }}</h5>
                <p class="card-text">
                  Location: {{ trek.location }} <br>
                  Difficulty: {{ trek.difficulty }} <br>
                  Duration: {{ trek.duration }} days <br>
                  Price: ₹{{ trek.price }} <br>
                  Slots Available: {{ trek.slots_available }} <br>
                  Status: <span :class="statusClass(trek.status)">{{ trek.status }}</span><br>
                  Guide: {{ guideName(trek.assigned_guide_id) || 'Not Assigned' }}
                </p>

                <!-- Status Change -->
                <div class="d-flex justify-content-between mb-2">
                  <select v-model="trek.status" @change="updateTrekStatus(trek.id, trek.status)" class="form-select form-select-sm w-auto">
                    <option value="open">Open</option>
                    <option value="full">Full</option>
                    <option value="completed">Completed</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                  <button class="btn btn-danger btn-sm" @click="deleteTrek(trek.id)">Delete</button>
                </div>

                <!-- Guide Assignment -->
                <div>
                  <label class="form-label">Assign Guide</label>
                  <select v-model="trek.assigned_guide_id"
                          @change="assignGuide(trek.id, trek.assigned_guide_id)"
                          class="form-select form-select-sm">
                    <option disabled value="">Select Guide</option>
                    <option v-for="guide in eligibleGuides" :key="guide.id" :value="guide.id">
                      {{ guide.name }} ({{ guide.specialization }})
                    </option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Message -->
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
  name: "AdminTreks",
  data() {
    return {
      treks: [],
      eligibleGuides: [],
      searchQuery: '',
      message: ''
    }
  },
  methods: {
    async fetchTreks() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:5000/api/admin/treks', {
          headers: { Authorization: `Bearer ${token}` },
          params: { search: this.searchQuery }
        })
        this.treks = res.data
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to load treks"
      }
    },
    async fetchEligibleGuides() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:5000/api/admin/eligible_guides', {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.eligibleGuides = res.data
      } catch (error) {
        console.error("Failed to load eligible guides")
      }
    },
    async assignGuide(trekId, guideId) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:5000/api/admin/treks/${trekId}/assign_guide`,
          { guide_id: guideId },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchTreks()
      } catch (error) {
        if (error.response?.status === 409) {
          this.message = error.response.data.warning
        } else {
          this.message = error.response?.data?.error || "Failed to assign guide"
        }
      }
    },
    guideName(id) {
      const guide = this.eligibleGuides.find(g => g.id === id)
      return guide ? guide.name : null
    },
    statusClass(status) {
      switch (status) {
        case 'open': return 'text-success'
        case 'full': return 'text-warning'
        case 'completed': return 'text-primary'
        case 'cancelled': return 'text-danger'
        default: return ''
      }
    },
    async updateTrekStatus(id, status) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:5000/api/admin/treks/${id}`,
          { status },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchTreks()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to update trek status"
      }
    },
    async deleteTrek(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.delete(`http://localhost:5000/api/admin/treks/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.message = res.data.message
        this.fetchTreks()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to delete trek"
      }
    }
  },
  mounted() {
    this.fetchTreks()
    this.fetchEligibleGuides()
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
.trek-card {
  background-color: #F5F5DC;
}
.trek-card .card-title {
  color: #8B5E3C;
}
</style>
