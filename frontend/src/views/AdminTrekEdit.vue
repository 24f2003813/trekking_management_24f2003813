<template>
  <div class="admin-trek-edit">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Edit Trek</span>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/admin/dashboard" class="nav-link text-light">Dashboard</router-link>
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
          <li class="nav-item"><router-link to="/admin/dashboard" class="nav-link">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/admin/treks" class="nav-link">Treks</router-link></li>
          <li class="nav-item"><router-link to="/admin/bookings" class="nav-link">Bookings</router-link></li>
          <li class="nav-item"><router-link to="/admin/staff" class="nav-link">Staff</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <h3 class="mb-4">Edit Trek Details</h3>
        <form @submit.prevent="updateTrek" class="w-50">
          <div class="mb-3">
            <label class="form-label">Trek Name</label>
            <input type="text" v-model="trek.name" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Status</label>
            <select v-model="trek.status" class="form-select">
              <option value="open">Open</option>
              <option value="cancelled">Cancelled</option>
              <option value="full">Full</option>
              <option value="completed">Completed</option>
            </select>
          </div>
          <div class="mb-3">
            <label class="form-label">Max Trekkers</label>
            <input type="number" v-model="trek.max_trekker" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Assigned Guide</label>
            <select v-model="trek.assigned_guide_id" class="form-select">
              <option disabled value="">Select Guide</option>
              <option v-for="guide in staffList" :key="guide.id" :value="guide.id">
                {{ guide.name }} ({{ guide.email }})
              </option>
            </select>
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
  name: "AdminTrekEdit",
  data() {
    return {
      trek: {
        id: "",
        name: "",
        status: "",
        max_trekker: "",
        assigned_guide_id: ""
      },
      staffList: []
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const trekId = this.$route.params.id;

      const res = await axios.get(`http://localhost:5000/api/admin/treks/${trekId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.trek = {
        id: res.data.id,
        name: res.data.name,
        status: res.data.status,
        max_trekker: res.data.max_trekker,
        assigned_guide_id: res.data.assigned_guide?.id || ""
      };

      const staffRes = await axios.get("http://localhost:5000/api/admin/staff", {
        headers: { Authorization: `Bearer ${token}` }
      });
      this.staffList = staffRes.data;
    } catch (err) {
      alert(err.response?.data?.error || "Unable to load trek details");
    }
  },
  methods: {
    async updateTrek() {
      try {
        const token = localStorage.getItem("token");
        await axios.put(`http://localhost:5000/api/admin/treks/${this.trek.id}`, this.trek, {
          headers: { Authorization: `Bearer ${token}` }
        });
        alert("Trek updated successfully!");
        this.$router.push("/admin/treks");
      } catch (err) {
        alert(err.response?.data?.error || "Failed to update trek");
      }
    }
  }
};
</script>

<style scoped>
.admin-trek-edit {
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
