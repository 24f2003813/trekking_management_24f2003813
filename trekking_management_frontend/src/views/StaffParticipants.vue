<template>
  <div class="staff-dashboard">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Staff Participants</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><router-link to="/logout" class="nav-link text-light">Logout</router-link></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="d-flex">
      <div class="sidebar bg-light p-3">
        <ul class="nav flex-column">
          <li class="nav-item"><router-link to="/staff/dashboard" class="nav-link">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/staff/profile" class="nav-link">Edit Profile</router-link></li>
          <li class="nav-item"><router-link to="/staff/participants" class="nav-link">Participants</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <h2 class="mb-4">Participants</h2>

        <input type="text" v-model="searchQuery" class="form-control mb-3" placeholder="Search by name, contact, trek">

        <table class="table table-striped table-bordered">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Contact</th>
              <th>Trek</th>
              <th>Boarded?</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in filteredParticipants" :key="p.id">
              <td>{{ p.id }}</td>
              <td>{{ p.name }}</td>
              <td>{{ p.email }}</td>
              <td>{{ p.contact_number }}</td>
              <td>{{ p.trek }}</td>
              <td>
                <input type="checkbox" v-model="p.boarded">
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
  name: "StaffParticipants",
  data() {
    return {
      participants: [],
      searchQuery: ""
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/api/staff/participants", {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.participants = res.data.map(p => ({ ...p, boarded: false }));
    } catch (err) {
      alert(err.response?.data?.error || "Failed to load participants");
    }
  },
  computed: {
    filteredParticipants() {
      const q = this.searchQuery.toLowerCase();
      return this.participants.filter(p =>
        p.name.toLowerCase().includes(q) ||
        p.contact_number.toLowerCase().includes(q) ||
        p.trek.toLowerCase().includes(q)
      );
    }
  }
};
</script>

<style scoped>
.staff-dashboard {
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
  background-color: #F5F5DC;
  border-radius: 5px;
}
</style>
