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
import TrekEdit from '../views/AdminTrekEdit.vue'
import Bookings from '../views/AdminBooking.vue'
import Logout from '../views/Logout.vue'
import StaffDashboard from '../views/StaffDashboard.vue'
import StaffProfile from '../views/StaffProfile.vue'
import AdminTrekEdit from '../views/AdminTrekEdit.vue'
import StaffTrek from '../views/StaffTrek.vue'
import StaffParticipants from '../views/StaffParticipants.vue'
import TrekkerDashboard from '../views/TrekkerDashboard.vue'
import TrekkerHistory from '../views/TrekkerHistory.vue'
import TrekkerProfile from '../views/TrekkerProfile.vue'
import TrekkerTrek from '../views/TrekkerTrek.vue'
import TrekDetails from '../views/TrekDetails.vue'
import TrekkerBadge from '../views/TrekkerBadge.vue'


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
  {path:'/staff/dashboard',component:StaffDashboard},
  {path:'/staff/profile',component:StaffProfile},
  {path:'/staff/participants',component:StaffParticipants},
  {path:'/admin/trek/edit',component:AdminTrekEdit},
  {path:'/staff/treks/:id',component:StaffTrek},
  {path:'/trekker/dashboard',component:TrekkerDashboard},
  {path:'/trekker/history',component:TrekkerHistory},
  {path:'/trekker/profile',component:TrekkerProfile},
  {path:'/trekker/trek',component:TrekkerTrek},
  {path:'/trek/details/:id',component:TrekDetails},
  {path:'/trekker/badge',component:TrekkerBadge},
  {path:'/logout', component:Logout}

]
const router=createRouter({
  history: createWebHistory(),
  routes
})
export default router


