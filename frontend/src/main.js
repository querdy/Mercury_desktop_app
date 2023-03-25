import { createApp } from 'vue'
import Notifications from '@kyvg/vue3-notification'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


createApp(App)
    .use(router)
    .use(Notifications)
    .mount('#app')

