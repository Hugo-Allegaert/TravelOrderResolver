<template>
  <div>
    <Loader v-if="loading == true"/>
    <ListResult v-bind:data="data" :from="'Nantes'" :to="'Paris'" v-if="loading == false && error == false"/>
    <div v-if="error == true">
      ERROR 500
    </div>
  </div>
</template>

<script>
import ListResult from './components/ListResults.vue'
import Loader from './components/Loader.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    ListResult,
    Loader
  },
   data () {
    return {
      data: '',
      loading: true,
      error: false
    }
  },
  mounted () {
    const urlParams = new URLSearchParams(window.location.search)
    const start_id = urlParams.get('start')
    const end_id = urlParams.get('end')
    this.loading = true
    console.log('http://localhost:8000/trip/start_id='+start_id+'&end_id='+end_id)
     axios
      .get('http://localhost:8000/trip/start_id='+start_id+'&end_id='+end_id)
      .then(response => {
        console.log(response)
        this.data = response.data
        this.loading = false
      })
      .catch(e => {
        console.log(e)
        this.error = true
        this.loading = false
      })
  }
}
</script>

<style>
body {
  font-family: 'Comfortaa', cursive;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background: rgb(250, 250, 250);
  color:  #ea542f;
  text-align: center;
}
</style>