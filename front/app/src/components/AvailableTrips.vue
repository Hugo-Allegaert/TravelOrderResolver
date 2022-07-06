<template>
    <div class="container-list">
        <span style="display: none">{{date}}</span>
        <Collapsable :title="'Carte de l\'itinéraire'" :collapse="true">
            <div class="container-map">
                <Map :trips="all_trips" />
            </div>
        </Collapsable>

        <div class="divider"></div>
        <Collapsable :title="'Trajets Suggérés'" :collapse="true">
            <div v-if="availableTrip">
                <div v-for="(trip, idx) in possible_trips" :key="'sugestedtrip' + idx">
                    <FullTrip v-if="fullComputedDate >= trip.date_start && fullComputedDate <= trip.date_end && trip.days[day] == '1'" :trip="trip"/>
                </div>
            </div>
            <div v-else class="empty-res">
                <i class="fas fa-exclamation-triangle"></i>
                <div style="margin-left: 20px">
                    <span>Votre demande n’a pu aboutir pour la date sélectionné. Veuillez en choisir une différente.</span><br/>
                    <span> Merci de votre compréhension.</span>
                </div>
            </div>
        </Collapsable>

        <div class="divider"></div>
        <Collapsable :title="'Autres Itinéraires'" :collapse="false">
            <div v-for="(i, idx) in all_trips" :key="'other' + idx">
                <div class="trip-title">Trajets {{i.start_name}} <i class="fas fa-arrow-right"></i> {{i.end_name}}</div>
                <div v-for="(trip, j) in i.trips" :key="'othertrip' + j">
                    <Trip v-if="computedDate >= trip.start_date && computedDate <= trip.end_date && trip[day] == '1'" :trip="trip" :start_name="i.start_name" :end_name="i.end_name"/>
                </div>
                <div class="divider"></div>
            </div>
        </Collapsable>
    </div>
</template>

<script>
import Trip from './Trip.vue'
import FullTrip from './FullTrip.vue'
import Collapsable from './Collapsable.vue'
import moment from 'moment'
import Map from './Map.vue'

export default {
  name: 'AvailableTrips',
  components: {
    Trip,
    FullTrip,
    Collapsable,
    Map
  },
  props: {
    date: Date,
    all_trips: Array,
    possible_trips: Array
  },
  data() {
      return {
          availableTrip: false
      }
  },
  watch: {
    date: {
        immediate: true, 
        handler (val) {
            const days = {0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday'}
            if (val !== null) { 
                let d = new Date(val);
                this.computedDate = moment(val).format('YYYYMMDD')
                this.fullComputedDate = moment(val).format('YYYY-MM-DD')
                this.day = days[d.getDay()]
            }

            this.availableTrip = false
            this.possible_trips.forEach(trip => {
                if (this.fullComputedDate >= trip.date_start && this.fullComputedDate <= trip.date_end && trip.days[this.day] == '1') {
                    this.availableTrip = true
                }
            });
        }
    }
  }
}
</script>

<style scoped>
.container-list {
    margin: 20px 20px 20px 20px;
    text-align: left;
    color: black;
    overflow: hidden;
    padding: 0 12% 0 12%;
}

.trip-title {
    font-size: 1.2em;
    font-weight: bold;
    margin-top: 1em;
}

.divider {
    margin-top: 50px;
}

.empty-res {
    display: flex;
    padding: 20px;
    align-items: center;
    background-color: #fff0ed;
    color: #d9002e;
    border-radius: 10px;
}

.container-map {
    height: 500px;
    width: 73%;
    box-shadow: 0 2px 1px -1px rgb(0 0 0 / 20%), 0 1px 1px 0 rgb(0 0 0 / 14%), 0 1px 3px 0 rgb(0 0 0 / 12%);
}
</style>
