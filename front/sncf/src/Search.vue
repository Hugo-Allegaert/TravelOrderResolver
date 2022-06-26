<template>
    <div class="search-container">
        <div v-if="!loading && data == null">
          <h1 style="color: black">Où souhaitez-vous aller ?</h1>
          <Voice v-model="text"/>
          <div v-if="error" class="error-container">
            <i class="fa-2x fas fa-info-circle"></i>
            <span style="margin-left: 10px">{{errormsg}}</span>
          </div>
          <div v-if="notfound" class="notfound-container">
            <i class="fa-2x fas fa-exclamation-triangle"></i>
            <span style="margin-left: 10px">{{notfoundmsg}}</span>
          </div>
        </div>
        <div v-if="loading">
          <div class="fa-3x">
            <i class="fas fa-spinner fa-pulse"></i>
          </div>
        </div>
        <div v-if="!loading && data != null">
          <h1 style="color: black">Ai-je bien compris ?</h1>
          <div class="verif-map-container">
            <Map :trips="this.data" />
          </div>
          <div class="btn-container">
            <a class="btn-validate" :href="`/trip?start=${start_id}&end=${end_id}`"><i class="fas fa-check"></i> OUI</a>
            <a class="btn-refuse" v-on:click="data = null, error = true, start_id = '', end_id = ''"><i class="fas fa-times"></i> NON</a>
          </div>
        </div>
    </div>
</template>

<script>
import Voice from './components/Voice.vue'
import Map from './components/Map.vue'
import axios from 'axios'

export default {
  name: 'Search',
  components: {
    Voice,
    Map
  },
  data() {
    return {
      text: '',
      loading: false,
      error: false,
      data: null,
      errormsg: "Faites une demande de trajet intelligible, comprennent une gare de départ et d'arriver situé en France.",
      notfound: false,
      notfoundmsg: "Oups, aucun trajet n'a été trouvé pour votre demande.",
      start_id: '',
      end_id: ''
    }
  },
  watch: {
    text: {
      immediate: true, 
      handler (val) {
        console.log(val)
        if (val != '') {
          this.loading = true
          axios.post('http://localhost:8000/travel-order', {'travel_order': val}).then(res => {
              const start_name = res.data.origins[0]
              const end_name = res.data.destinations[0]
              axios.get('http://localhost:8000/stops_info/start_name='+start_name+'&end_name='+end_name)
                .then(res => {
                  let data = res.data
                  this.data = [
                    {'start_name': data.start.stop_name, 'start_lat': data.start.stop_lat, 'start_lon': data.start.stop_lon},
                    {'end_name': data.end.stop_name, 'end_lat': data.end.stop_lat, 'end_lon': data.end.stop_lon},
                    ]
                  this.start_id = data.start.stop_id
                  this.end_id = data.end.stop_id
                  this.error = false
                  this.loading = false
                })
                .catch(e => {
                  console.log(e)
                  this.error = true
                  this.notfound = true
                  this.loading = false
                })
          }).catch(e => {
            console.log(e)
            this.error = true
            this.loading = false
          })
        }
      }
    }
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
  margin: 0;
}
</style>

<style scoped>
.search-container {
  height: 83vh;
  padding: 10% 25% 0 25%;
  background-image: url("/img/bg.png");
}

.verif-map-container {
  width: 50%;
  height: 400px;
  box-shadow: 0 2px 1px -1px rgb(0 0 0 / 20%), 0 1px 1px 0 rgb(0 0 0 / 14%), 0 1px 3px 0 rgb(0 0 0 / 12%);
}

.btn-container {
  margin-top: 20px;
  display: flex;
  justify-content: space-around;
}

.btn-validate {
  text-decoration: none;
  padding: 10px;
  color: white;
  background-color: #26a69a;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 1px -1px rgb(0 0 0 / 20%), 0 1px 1px 0 rgb(0 0 0 / 14%), 0 1px 3px 0 rgb(0 0 0 / 12%);
}

.btn-refuse {
  padding: 10px;
  color: white;
  background-color: #df405a;;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  box-shadow: 0 2px 1px -1px rgb(0 0 0 / 20%), 0 1px 1px 0 rgb(0 0 0 / 14%), 0 1px 3px 0 rgb(0 0 0 / 12%);
}

.error-container {
  margin-top: 20px;
  padding: 10px;
  background-color: #5296ec;
  color: white;
  border-radius: 20px;
  display: flex;
  align-items: center;
  opacity: 0.9;
}

.notfound-container {
  margin-top: 20px;
  padding: 10px;
  background-color: #ea542f;
  color: white;
  border-radius: 20px;
  display: flex;
  align-items: center;
  opacity: 0.9;
}
</style>