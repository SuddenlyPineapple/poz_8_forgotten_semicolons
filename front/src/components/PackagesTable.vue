<template>
  <div>
    <v-data-table
        :headers="headers"
        :items="packages.paczki"
        class="elevation-1"
    >
        <template v-slot:items="props" :to="route.to" :href="route.to">
        <td>{{ props.item.pack_id}}</td>
        <td class="text-xs-right">{{ props.item.date_sent }}</td>
        <td class="text-xs-right">{{ props.item.date_deli }}</td>
        <td class="text-xs-right">{{ props.item.product.name }}</td>
        <td class="text-xs-right" :date="props.item.date_deli">{{ now }}</td>
        <td class="text-xs-center"><v-btn color="warning" :to="'/paczka/'+props.item.pack_id">Szczegóły</v-btn></td>
        </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';
import { mapGetters, mapMutations } from 'vuex';
import axios from 'axios';

export default Vue.extend({
   data() {
    return {
        headers: [
          { text: 'Numer Paczki', align: 'left', sortable: true, value: 'pack_id'},
          { text: 'Data Nadania', align: 'right', value: 'date_sent' },
          { text: 'Data Odbioru', align: 'right', value: 'date_deli' },
          { text: 'Przedmiot', align: 'right', value: 'product.name' },
          { text: 'Licznik', align: 'right', value: 'now' },
          { text: 'Szczegóły', align: 'right', sortable: false }
        ],
        packages: {},
        now: Math.trunc((new Date()).getTime() / 1000)
      };
    },
    methods: {
        sendQuery() {
            axios
                .get('http://3.17.203.94:6060/paczki?user=u0')
                .then( (response) => (this.packages = response.data));
        }
    },
    mounted() {
        this.sendQuery();
        window.setInterval(() => {
        this.now = Math.trunc((new Date()).getTime() / 1000);
        }, 1000);
    }
});

</script>