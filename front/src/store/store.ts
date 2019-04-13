import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

function getPackages() {
  axios
  .get('http://3.17.203.94:6060/paczki?user=u0').then((response) => {
      return response.data;
    }
  );
}

export default new Vuex.Store({
  state: {
    drawer: false,
    routes: [
      {
        text: 'Home',
        to: '/'
      },
      {
        text: 'Moje Paczki',
        to: '/moje_paczki'
      },
      {
        text: 'O nas',
        to: '/about'
      },
    ],
    packages: getPackages(),
  },
  getters: {
    routes: (state)  => {
      return state.routes;
    },
    packages: (state)  => {
      return state.packages;
    },
  },
  mutations: {
    setDrawer: (state, payload) => (state.drawer = payload),
    toggleDrawer: (state) => (state.drawer = !state.drawer),
    setPackages: (state, payload) => (state.packages = getPackages()),
  },
  actions: {

  }
});
