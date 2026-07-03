import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import LandingView from '../views/LandingView.vue'
import Dashboard from '../views/AdminDashboard.vue'
import Treks from '../views/AdminTreks.vue'
import TrekAdd from '../views/AdminTrekAdd.vue'
import Staff from '../views/AdminStaff.vue'
import StaffAdd from '../views/AdminStaffAdd.vue'
// import StaffEdit from '../views/AdminStaffEdit.vue'
import Users from '../views/AdminTrekker.vue'
import Bookings from '../views/AdminBooking.vue'
import Logout from '../views/Logout.vue'


const routes =[
  {path: '/', component:LandingView},
  {path:'/login', component:Login},
  {path:'/register',component:Register},
  {path:'/admin/dashboard',component:Dashboard},
  {path:'/admin/treks',component:Treks},
  {path:'/admin/treks/add',component:TrekAdd},
  {path:'/admin/staff',component:Staff},
  {path:'/admin/staff/add',component:StaffAdd},
  // {path:'/admin/staff/edit',component:StaffEdit},
  {path:'/admin/trekkers',component:Users},
  {path:'/admin/bookings',component:Bookings},
  {path:'/logout', component:Logout}

]
const router=createRouter({
  history: createWebHistory(),
  routes
})
export default router


