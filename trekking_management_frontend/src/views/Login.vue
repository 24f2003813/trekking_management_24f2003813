<template>
  <div class="login-page">
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <a class="navbar-brand text-light fw-bold">Trekking Buddy</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link text-light">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register" class="nav-link text-light">Register</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <header class="hero-section d-flex align-items-center justify-content-center">
      <div class="card shadow-lg p-4 form-card">
        <h2 class="text-center mb-4" style="color:#8B5E3C;">LOGIN PAGE</h2>
        <form @submit.prevent="sendLogin">
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input type="email" class="form-control" id="email" v-model="form.email">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" v-model="form.password">
          </div>
          <div class="mb-3 form-check">
            <input type="checkbox" class="form-check-input" id="remember">
            <label class="form-check-label" for="remember">Remember me</label>
          </div>
          <button type="submit" class="btn btn-brown w-100">Login</button>
        </form>
      </div>
    </header>

    <section class="container my-5">
      <div class="row">
        <div class="col-md-4" v-for="info in infos" :key="info.title">
          <div class="card border-0 shadow-sm info-card">
            <div class="card-body">
              <h5 class="card-title">{{ info.title }}</h5>
              <p class="card-text">{{ info.text }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: "LoginPage",
  data() {
    return {
      infos: [
        { title: "For Admins", text: "Manage treks, staff, and bookings with a powerful dashboard." },
        { title: "For Staff", text: "View assigned treks, update trek status, and manage participants." },
        { title: "For Trekkers", text: "Browse treks, book adventures, and track your trekking history." }
      ],
      form:{
        email:'',
        password:''
      },
      errorMessage:''
    }
  },
  methods:{
    async sendLogin(){
        try {
            const rec=await axios.post('http://localhost:5000/api/auth/login',this.form)

            localStorage.setItem('token',rec.data.token)
            localStorage.setItem('role',rec.data.role)

            if(rec.data.role === 'admin'){
                this.$router.push('/admin/dashboard')
            } else if (rec.data.role === 'staff'){
                this.$router.push('/staff/dashboard')
            } else{
                this.$router.push('/trekker/dashboard')
            }
            alert(rec.data.notification)
            this.errorMessage=''
        } catch(error){
            console.error("login failed",error)
            this.errorMessage=error.response?.data?.error||"Login failed"
       }
    }
  }
}
</script>

<style scoped>

.hero-section {
  background-size: cover;
  min-height: 80vh;
  position: relative;
}
.hero-section::before {
  content: "";
  position: absolute;
  inset: 0;
  background-color: rgba(139, 94, 60, 0.6); /* brown overlay */
}
.form-card {
  background-color: #F5F5DC; /* beige */
  border-radius: 10px;
  z-index: 1;
  width: 400px;
}
.btn-brown {
  background-color: #8B5E3C;
  color: #fff;
}
.btn-brown:hover {
  background-color: #5C4033;
}
.info-card {
  background-color: #F5F5DC;
}
.info-card .card-title {
  color: #8B5E3C;
}
.mb-3{
    margin-left: 10px;
}
</style>
