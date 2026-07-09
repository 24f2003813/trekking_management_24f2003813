<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg" style="background-color:#8B5E3C;">
      <div class="container-fluid">
        <a class="navbar-brand text-light fw-bold" >Trekking Buddy</a>
        <div class="collapse navbar-collapse">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link text-light">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/login" class="nav-link text-light">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register" class="nav-link text-light">Register</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <header class="text-center py-5" style="background-color:#F5F5DC;">
      <h1 class="fw-bold" style="color:#8B5E3C;">Welcome to Trekking Buddy</h1>
      <p class="lead" style="color:#5C4033;">
        Organize treks, manage participants, and explore adventures with ease.
      </p>
    </header>

    <section class="container my-5">
      <div class="row">
        <div class="col-md-4">
          <div class="card border-0 shadow-sm" style="background-color:#F5F5DC;">
            <div class="card-body">
              <h5 class="card-title" style="color:#8B5E3C;">For Admins</h5>
              <p class="card-text">Manage treks, staff, and bookings with a powerful dashboard.</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm" style="background-color:#F5F5DC;">
            <div class="card-body">
              <h5 class="card-title" style="color:#8B5E3C;">For Staff</h5>
              <p class="card-text">View assigned treks, update trek status, and manage participants.</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-0 shadow-sm" style="background-color:#F5F5DC;">
            <div class="card-body">
              <h5 class="card-title" style="color:#8B5E3C;">For Trekkers</h5>
              <p class="card-text">Browse treks, book adventures, and track your trekking history.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="text-center py-3" style="background-color:#8B5E3C; color:#F5F5DC;">
      <strong>Trekking Management System</strong>
      <p>Contact Us:TrekkingBuddy@gmail.com</p>
    </footer>
  </div>
</template>

<script>
export default{
    name: 'LandingView'
}
</script>