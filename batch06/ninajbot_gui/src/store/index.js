import { createStore } from "vuex";
import rosStore from "./modules/ros/rosStore.js";
import common from "./common.js";
export default createStore({
  state: {},
  getters: {},
  mutations: {},
  actions: {},
  modules: {
    rosStore,
    common
  },
});
