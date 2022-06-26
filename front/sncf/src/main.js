import App from './App.vue'
import Search from './Search.vue'
import Vue from 'vue/dist/vue.js'
import moment from 'moment'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

Vue.prototype.moment = moment

const NotFound = { template: '<p>Page not found</p>' }

const routes = {
  '/': Search,
  '/trip': App
}

new Vue({
  el: '#app',
  data() {
    return {
      currentRoute: window.location.pathname
    }
  },
  computed: {
    ViewComponent () {
      return routes[this.currentRoute] || NotFound
    }
  },
  render (h) { return h(this.ViewComponent) }
})

