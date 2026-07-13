<template>
  <div class="staff-dashboard">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Staff Dashboard</span>

        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/logout" class="nav-link text-light">
                Logout
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="d-flex">
      <div class="sidebar bg-light p-3">
        <ul class="nav flex-column">
          <li class="nav-item">
            <router-link to="/staff/dashboard" class="nav-link">
              Dashboard
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/staff/profile" class="nav-link">
              Edit Profile
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/staff/participants" class="nav-link">
              Participants
            </router-link>
          </li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <h2 class="mb-4">Assigned Trek</h2>
        <div v-if="loading">
          Loading trek details...
        </div>
        <div v-else-if="trek">
          <div class="card shadow-sm p-4">
            <h4>{{ trek.trek_name }}</h4>
            <p><strong>ID:</strong> {{ trek.trek_id }}</p>
            <p><strong>Location:</strong> {{ trek.location }}</p>
            <p><strong>Status:</strong> {{ trek.trek_status }}</p>
            <p><strong>Participants:</strong> {{ trek.participant_count }}</p>
            <p><strong>Maximum Capacity:</strong> {{ trek.max_trekker }}</p>
            <p><strong>Start Date:</strong> {{ trek.start_date }}</p>
            <p><strong>End Date:</strong> {{ trek.end_date }}</p>
            <p><strong>Description:</strong> {{ trek.description }}</p>
            <hr>
            <div class="mb-3">
              <label class="form-label">Update Capacity</label>
              <input
                type="number"
                class="form-control"
                v-model="newCapacity">
            </div>
            <button class="btn btn-primary mb-4" @click="updateCapacity">Update Capacity</button>
            <hr>
            <div class="mb-3">
              <label class="form-label">Update Trek Status</label>
              <select class="form-select" v-model="newStatus">
                <option disabled value="">Select Status</option>
                <option value="open">Open</option>
                <option value="completed">Completed</option>
              </select>
            </div>
            <button class="btn btn-success" @click="updateStatus">Update Status</button>
          </div>
        </div>
        <div v-else>
          <div class="alert alert-warning">
            No trek assigned.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "StaffTrek",
  data() {
    return {
      trek: null,
      loading: true,
      newCapacity: "",
      newStatus: ""
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const trekId = this.$route.params.id;
      const res = await axios.get(
        `http://localhost:5000/api/staff/treks/${trekId}`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );
      this.trek = res.data;
    } catch (err) {
      console.log(err.response);
      alert(
        err.response?.data?.error ||
        "Failed to load trek details"
      );
    } finally {
      this.loading = false;
    }
  },
  methods: {
    async updateCapacity() {
      try {
        const token = localStorage.getItem("token");
        await axios.put(
          `http://localhost:5000/api/staff/treks/${this.trek.trek_id}/slots_capacity`,
          {
            max_trekker: this.newCapacity
          },
          {headers: {Authorization: `Bearer ${token}`}});
        this.trek.max_trekker = this.newCapacity;
        this.newCapacity = "";
        alert("Capacity updated successfully");
      } catch (err) {
        alert(err.response?.data?.error ||"Failed to update capacity" );
      }
    },
    async updateStatus() {
      try {
        const token = localStorage.getItem("token");
        await axios.put(
          `http://localhost:5000/api/staff/treks/${this.trek.trek_id}/status`,
          {status: this.newStatus},
          {headers: {Authorization: `Bearer ${token}`}});
        this.trek.trek_status = this.newStatus;
        this.newStatus = "";
        alert("Status updated successfully");
      } catch (err) {
        alert(
          err.response?.data?.error ||"Failed to update status"
        );
      }
    }
  }
};
</script>

<style scoped>
.staff-dashboard{
    min-height:100vh;
}
.sidebar{
    width:220px;
    border-right:1px solid #ddd;
}
.sidebar .nav-link{
    color:#8B5E3C;
    font-weight:500;
    margin-bottom:10px;
}
.sidebar .nav-link:hover{
    background:#F5F5DC;
    border-radius:5px;
}
.card{
    max-width:700px;
}
</style>