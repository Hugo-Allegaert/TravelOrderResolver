<template>
    <div class="trip-container">
         <div class="line-time">
                <span class="time">{{trip.departure_time.substr(0, 5)}}</span>
                <span class="city">{{start_name.substring(8)}}</span>
                <span class="detail">{{moment(trip.arrival_time, 'HH:mm').subtract(trip.departure_time, 'hours').format('H:mm')}}h</span>
            </div>
            <div class="line-time">
                <span class="time">{{trip.arrival_time.substr(0, 5)}}</span>
                <span class="city">{{end_name.substring(8)}}</span>
                <span class="detail">n° {{trip.trip_id}}</span>
            </div>
    </div>
</template>

<script>
export default {
  name: 'Trip',
  props: {
    trip: Object,
    start_name: String,
    end_name: String
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
    width: 12.5625rem;
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