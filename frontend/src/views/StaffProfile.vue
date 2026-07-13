<template>
  <div class="staff-profile">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Staff Profile</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
            </li>
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
          <li class="nav-item"><router-link to="/staff/dashboard" class="nav-link">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/staff/profile" class="nav-link">Profile</router-link></li>
          <li class="nav-item"><router-link to="/staff/participants" class="nav-link">Participants</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <h3 class="mb-4">Edit Profile</h3>
        <form @submit.prevent="updateProfile" class="w-50">
          <div class="mb-3">
            <label class="form-label">Name</label>
            <input type="text" v-model="profile.name" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Email (read-only)</label>
            <input type="email" v-model="profile.email" class="form-control" disabled />
          </div>
          <div class="mb-3">
            <label class="form-label">Contact Number</label>
            <input type="text" v-model="profile.contact_number" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">experience</label>
            <textarea v-model="profile.experience" class="form-control" rows="3"></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Save Changes</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "StaffProfile",
  data() {
    return {
      profile: {
        name: "",
        email: "",
        contact_number: "",
        experience: ""
      }
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/api/staff/profile", {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.profile = {
        name: res.data.name,
        email: res.data.email,
        contact_number: res.data.contact_number,
        experience: res.data.experience
      };
    } catch (err) {
        console.log(err.response);
        console.log(err.response?.status);
        console.log(err.response?.data);
        alert(JSON.stringify(err.response?.data) || "Unable to load profile");
    }
  },
  methods: {
    async updateProfile() {
      try {
        const token = localStorage.getItem("token");
        await axios.put("http://localhost:5000/api/staff/profile", this.profile, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Profile updated successfully!");
      } catch (err) {
        console.log(err.response);
        console.log(err.response?.status);
        console.log(err.response?.data);
        alert(JSON.stringify(err.response?.data) || "Unable to load profile");
      }
    }
  }
};
</script>

<style scoped>
.staff-profile {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
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
