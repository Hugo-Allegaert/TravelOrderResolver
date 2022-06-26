<template>
    <div>
        <div class="header">
            <div class="header-trip">
                <span><i class="fas fa-map-marker-alt"></i> {{from}} <i class="fas fa-arrow-right"></i> {{to}}</span>
            </div>
            <div class="header-btn">
                <div class="header-date">
                    <i class="fas fa-calendar-week"></i>
                    <datepicker style="margin-left: 10px" class="input-date" :open-date="this.openDate" :format="customFormatter" :highlighted="this.highlighted" :disabled-dates="disabledDates" placeholder="Select date" v-model="date" ></datepicker>
                </div>
                <a href="/" class="header-link">Nouvelle recherche</a>
            </div>
        </div>
        <div class="trips-container">
            <AvailableTrips :date="this.date" v-bind:all_trips="data.all_trips" v-bind:possible_trips="data.possible_trips"/>
        </div>
    </div>
</template>

<script>
import AvailableTrips from './AvailableTrips.vue';
import Datepicker from 'vuejs-datepicker';
import moment from 'moment'

export default {
    name: 'ListResult',
    props: {
        data: {
            all_trips: Array,
            possible_trips: Array
        },
    },
    components: {
        AvailableTrips,
        Datepicker
    },
    data() {
      return {
          date: new Date('2020-02-20'),
          openDate: new Date('2020-02-20'),
          from: '',
          to: '',
          highlighted: {
              dates: []
          },
          disabledDates: {
              customPredictor: function(date) {
                if(date.getFullYear() > 2020 || date.getFullYear() < 2020) {
                    return true
                }
                if (date.getMonth() + 1 < 2 || date.getMonth() + 1 > 5) {
                    return true
                }
            }
        }
      }
    },
    methods: {
        customFormatter(date) {
            return moment(date).format('DD/MM/YYYY');
        }
    },
    mounted () {
        this.from = this.data.all_trips[0]['start_name'].substring(8)
        this.to = this.data.all_trips[Object.keys(this.data.all_trips).length - 1]['end_name'].substring(8)
        let highlightedDates = []
        const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        this.data.possible_trips.forEach(el => {
            let start = moment(el.date_start)
            let end = moment(el.date_end)
            let current = start.clone()
            while (current.isSameOrBefore(end)) {
                if (el.days[days[current.day()]] == 1)  {
                    highlightedDates.push(new Date(current.format('YYYY-MM-DD')))
                }
                current = current.add(1, 'days')
            }
        });
        this.highlighted.dates = highlightedDates

        // Style datepicker
        const specificityHax = `
            .vdp-datepicker__calendar {
                transform: translateX(-68%) !important;
                color: #464645 !important;
            }

            .input-date input {
                border: none;
                color: white;
                background: inherit;
                font-size: 1em;
                width: calc(1em*6);
            }
        `;
        const style = document.createElement('style');
        if (style.styleSheet) style.styleSheet.cssText = specificityHax;
        else style.appendChild(document.createTextNode(specificityHax));
        document.getElementsByTagName('head')[0].appendChild(style);
    }
}
</script>

<style scoped>
.header {
    background-color: #ea542f;
    display: flex;
    padding: 1rem 1rem;
    justify-content: space-between;
    align-items: center;
}
.header {
    color: #fff;
}

.header-trip {
    font-weight: bold;
    font-size: 1.6rem;
}

.header-date {
    font-size: 1.6rem;
    display: flex;
    align-content: center;
    
    border-style: solid;
    border-radius: 25px;
    padding: 10px;
    border-width: 2px;
    align-items: center;
    font-size: 1em;
}

@media (min-width: 545px) and (max-width: 1024px) {
    .container, div:not(.container-sub-paragraph)>.sncf_strate__encart {
        padding: 0 5rem;
    }
}

.container, div:not(.container-sub-paragraph)>.sncf_strate__encart {
    width: 1000px;
    max-width: 100%;
    margin: 0 auto;
}

.vdp-datepicker__calendar {
    transform: translateX(-49%) !important;
    color: #464645 !important;
 }

 .header-btn {
     display: flex;
     align-items: center;
 }

 .header-link {
     color: white;
     background: inherit;
     font-size: 1em;
     width: calc(1em*6);
     border-style: solid;
     border-radius: 20px;
     border-width: 2px;
     text-decoration: none;
     padding: 5px;
     margin-left: 10px;
}

.trips-container {
    background-color: rgb(250, 250, 250);
}
</style>