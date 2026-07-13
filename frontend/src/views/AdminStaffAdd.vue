<template>
  <div class="dashboard">
    <nav class="navbar navbar-expand-lg navbar-dark bg-brown">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Trekking Management</a>
      </div>
    </nav>

    <div class="main d-flex">
      <aside class="sidebar bg-light p-3">
        <ul class="nav flex-column">
          <li class="nav-item">
            <router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/staff/add" class="nav-link">👤 Add Staff</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/admin/staff" class="nav-link">📋 Staff List</router-link>
          </li>
        </ul>
      </aside>

      <div class="content container mt-4">
        <h2 style="color:#8B5E3C;">Add New Staff Member</h2>

        <div v-if="message" class="alert alert-info mt-3 text-center">
          {{ message }}
        </div>

        <form @submit.prevent="addStaff" class="form-card p-4 shadow-sm">
          <div class="mb-3">
            <label class="form-label">Name</label>
            <input type="text" v-model="newStaff.name" class="form-control" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Email</label>
            <input type="email" v-model="newStaff.email" class="form-control" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Password</label>
            <input type="password" v-model="newStaff.password" class="form-control" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Contact Number</label>
            <input type="text" v-model="newStaff.contact_number" class="form-control" required>
          </div>

          <div class="mb-3">
            <label class="form-label">Experience (years)</label>
            <input type="number" v-model="newStaff.experience" class="form-control" min="0">
          </div>

          <div class="mb-3">
            <label class="form-label">Specialization</label>
            <select v-model="newStaff.specialization" class="form-select">
              <option value="mountain">Mountain</option>
              <option value="river">River</option>
              <option value="desert">Desert</option>
              <option value="forest">Forest</option>
              <option value="General">General</option>
            </select>
          </div>

          <button type="submit" class="btn btn-brown">Add Staff</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "AdminView",
  data() {
    return {
      newStaff: {
        name: '',
        email: '',
        password: '',
        specialization: 'General',
        contact_number: '',
        experience: ''
      },
      message: ''
    }
  },
  methods: {
    async addStaff() {
        try {
            const token = localStorage.getItem('token')
            const payload = { ...this.newStaff }
            if (payload.experience === '' || payload.experience === null) {
            delete payload.experience  
            }
            const res = await axios.post('http://localhost:5000/api/admin/staff',
            payload,
            { headers: { Authorization: `Bearer ${token}` } }
            )
            this.message = res.data.message || "Staff added successfully!"

            this.newStaff = { 
            name: '', 
            email: '', 
            password: '', 
            specialization: 'General',
            contact_number: '',
            experience: ''
            }
        } catch (error) {
            console.log(error.response)
            console.log(error.response?.status)
            console.log(error.response?.data)
        }
        }
  }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.navbar {
  background-color: #8B5E3C;
}
.main {
  flex: 1;
  display: flex;
}
.sidebar {
  width: 200px;
  border-right: 1px solid #ddd;
}
.content {
  flex: 1;
}
.form-card {
  background-color: #F5F5DC;
  border-radius: 10px;
}
.btn-brown {
  background-color: #8B5E3C;
  color: #fff;
}
.btn-brown:hover {
  background-color: #5C4033;
}
</style>