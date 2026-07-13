<template>
  <div class="trekker-treks">
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
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <h3 class="mb-3">Available Treks</h3>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Name</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Dates</th>
              <th>Price</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in treks" :key="t.id">
              <td>{{ t.name }}</td>
              <td>{{ t.location }}</td>
              <td>{{ t.difficulty }}</td>
              <td>{{ t.start_date }} to {{ t.end_date }}</td>
              <td>{{ t.price }}</td>
              <td>
                <router-link :to="`/trek/details/${t.id}`" class="btn btn-primary btn-sm">
                  View Details
                </router-link>
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

export default {
  name: "TrekkerTreks",
  data() {
    return { treks: [], trekkerName: "" };
  },
  async mounted() {
    const token = localStorage.getItem("token");
    const res = await axios.get("http://localhost:5000/api/trekker/treks", {
      headers: { Authorization: `Bearer ${token}` }
    });
    this.treks = res.data;
    this.trekkerName = res.data[0].trekker_name  
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

