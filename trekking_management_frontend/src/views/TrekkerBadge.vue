<template>
  <div class="trekker-badge">
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
          <li class="nav-item"><router-link to="/trekker/treks" class="nav-link">Treks</router-link></li>
          <li class="nav-item"><router-link to="/trekker/badge" class="nav-link">Badges</router-link></li>
        </ul>
      </div>

      <!-- Content -->
      <div class="content flex-grow-1 p-4">
        <h2 class="mb-4" style="color:#8B5E3C;">My Badges</h2>

        <div v-for="badge in badges" :key="badge.id" class="mb-4">
          <h5>{{ badge.name }}</h5>
          <p>{{ badge.description }}</p>
          <div class="progress" style="height: 25px;">
            <div class="progress-bar" role="progressbar"
                 :style="{ width: (badge.progress / badge.criteria * 100) + '%' }"
                 :aria-valuenow="badge.progress"
                 :aria-valuemin="0"
                 :aria-valuemax="badge.criteria">
              {{ badge.progress }}/{{ badge.criteria }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TrekkerBadge",
  data() {
    return { badges: [], trekkerName: "" }
  },
  async mounted() {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://localhost:5000/api/user/badges", {
      headers: { Authorization: `Bearer ${token}` }
    });
    this.badges = res.data;
    this.trekkerName = localStorage.getItem("trekkerName") || "Trekker";
  }
}
</script>

<style scoped>
.trekker-badge {
  min-height: 100vh;
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
  background-color: #F3E5AB;
  border-radius: 5px;
}
.progress-bar {
  background-color: #8B5E3C; 
  font-weight: bold;
}
</style>
