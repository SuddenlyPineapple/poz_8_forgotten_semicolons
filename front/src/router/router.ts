import Vue from 'vue';
import Router from 'vue-router';
import HomePage from '../views/HomePage.vue';
import MyPacks from '../views/MyPacks.vue';
import About from '../views/About.vue';
import PackDetails from '../views/PackDetails.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
      {
        path: '/',
        component: HomePage,
        name: 'Home'
      },
      {
        path: '/moje_paczki',
        component: MyPacks,
        name: 'Moje Paczki'
      },
      {
        path: '/about',
        component: About,
        name: 'O nas'
      },
      {
        path: '/paczka/:pid',
        component: PackDetails,
        props: true,
        name: 'Paczka'
      }
  ]
});
