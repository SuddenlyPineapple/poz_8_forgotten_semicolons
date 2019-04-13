<template>
  <div id="app" class="marg-56">
    <v-app>
      <Toolbar/>
      <Drawer/>
      <router-view></router-view>
    </v-app>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';
import Toolbar from './components/Toolbar.vue';
import Drawer from './components/Drawer.vue';

@Component({
  components : {
      Toolbar,
      Drawer
  }
})

export default class App extends Vue {
  public items = [
    { title: 'Home', path: '/'},
    { title: 'Moje Paczki', path: '/moje_paczki'},
    { title: 'Paczka', path: '/paczka/:pid'},
    { title: 'O nas', path: '/about'}
  ];
}

</script>
<style lang="scss">
  div#app {
    font-family: "Roboto";
  }
  v-navigation-drawer {
    min-height: 200px
  }
  .marg-56 {
    margin-top: 56px
  }
</style>
