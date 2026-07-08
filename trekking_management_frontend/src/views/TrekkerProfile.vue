<template>
  <div class="trekker-profile">
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
          <li class="nav-item"><router-link to="/trekker/trek" class="nav-link">Treks</router-link></li>
          <li class="nav-item"><router-link to="/trekker/badge" class="nav-link">Badge</router-link></li>
        </ul>
      </div>

      <!-- Content -->
      <div class="content flex-grow-1 p-4">
        <h3 class="mb-3">My Profile</h3>

        <form @submit.prevent="updateProfile">
          <div class="mb-3">
            <label class="form-label">Name</label>
            <input v-model="profile.name" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Email</label>
            <input v-model="profile.email" type="email" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Contact Number</label>
            <input v-model="profile.contact_number" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Emergency Contact Number</label>
            <input v-model="profile.emergency_contact_number" type="text" class="form-control" />
          </div>

          <button type="submit" class="btn btn-success">Update Profile</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TrekkerProfile",
  data() {
    return {
      trekkerName: "",
      profile: {
        name: "",
        email: "",
        contact_number: "",
        emergency_contact_number: ""
      }
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/api/user/edit_profile", {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.profile = res.data;
      this.trekkerName = res.data.name;
    } catch (err) {
      alert(err.response?.data?.error || "Failed to load profile");
    }
  },
  methods: {
    async updateProfile() {
      try {
        const token = localStorage.getItem("token");
        await axios.put("http://localhost:5000/api/user/edit_profile", this.profile, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Profile updated successfully");
      } catch (err) {
        alert(err.response?.data?.error || "Failed to update profile");
      }
    }
  }
};
</script>

<style scoped>
.trekker-profile {
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
</style>
