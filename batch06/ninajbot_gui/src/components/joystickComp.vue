<template>
  <div id="zone_joystick"></div>
</template>

<script>
import { mapGetters, mapMutations } from "vuex";

export default {
  data() {
    return {
      manager: null,
      linear_speed: 0.0,
      angular_speed: 0.0,
      timer: null,
    };
  },
  computed: {
    ...mapGetters(["max_linear_vel", "max_angular_vel"]),
  },
  methods: {
    ...mapMutations(["publishVel"]),
  },
  mounted() {
    let vm = this;
    // declare nipple
    this.manager = require("nipplejs").create({
      zone: document.getElementById("zone_joystick"),
      color: "#F2771A",
      threshold: 0.1,
      mode: "static",
      size: 150,
      position: { left: 50 + "%", top: 50 + "%" },
    });
    // on nipple move start
    this.manager.on("start", function () {
      vm.timer = setInterval(function () {
        vm.publishVel({ linear: vm.linear_speed, angular: vm.angular_speed });
      }, 80);
    });
    //on nipple move end
    this.manager.on("end", function () {
      if (vm.timer) {
        clearInterval(vm.timer);
      }
      vm.publishVel({ linear: 0, angular: 0 });
    });
    // on nipple moving
    this.manager.on("move", function (event, nipple) {
      var max_distance = 75.0; // pixels;
      vm.linear_speed =
        (Math.sin(nipple.angle.radian) * vm.max_linear_vel * nipple.distance) /
        max_distance;
      vm.angular_speed =
        (-Math.cos(nipple.angle.radian) *
          vm.max_angular_vel *
          nipple.distance) /
        max_distance;
    });
  },
  unmounted() {
    clearInterval(this.timer);
  },
};
</script>

<style scoped>
#zone_joystick {
  position: fixed;
  right: 110px;
  bottom: 110px;
}

@media screen and (max-width: 1024px) {
  #joystick_img {
    width: 45vw;
  }
}
</style>