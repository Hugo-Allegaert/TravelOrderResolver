<template>
    <div>
        <div class="trip-container" v-on:click="expand = !expand">
            <div class="line-time">
                <span class="time">{{trip.time_start}}</span>
                <span class="city">{{trip.start.substring(8)}}</span>
                <span class="detail">{{moment(trip.time_end, 'HH:mm').subtract(trip.time_start, 'hours').format('H:mm')}}h</span>
            </div>
            <div class="line-time">
                <span class="time">{{trip.time_end}}</span>
                <span class="city">{{trip.end.substring(8)}}</span>
                <span class="detail" v-if="Object.keys(trip.trips).length - 1 == 0">direct</span>
                <span class="detail" v-else>{{Object.keys(trip.trips).length - 1}} correspondance</span>
            </div>
        </div>
        <div v-if="expand == true">
            <ul class="trip-detail-container">
                <li v-for="(i, idx) in trip.trips" :key="'detailtrip' + idx">
                    <div style='display: flex'>
                        <span class="detail-trip-time">{{moment(i.departure_time, 'HH:mm:ss').format('HH:mm')}}</span>
                        <div class="point"></div>
                        <span class="detail-trip-dest">{{i.departure_stop}}</span>
                    </div>
                    <div style='display: flex'>
                        <span class="detail-trip-duration">{{moment(i.arrival_time, 'HH:mm').subtract(i.departure_time, 'hours').format('H:mm')}}h</span>
                        <div class="border"></div>
                        <div class="detail-trip-card-container">
                            <div class="detail-trip-card">
                                <p>TER</p>
                                <p style="font-weight: bold">n° {{i.trip_id}}</p>
                            </div>
                        </div>
                    </div>
                    <div style='display: flex'>
                        <span class="detail-trip-time">{{moment(i.arrival_time, 'HH:mm:ss').format('HH:mm')}}</span>
                        <div class="point"></div>
                        <span class="detail-trip-dest">{{i.arrival_stop}}</span>
                    </div>
                    <div style='display: flex' v-if="idx < Object.keys(trip.trips).length - 1">
                        <span class="detail-trip-duration"></span>
                        <div class="correspondence-border"></div>
                        <div class="detail-trip-card-container">
                            <p class="correspondence">Correspondance {{moment(trip.trips[idx + 1].departure_time, 'HH:mm').subtract(i.arrival_time, 'hours').format('H:mm')}}h</p>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
  name: 'FullTrip',
  props: {
    trip: Object
  },
  data() {
      return {
          expand: false
      }
  }
}
</script>

<style scoped>
.trip-container {
    margin-top: 1em;
    background-color: #fff;
    border-width: 0.0625rem;
    border-color: #d6d3cd;
    border-style: solid;
    border-radius: 0.5rem;
    color: #000;
    padding: 1em;
    line-height: 1.5em;
    cursor: pointer;
}

.line-time {
    display: flex;
    text-align: left;
}

.time {
    font-weight: bold;
    flex: 0 0 3.125rem;
}

.city {
    text-transform: uppercase;
    display: flex;
    flex: 1 1 0%;
    margin-left: 0.625rem;
    min-width: 0px;
    white-space: nowrap;
    overflow: hidden;
}

.detail {
    color: rgb(123, 113, 98);
    font-size: 0.9em;
}

.trip-detail-container {
    flex: 0 1 0%;
    background: #f7f6f5;
    padding: 20px;
    border-radius: 5px;
}

.trip-detail-container li {
    display: flex;
    flex-direction: column;
    margin: 0px;
    padding: 0px;
    color: rgb(181, 23, 66);
    font-weight: bold;
}

.border {
    min-height: 150px;
    border-color: rgb(181, 23, 66);
    border-left-style: solid;
    border-left-width: 0.25rem;
    position: relative;
}

.correspondence-border {
    min-height: 75px;
    border-color: gray;
    border-left-style: dashed;
    position: relative;
}

.point {
    height: 0.75rem;
    width: 0.75rem;
    background-color: rgb(255, 255, 255);
    border-color: rgb(181, 23, 66);
    border-style: solid;
    border-width: 0.203125rem;
    border-radius: 50%;
    position: relative;
}

.detail-trip-time {
    display: flex;
    position: relative;
    margin: 0px;
    width: 4rem;
    -webkit-box-pack: end;
    justify-content: flex-end;
    padding-right: 1.25rem;
    text-align: right;
    flex-shrink: 0;
}

.detail-trip-dest {
    display: flex;
    position: relative;
    margin: 0px;
    flex-direction: column;
    padding-left: 1.25rem;
    -webkit-box-pack: start;
    justify-content: flex-start;
    color: rgb(181, 23, 66);
}

.detail-trip-duration {
    color: rgb(123, 113, 98);
    display: flex;
    position: relative;
    margin: 0px;
    width: 4rem;
    -webkit-box-pack: end;
    padding-right: 1.7rem;
    text-align: right;
    flex-shrink: 0;
    align-items: center;
    justify-content: right;
    font-size: 0.8em;
}

.detail-trip-card {
    font-size: 0.8em;
    font-weight: lighter;
    position: relative;
    padding: 10px;
    background-color: #fff;
    border-width: 0.0625rem;
    border-color: #d6d3cd;
    border-style: solid;
    border-radius: 0.5rem;
    color: #000;
}

.detail-trip-card-container {
    display: flex;
    align-items: center;
    padding: 10px    
}

.correspondence {
    color: gray;
    font-size: 0.8em;
}
</style>