<template>
  <div class="admin-dashboard">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Admin Dashboard</span>
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
          <li class="nav-item"><router-link to="/admin/treks/add" class="nav-link">Add Trek</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <h2 class="mb-4" style="color:#8B5E3C;">Add New Trek</h2>
        <form @submit.prevent="addTrek" class="card p-4 shadow-sm form-card">
          <div class="mb-3"><label class="form-label">Name</label><input v-model="trek.name" class="form-control"></div>
          <div class="mb-3"><label class="form-label">Location</label><input v-model="trek.location" class="form-control"></div>
          <div class="mb-3"><label class="form-label">Description</label><textarea v-model="trek.description" class="form-control"></textarea></div>
          <div class="mb-3"><label class="form-label">Duration (days)</label><input type="number" v-model="trek.duration" class="form-control"></div>
          <div class="mb-3"><label class="form-label">Difficulty</label>
            <select v-model="trek.difficulty" class="form-select">
              <option>Easy</option><option>Moderate</option><option>Hard</option>
            </select>
          </div>
          <div class="mb-3"><label class="form-label">Price</label><input type="number" v-model="trek.price" class="form-control"></div>
          <div class="mb-3"><label class="form-label">Slots Available</label><input type="number" v-model="trek.slots_available" class="form-control"></div>
          <div class="mb-3"><label class="form-label">Start Date</label><input type="date" v-model="trek.start_date" class="form-control"></div>
          <div class="mb-3"><label class="form-label">End Date</label><input type="date" v-model="trek.end_date" class="form-control"></div>
          <div class="mb-3"><label class="form-label">Assign Guide</label>
            <select v-model="trek.assigned_guide_id" class="form-select">
              <option v-for="guide in eligibleGuides" :key="guide.id" :value="guide.id">
                {{ guide.name }} ({{ guide.specialization }})
              </option>
            </select>
          </div>
          <button type="submit" class="btn btn-brown w-100">Add Trek</button>
        </form>
        <div v-if="message" class="alert alert-info mt-3">{{ message }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "AdminAddTrek",
  data() {
    return {
      trek: {
        name:'', location:'', description:'', duration:'',
        difficulty:'', price:'', slots_available:'',
        start_date:'', end_date:'', assigned_guide_id:''
      },
      eligibleGuides: [],
      message: ''
    }
  },
  methods: {
    async fetchEligibleGuides() {
      const token = localStorage.getItem('token')
      const res = await axios.get('http://127.0.0.1:5000/api/admin/eligible_guides', {
        headers: { Authorization: `Bearer ${token}` }
      })
      console.log("Eligible guides:", res.data);
      this.eligibleGuides = res.data
    },
    async addTrek() {
      try {
        const token = localStorage.getItem('token')
        const res = await axios.post('http://127.0.0.1:5000/api/admin/treks', this.trek, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.message = res.data.notification
        this.trek = {}
      } 
        catch (err) {
          console.log(err.response.status);
          console.log(err.response.data);
        }
      }
    },
  mounted() {
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
.form-card {
  background-color: #F5F5DC;
  border-radius: 10px;
}
.info-card {
  background-color: #F5F5DC;
}
.info-card .card-title {
  color: #8B5E3C;
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

