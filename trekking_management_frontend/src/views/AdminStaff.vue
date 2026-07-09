<template>
  <div class="admin-dashboard">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Admin Staff</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><router-link to="/" class="nav-link text-light">Home</router-link></li>
            <li class="nav-item"><router-link to="/logout" class="nav-link text-light">Logout</router-link></li>
            <li class="nav-item"><router-link to="/admin/staff/add" class="nav-link text-light">Add New Staff</router-link></li>
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
        <h2 class="mb-4" style="color:#8B5E3C;">Manage Staff</h2>

        <!-- Search -->
        <div class="input-group mb-3">
          <input type="text" class="form-control" placeholder="Search staff member..." v-model="searchQuery">
          <button class="btn btn-brown" @click="fetchStaff">Search</button>
        </div>

        <!-- Staff Table -->
        <table class="table table-striped table-bordered">
          <thead class="table-light">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Specialization</th>
              <th>Status</th>
              <th class="text-end">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="staff in staffs" :key="staff.id">
              <td>{{ staff.name }}</td>
              <td>{{ staff.email }}</td>
              <td>{{ staff.specialization }}</td>
              <td>
                <span :class="staff.status === 'active' ? 'text-success' : 'text-danger'">
                  {{ staff.status }}
                </span>
              </td>
              <td class="text-end">
                <button 
                  v-if="staff.status === 'active'" 
                  class="btn btn-warning btn-sm me-2" 
                  @click="blockStaff(staff.id)">
                  Block
                </button>
                <button 
                  v-else 
                  class="btn btn-success btn-sm me-2" 
                  @click="unblockStaff(staff.id)">
                  Unblock
                </button>
                <button 
                  class="btn btn-danger btn-sm" 
                  @click="deleteStaff(staff.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>

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
  name: "AdminStaff",
  data() {
    return {
      staffs: [],
      searchQuery: '',
      message: ''
    }
  },
  methods: {
    async fetchStaff() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('http://localhost:5000/api/admin/staff', {
          headers: { Authorization: `Bearer ${token}` },
          params: { search: this.searchQuery }
        })
        this.staffs = res.data
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to load staff"
      }
    },
    async blockStaff(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:5000/api/admin/staff/${id}`, 
          { status: 'blocked' }, 
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchStaff()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to block staff"
      }
    },
    async unblockStaff(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.put(`http://localhost:5000/api/admin/staff/${id}`, 
          { status: 'active' }, 
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.message = res.data.message
        this.fetchStaff()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to unblock staff"
      }
    },
    async deleteStaff(id) {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.delete(`http://localhost:5000/api/admin/staff/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.message = res.data.message
        this.fetchStaff()
      } catch (error) {
        this.message = error.response?.data?.error || "Failed to delete staff"
      }
    }
  },
  mounted() {
    this.fetchStaff()
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
</style>
