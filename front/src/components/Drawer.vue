<template>
    <v-navigation-drawer v-model="drawer" app dark temporary >
      <v-flex xs12 class="text-xs-center my-4">
          <v-avatar :size="100" color="grey lighten-4 my-4">
            <img src="https://avatars2.githubusercontent.com/u/19464921?s=460&v=4" alt="avatar">
          </v-avatar>
          <div class="title white--text">John Doe</div>
          <div><a href="mailto:john-doe@gmail.com">john-doe@gmail.com</a></div>
      </v-flex>

      <v-divider></v-divider>
      <v-list>
        <v-list-tile
          v-for="(route, i) in routes"
          :key="i"
          :to="route.to"
          :href="route.to"
          @click="onClick($event, route)"
        >
          <v-list-tile-title v-text="route.text"/>
        </v-list-tile>
      </v-list>
      <h1 class="absolute-logo white--text"><span class="orange--text">Alle</span>Paczka</h1> 
    </v-navigation-drawer>
</template>

<script lang="js">
  import {Vue, Component, Prop} from 'vue-property-decorator';
  import { mapGetters, mapMutations } from 'vuex';

  export default {
    name: 'Drawer',
    computed: {
      ...mapGetters(['routes']),
      drawer: {
        get() {
          return this.$store.state.drawer;
        },
        set(val) {
          this.setDrawer(val);
        }
      }
    },
    methods: {
      ...mapMutations(['setDrawer']),
      onClick(e, item) {
        e.stopPropagation();
        if (item.to === '/') {
          this.$vuetify.goTo(0);
          this.setDrawer(false);
          return;
        }
        if (item.to || !item.href) { return; }
        this.$vuetify.goTo(item.href);
        this.setDrawer(false);
      }
    }
  };
</script>

<style lang="scss">

.absolute-logo {
  position: absolute;
  bottom: 5%;
  left: 20px;
}

.v-list__tile--active {
  color: orange !important;
  caret-color: orange !important;
}
.center {
  text-align: center;
}

</style>
