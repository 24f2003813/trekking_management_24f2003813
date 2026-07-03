<template>
  <div class="logout-page d-flex flex-column align-items-center justify-content-center vh-100">
    <div class="card shadow-sm p-4 text-center">
      <h2 style="color:#8B5E3C;">Logging Out...</h2>
      <p>You have been logged out successfully.</p>
      <router-link to="/" class="btn btn-brown mt-3">Go to Home</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "Logout",
  mounted() {
    // Clear token and any other session data
    localStorage.removeItem('token')
    localStorage.removeItem('user') // if you store user info
    // Optionally redirect after a short delay
    setTimeout(() => {
      this.$router.push('/')
    }, 1500)
  }
}
</script>

<style scoped>
.logout-page {
  background-color: #F5F5DC;
}
.btn-brown {
  background-color: #8B5E3C;
  color: #fff;
}
.btn-brown:hover {
  background-color: #5C4033;
}
</style>
