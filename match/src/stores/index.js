import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    board: null
  },
  mutations: {
    storeBoard (state, board) {
      state.board = board
    }
  }
})
