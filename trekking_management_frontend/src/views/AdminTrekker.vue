<template>
  <div class="admin-dashboard">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Admin Trekkers</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><router-link to="/" class="nav-link text-light">Home</router-link></li>
            <li class="nav-item"><router-link to="/logout" class="nav-link text-light">Logout</router-link></li>
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
        <h2 class="mb-4" style="color:#8B5E3C;">Manage Trekkers</h2>
        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="Search trekker..." v-model="searchQuery">
          <button class="btn btn-brown" @click="fetchTrekkers">Search</button>
        </div>
        <table class="table table-striped table-bordered">
          <thead class="table-light">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Contact Number</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trekker in trekkers" :key="trekker.id">
              <td>{{ trekker.name }}</td>
              <td>{{ trekker.email }}</td>
              <td>{{ trekker.contact_number }}</td>
              <td>
                <span :class="statusClass(trekker.status)" class="badge">
                  {{ trekker.status }}
                </span>
              </td>
              <td class="text-end">
                <button 
                  v-if="trekker.status === 'active'" 
                  class="btn btn-warning btn-sm me-2" 
                  @click="blockTrekker(trekker.id)">
                  Block
                </button>
                <button 
                  v-else 
                  class="btn btn-success btn-sm me-2" 
                  @click="unblockTrekker(trekker.id)">
                  Unblock
                </button>
                <button 
                  class="btn btn-danger btn-sm" 
                  @click="deleteTrekker(trekker.id)">
                  Delete
                </button>
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
  name: "AdminTrekkers",
  data() {
    return {
      trekkers: [],
      searchQuery: '',
      message: ''
    }
  },
  methods: {
    async fetchTrekkers() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:5000/api/admin/users', {
          headers: { Authorization: `Bearer ${token}` },
          params: { search: this.searchQuery }
        })
        this.trekkers = res.data
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to load trekkers"
      }
    },
    async blockTrekker(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:5000/api/admin/users/${id}/status`, 
          { status: 'blocked' }, 
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchTrekkers()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to block trekker"
      }
    },
    async unblockTrekker(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:5000/api/admin/users/${id}/status`, 
          { status: 'active' }, 
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchTrekkers()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to unblock trekker"
      }
    },
    async deleteTrekker(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.delete(`http://localhost:5000/api/admin/users/${id}/status`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.message = res.data.message
        this.fetchTrekkers()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to delete trekker"
      }
    },
    statusClass(status) {
      return status === 'active' ? 'bg-success' : 'bg-danger'
    }
  },
  mounted() {
    this.fetchTrekkers()
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
