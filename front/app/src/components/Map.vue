<template>
<div class="map-container">
    <l-map :center="center" :zoom="zoom" class="map" ref="map" style="width: inherit; height: inherit; z-index: 1;" @update:zoom="zoomUpdated" @update:center="centerUpdated">
        <l-tile-layer :url="url"></l-tile-layer>
        <div v-for="(icon, idx) in this.icons" :key="'icon'+idx">
         <l-marker :lat-lng="icon['coord']">
            <l-icon ref="icon">
                <img class="icon" :src="icon['img']"/>
            </l-icon>
            <l-popup>
                <div>
                    {{icon['label']}}
                </div>
            </l-popup>
         </l-marker>
        </div>
        <l-polyline :lat-lngs="polyline"/>
   </l-map>
</div>
</template>

<script>
import { LMap, LTileLayer, LIcon, LMarker, LPopup, LPolyline } from 'vue2-leaflet';
import { latLng } from "leaflet";
import 'leaflet/dist/leaflet.css';

export default {
    components: {
        LMap,
        LTileLayer,
        LMarker,
        LIcon,
        LPopup,
        LPolyline
    },
   props: {
     trips: Array
    },
    data () {
        return {
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            center: [ 47.081012, 2.398782 ],
            zoom: 6,
            withPopup: latLng(47.41322, 2.398782),
            icons: [],
            polyline: []
        }
    },
    methods: {
        zoomUpdated (zoom) {
            this.zoom = zoom;
        },
        centerUpdated (center) {
            this.center = center;
        }
    },
    mounted () {
        var BreakException = {};
        try {
            let new_icon = {'label': 'Départ : ', 'coord': ''}
                new_icon['coord'] = latLng(this.trips[0].start_lat, this.trips[0].start_lon)
                new_icon['label'] += this.trips[0].start_name
                new_icon['img'] = '/starticon.png'
                this.icons.push(new_icon)
                this.polyline.push(latLng(this.trips[0].start_lat, this.trips[0].start_lon))
            this.trips.forEach((el, idx) => {
                if (idx == Object.keys(this.trips).length) {
                    throw BreakException;
                }
                if (idx > 0) {
                    let new_icon = {'label': 'Correspondance : ', 'coord': ''}
                    new_icon['coord'] = latLng(el.start_lat, el.start_lon)
                    new_icon['label'] += el.start_name
                    new_icon['img'] = '/stopicon.png'
                    this.icons.push(new_icon)
                    this.polyline.push(latLng(el.start_lat, el.start_lon))
                }
            });
        } catch (e) {
            if (e !== BreakException) throw e;
        }
        let new_icon = {'label': 'Arrivé : ', 'coord': ''}
        new_icon['coord'] = latLng(this.trips[Object.keys(this.trips).length - 1].end_lat, this.trips[Object.keys(this.trips).length - 1].end_lon)
        new_icon['label'] += this.trips[Object.keys(this.trips).length - 1].end_name
        new_icon['img'] = '/endicon.png'
        this.icons.push(new_icon)
        this.polyline.push(latLng(latLng(this.trips[Object.keys(this.trips).length - 1].end_lat, this.trips[Object.keys(this.trips).length - 1].end_lon)))
    }
}
</script>

<style>
 .map {
   position: absolute;
   overflow: hidden
 }

.map-container {
    width: inherit;
    height: inherit;
    z-index: 1;
}

.icon {
    width: 30px;
    margin-left: -8px;
    margin-top: -20px;
}
</style>