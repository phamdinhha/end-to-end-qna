import Vue from 'vue';
import VueRouter from 'vue-router';
import hpqaUI from '../components/hpqaUI.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'hpqaUI',
    component: hpqaUI,
  },
  {
    path: '/rawbert',
    name: 'hpqaUI',
    component: hpqaUI,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
