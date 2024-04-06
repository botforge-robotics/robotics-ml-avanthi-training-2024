<template>
  <div class="camera_container mt-4">
    <img id="camera" :src="stream_link" />
    <div class="btn-group dropend">
      <button
        type="button"
        class="btn btn_orange drop_down_btn"
        data-bs-toggle="dropdown"
        aria-expanded="false"
      >
        <font-awesome-icon :icon="['fas', 'gear']"  style="color: white"/>
      </button>
      <ul class="dropdown-menu">
        <li>
          <button
            class="dropdown-item"
            type="button"
            :class="{ active: this.image_topic_name == topic }"
            v-for="(topic, index) in image_topics_list"
            @click="setImageTopic(topic)"
             :key="index"
          >
            {{ topic }}
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      img_listner: null,
      image_topics_list: ["/"],
      stream_link: "http://",
    };
  },
  computed: {
    ...mapGetters(["ros", "robotIP"]),
    image_topic_name: {
      get() {
        return this.$store.getters.image_topic_name;
      },
      set(value) {
        this.$store.commit("updateImageTopicName", value);
      },
    },
  },
  methods: {
    setImageTopic(topic){
      this.image_topic_name = topic;
      this.subscribeImage(topic);
    },
    subscribeImage(topic) {
      //   this.img_listner = this.ros.Topic({
      //     ros: this.ros,
      //     name: topic,
      //     messageType: "sensor_msgs/CompressedImage",
      //   });
      //   this.img_listner.subscribe(function (m) {
      //     document.getElementById("camera").src =
      //       "data:image/jpg;base64," + m.data;
      //   });
      var to = topic.lastIndexOf("/");
      to = to == -1 ? topic.length : to + 1;
      topic = topic.substring(0, to - 1);
      this.stream_link =
        "http://" + this.robotIP + ":9000/stream?topic=" + topic;
    },
    // unSubscribeImage() {
    //   this.img_listner.unsubscribe();
    // },
  },
  mounted() {
    let vm = this;
    // this.subscribeImage(this.image_topic_name);
    this.ros.getTopicsForType(
      "sensor_msgs/CompressedImage",
      (data) => {
        vm.image_topics_list = [...data];
      },
      () => {}
    );
    var to = this.image_topic_name.lastIndexOf("/");
    to = to == -1 ? this.image_topic_name.length : to + 1;
    this.stream_link =
      "http://" +
      this.robotIP +
      ":9000/stream?topic=" +
      this.image_topic_name.substring(0, to - 1);
  },
  // unmounted() {
  //   this.unSubscribeImage();
  // },
};
</script>

<style scoped>
.camera_container {
  position: fixed;
  width: 480px;
}
.camera_container > .btn-group {
  position: absolute;
  top: 10px;
  right: 5px;
}
#camera {
  width: 480px;
  height: 360px;
  border-radius: 10px;
  background-color: black;
}
</style>