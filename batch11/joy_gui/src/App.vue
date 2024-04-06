<template>
  <home-view></home-view>
</template>

<script>
import HomeView from "./views/HomeView.vue";
export default {
  data() {
    return {
      property: "value",
    };
  },
  components: {
    HomeView,
  },
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  overflow-y: hidden;
  background-color: #181623;
  height: 100vh;
}
body {
  background-color: #181623;
  overflow-y: hidden;
}
</style>
