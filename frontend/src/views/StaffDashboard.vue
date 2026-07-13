<template>
  <div class="staff-dashboard">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <span class="navbar-brand text-light fw-bold">Staff Dashboard</span>
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
          <li class="nav-item"><router-link to="/staff/dashboard" class="nav-link">Dashboard</router-link></li>
          <li class="nav-item"><router-link to="/staff/profile" class="nav-link"> Edit Profile</router-link></li>
          <li class="nav-item"><router-link to="/staff/participants" class="nav-link">Participants</router-link></li>
        </ul>
      </div>

      <div class="content flex-grow-1 p-4">
        <div class="row g-4">
          <div class="col-md-3" v-for="card in summaryCards" :key="card.title">
            <div class="card text-center shadow-sm summary-card">
              <div class="card-body">
                <h5 class="card-title">{{ card.title }}</h5>
                <p class="card-text display-6 fw-bold">{{ card.value }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-5">
          <h4 class="mb-3">Assigned Treks</h4>
          <table class="table table-striped table-bordered">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Trek Name</th>
                <th>Status</th>
                <th>View /Edit</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trek in trekDetails" :key="trek.trek_id">
                <td>
                    {{ trek.trek_id }}
                </td>
                <td>
                    {{ trek.trek_name }}
                </td>
                <td>
                    {{ trek.trek_status }}
                </td>
                <td>
                    <button class="btn btn-sm btn-success" @click="viewTrek(trek)">View And Edit</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from "axios";
export default {
  name: "StaffDashboard",
  data() {
    return {
      summaryCards: [],
      trekDetails: []
    };
  },
  async mounted() {
    try {
      const token = localStorage.getItem("token");
      const res = await axios.get("http://localhost:5000/api/staff/dashboard", {
        headers: { Authorization: `Bearer ${token}` }
      });


      this.summaryCards = [
        { title: "Treks Assigned", value: res.data.overview.treks_assigned },
        { title: "Total Participants", value: res.data.overview.participants_total }
      ];


      this.trekDetails = res.data.trek_details.map(trek => ({
        ...trek,
      }));
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Unable to connect to the server.");
    }
  },
  methods:{
    viewTrek(trek) {
      this.$router.push(`/staff/treks/${trek.trek_id}`);
    }
  }
};
</script>

<style scoped>
.staff-dashboard {
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

.summary-card {
  background-color: #F5F5DC;
  border: none;
}
.summary-card .card-title {
  color: #8B5E3C;
  font-weight: 600;
}
.summary-card .card-text {
  color: #5C4033;
}
</style>
