import Vue from 'vue'
import Router from 'vue-router'
import Match from '@/components/match.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Match',
      component: Match
    }
  ]
})
