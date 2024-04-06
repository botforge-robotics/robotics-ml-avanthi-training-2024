<template>
  <nav class="navbar navbar-expand-lg bg-light fixed-top">
    <div class="container-fluid">
      <div>
        <img
          class="navbar-brand"
          src="./assets/images/logo.png"
          alt="UnReal Robotics"
          width="250"
        />
      </div>
      <h2 style="marginright: 14rem">AMR</h2>
      <div></div>
    </div>
    <div class="d-flex">
     <input
            class="form-control me-2"
            placeholder="Robot IP"
            id="ip-input"
            v-model="robotIp"
            :disabled="isRoboConnected"
          />
      <button
        v-if="isRoboConnected"
        class="icon-btn btn btn-danger"
        @click="() => {}"
      >
        <font-awesome-icon
          :icon="['fas', 'power-off']"
          size="lg"
          style="color: white"
        />
      </button>
      <button
        v-if="!isRoboConnected"
        class="icon-btn btn btn-success"
        @click="
          connectRobot('ws://' + this.robotIp + ':9090');
          updateRobotIP({ data: this.robotIp });
        "
      >
        <font-awesome-icon
          :icon="['fas', 'link']"
          shake
          size="lg"
          style="color: white"
        />
      </button>
      <button
        v-if="isRoboConnected"
        class="icon-btn btn btn-danger"
        @click="disconnectRobot"
      >
        <font-awesome-icon
          :icon="['fas', 'link-slash']"
          size="lg"
          style="color: white"
        />
      </button>
    </div>
  </nav>
  <div class="page-container">
    <disconnectView v-if="!isRoboConnected"> </disconnectView>
    <homeView v-if="isRoboConnected"></homeView>
  </div>
</template>

<script>
import { mapGetters, mapActions, mapMutations } from "vuex";
import disconnectView from "./components/DisconnectedView.vue";
import homeView from "./views/HomeView.vue";
export default {
  data() {
    return {
      robotIp: "localhost",
      log_listner: null,
    };
  },
  components: {
    disconnectView,
    homeView,
  },
  computed: {
    ...mapGetters(["isRoboConnected", "ros"]),
  },
  methods: {
    ...mapActions(["connectRobot", "disconnectRobot", "addToLogsAction"]),
    ...mapMutations([
      "showToast",
      "vel_pub",
      "eyes_pub",
      "focus_light_pub",
      "lcd_pub",
      "body_ws2812b_pub",
      "left_ws2812b_pub",
      "right_ws2812b_pub",
      "updateRobotIP",
    ]),
  },

  mounted() {
    window.document.title = "tortoisebot GUI";
    //ros callbacks
    let vm = this;
    this.ros.on("connection", function () {
      console.log("Connected to websocket server.");
      //set topics
      vm.vel_pub();
      vm.eyes_pub();
      vm.focus_light_pub();
      vm.lcd_pub();
      vm.body_ws2812b_pub();
      vm.left_ws2812b_pub();
      vm.right_ws2812b_pub();
      vm.showToast({
        time: Date.now().toString(),
        message: "Connected to tortoisebot",
      });
    });

    this.ros.on("error", function (error) {
      console.log("Error connecting to websocket server: ", error);
    });

    this.ros.on("close", function () {
      console.log("Connection to websocket server closed.");
      vm.showToast({
        time: Date.now().toString(),
        message: "Disconnected from tortoisebot",
      });
    });

    // ros log
    this.log_listner = this.ros.Topic({
      ros: this.ros,
      name: "/rosout",
      messageType: "rosgraph_msgs/Log",
    });
    this.log_listner.subscribe(function (data) {
      vm.addToLogsAction({
        secs: data.header.stamp.secs,
        level: data.level,
        name: data.name,
        file: data.file,
        msg: data.msg,
      });
    });
  },
  unmounted() {
    this.log_listner.unsubscribe();
  },
};
</script>
<style></style>
