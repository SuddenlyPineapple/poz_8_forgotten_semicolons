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
  </div>
</template>

<script lang="js">
import {Vue, Component, Prop} from 'vue-property-decorator';
import { mapGetters, mapMutations } from 'vuex';
import axios from 'axios';
import moment from 'moment';

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
        timeArr: ''
      };
    },
    methods: {
        sendQuery() {
            axios
                .get('http://3.17.203.94:6060/paczka_info?id=' + this.pid)
                .then( (response) => {
                    this.onepackage = response.data;
                    this.timeArr = this.onepackage.date_deli;
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
