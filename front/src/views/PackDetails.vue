<template>
  <div>
    <v-data-table 
    :headers="headers" 
    :items="[onepackage]"
    >
        <template v-slot:items="props">
        <td>{{ props.item.pack_id }}</td>
        <td class="text-xs-right">{{ props.item.date_sent }}</td>
        <td class="text-xs-right">{{ props.item.date_deli }}</td>
        <td class="text-xs-right">{{ props.item.product.name }}</td>
        <td class="text-xs-right" :date="props.item.date_deli"><h3 class="orange--text">{{ timeNow }}</h3></td>
        </template>
    </v-data-table>
    <div id="map">
        <gmap-map :center="center" :zoom="6.5" :options="{ styles: styles }" style="width: 100%; height:500px" >
            <gmap-polyline :path.sync="path" :options="{ strokeColor:'#E65100'}">
            </gmap-polyline>

        <GmapMarker
            v-for="(m, index) in onepackage.route"
            :key="index"
            :position="{lat:m.x, lng: m.y}"
            :clickable="true"
        />

        <!-- Curr Cord -->
        <GmapMarker
            :position="{lat:currCord.curr_coord[0], lng: currCord.curr_coord[1]}"
            :clickable="true"
            :icon="{ url: require('./../../assets/img/marker-a.png')}"
            :show="isOpen"
        />

        </gmap-map>
    </div>
     <v-card
        class="mx-auto"
        min-height="400px"
    >
     <v-card-text class="py-0">
        <v-timeline align-top dense >

            <v-timeline-item color="orange" small v-for="item in onepackage.route"  :key="item.name">
                <v-layout pt-3>
                    <v-flex xs3>
                    <strong>{{ item.date }}</strong>
                    </v-flex>
                    <v-flex>
                    <strong>{{ item.name }}</strong>
                    <div class="caption">DHL</div>
                    </v-flex>
                </v-layout>
            </v-timeline-item>
    
        </v-timeline>
     </v-card-text>
    </v-card>
  </div>
</template>

<script lang="js">
import {Vue, Component, Prop} from 'vue-property-decorator';
import { mapGetters, mapMutations } from 'vuex';
import axios from 'axios';
import moment from 'moment';
import * as VueGoogleMaps from 'vue2-google-maps';

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCkF7rIDbq8WFxWv8i09_dpeTkf1ueXwRA',
    libraries: 'places'
  }
});

export default Vue.extend({
   props: ['pid'],
   data() {
    return {
        headers: [
          { text: 'Numer Paczki', align: 'left', sortable: false, value: 'pack_id'},
          { text: 'Data Nadania', align: 'right', sortable: false, value: 'date_sent' },
          { text: 'Data Odbioru', align: 'right', sortable: false, value: 'date_deli' },
          { text: 'Przedmiot', align: 'right', sortable: false, value: 'product' },
          { text: 'Licznik', align: 'right', sortable: false, value: 'timeNow' }
        ],
        onepackage: [],
        timeNow: moment(new Date().getTime()).format('mm:ss'),
        timeArr: '',
        coordinates: [],
        center: { lat:  52.125736, lng: 19.080392 },
        markers: [],
        places: [],
        currentPlace: null,
        path: [],
        currCord: [],
        isOpen: true,
        styles: [
    {
        "featureType": "all",
        "elementType": "labels",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "saturation": 36
            },
            {
                "color": "#000000"
            },
            {
                "lightness": 40
            }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "color": "#000000"
            },
            {
                "lightness": 16
            }
        ]
    },
    {
        "featureType": "all",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "administrative",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 17
            },
            {
                "weight": 1.2
            }
        ]
    },
    {
        "featureType": "administrative.country",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#9e8972"
            }
        ]
    },
    {
        "featureType": "administrative.locality",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#c4c4c4"
            }
        ]
    },
    {
        "featureType": "administrative.neighborhood",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#ebaa63"
            }
        ]
    },
    {
        "featureType": "landscape",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 20
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 21
            },
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "poi.business",
        "elementType": "geometry",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#afaca8"
            },
            {
                "lightness": "0"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "visibility": "on"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "road.highway",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "color": "#afaca8"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 18
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#afaca8"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "road.arterial",
        "elementType": "labels.text.stroke",
        "stylers": [
            {
                "color": "#afaca8"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 16
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#999999"
            }
        ]
    },
    {
        "featureType": "transit",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 19
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "geometry",
        "stylers": [
            {
                "color": "#000000"
            },
            {
                "lightness": 17
            }
        ]
    }
]
      };
    },
    methods: {
        sendQuery() {
            axios
                .get('http://3.17.203.94:6060/paczka_info?id=' + this.pid)
                .then( (response) => {
                    this.onepackage = response.data;
                    this.timeArr = this.onepackage.date_deli;
                    this.path = this.onepackage.lines.map((x) =>
                        ({ lat: x[0], lng: x[1] })
                    );
                    // const leg = this.path.length;
                    // if (leg > 1) {
                    //     this.center = this.path[leg / 2];
                    // }
                    // const bounds = new google.maps.LatLngBounds();
                    // for (const sciezka of this.path) {
                    //     bounds.extend(sciezka);
                    // }
                    // this.$refs.gmap.$mapObject.fitBounds(bounds);
                    // this.$refs.gmap.$mapObject.panToBounds(bounds);
                    // this.$refs.gmap.$mapCreated.then((map) => {
                    //         map.fitBounds(bounds);
                    // });
                });
        },
        geolocate: () => {
            navigator.geolocation.getCurrentPosition( (position) => {
                this.center = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
                };
            });
        },
        getCurrState() {
            axios
                .get('http://3.17.203.94:6060/paczka_stan?id=' + this.pid)
                .then( (response) => {
                    this.currCord = response.data;
                });
        }
    },
    mounted() {
        this.sendQuery();
        window.setInterval(() => {
            const dateEnd = moment(this.timeArr);
            const dateNow = moment();
            const diff = dateEnd.diff(dateNow);
            this.timeNow = 'Dni: ' + moment(diff).format('DD HH:mm:ss');
        }, 1000);
        this.getCurrState();

        window.setInterval(() => {
            this.isOpen = !this.isOpen;
        }, 1000);
    },
});

</script>

<style lang="scss">
    .v-datatable__actions {
        display: none;
    }
    div.package-table {
        margin-top: 64px;
    }
</style>
