<template>
  <v-toolbar app flat dark>
        <v-toolbar-side-icon 
          class="hidden-md-and-up" 
          @click="toggleDrawer"
          >
        </v-toolbar-side-icon>
        <v-toolbar-title><span class="orange--text">Alle</span>Paczka</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-sm-and-down">
          <v-btn v-for="(route,i) in routes" :key="i" 
            :to="route.to" 
            class="ml-0 hidden-sm-and-down"
            flat>
            {{route.text}}
          </v-btn>
        </v-toolbar-items>
  </v-toolbar>
</template>

<script>
import {mapGetters, mapMutations} from 'vuex';

export default {
  computed: {
    ...mapGetters(['routes'])
  },
  methods: {
    ...mapMutations(['toggleDrawer'])
  }
};

</script>
