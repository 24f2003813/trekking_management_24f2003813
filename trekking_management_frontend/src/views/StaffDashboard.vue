<template>
  <div class="staff-dashboard">
    <!-- Navbar -->
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
          <li class="nav-item"><router-link to="/staff/trek" class="nav-link">My Trek</router-link></li>
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
                <th>Participants</th>
                <th>Current Capacity</th>
                <th>Update Capacity</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="trek in trekDetails" :key="trek.trek_id">
                <td>{{ trek.trek_id }}</td>
                <td>{{ trek.trek_name }}</td>
                <td>
                  <span :class="{
                    'badge bg-success': trek.trek_status === 'open',
                    'badge bg-danger': trek.trek_status === 'cancelled',
                    'badge bg-secondary': trek.trek_status === 'completed',
                    'badge bg-warning': trek.trek_status === 'full'
                  }">
                    {{ trek.trek_status }}
                  </span>
                </td>
                <td>{{ trek.participant_count }}</td>
                <td>{{ trek.max_trekker }}</td>
                <td>
                  <input type="number" v-model="trek.newCapacity" class="form-control form-control-sm" placeholder="Max trekkers">
                  <button class="btn btn-sm btn-primary me-2" @click="updateCapacity(trek)">Update Capacity</button>
                </td>
                <td>
                  
                  <select v-model="trek.newStatus" class="form-select form-select-sm d-inline-block w-auto me-2">
                    <option disabled value="">Change Status</option>
                    <option value="open">Open</option>
                    <option value="completed">Completed</option>
                  </select>
                  <button class="btn btn-sm btn-success" @click="updateStatus(trek)">Update Status</button>
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
        newCapacity: "",
        newStatus: ""
      }));
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Unable to connect to the server.");
    }
  },
  methods: {
    async updateCapacity(trek) {
      try {
        const token = localStorage.getItem("token");
        await axios.put(`http://localhost:5000/api/staff/treks/${trek.trek_id}/slots_capacity`, 
          { max_trekker: trek.newCapacity },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert(`Capacity updated for ${trek.trek_name}`);
        trek.max_trekker = trek.newCapacity; 
        trek.newCapacity = "";
      } catch (err) {
        alert(err.response?.data?.error || "Failed to update capacity");
      }
    },
    async updateStatus(trek) {
      try {
        const token = localStorage.getItem("token");
        await axios.put(`http://localhost:5000/api/staff/treks/${trek.trek_id}/status`, 
          { status: trek.newStatus },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert(`Status updated for ${trek.trek_name}`);
      } catch (err) {
        alert(err.response?.data?.error || "Failed to update status");
      }
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
