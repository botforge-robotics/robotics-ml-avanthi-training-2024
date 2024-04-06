import bootstrap from "bootstrap/dist/js/bootstrap.js";
import TimeAgo from 'javascript-time-ago';
import en from 'javascript-time-ago/locale/en';
TimeAgo.addDefaultLocale(en);
// Create formatter (English).
const timeAgo = new TimeAgo('en-US');
const state = {
  toasts: [],
};
const getters = {
  toasts: (state) => {
    let toasts = [];
    for(let i=0; i<state.toasts.length;i++){
      toasts.push({time:timeAgo.format(Number(state.toasts[i].time)),message:state.toasts[i].message})
    }
    return toasts;
  },
};
const mutations = {
  showToast: (state, payload) => {
    state.toasts.push({ time: payload.time, message: payload.message });
    setTimeout(() => {
      const toastElList = document.querySelectorAll(".toast");
      const toastList = [...toastElList].map(
        (toastEl) => new bootstrap.Toast(toastEl)
      );
      for (let i = 0; i < toastList.length; i++) {
        toastList[i].show();
      }
    }, 500);
  },
  deleteToast: (state, index) => {
    state.toasts.splice(index, 1);
  },
};
const actions = {};

export default {
  state,
  getters,
  mutations,
  actions,
};
