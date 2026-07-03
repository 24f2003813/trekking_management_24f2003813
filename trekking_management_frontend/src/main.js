import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import axios from 'axios'

axios.defaults.baseURL='https://localhost:5000'
axios.defaults.headers.common['']

const app = createApp(App)
app.use(router)
app.mount('#app')
