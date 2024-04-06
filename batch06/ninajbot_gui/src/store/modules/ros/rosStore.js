import ROSLIB from "roslib";
import * as actions from "./actions";
import * as getters from "./getters";
import * as mutations from "./mutations";

const strip = {
  h: 255,
  s: 255,
  v: 255,
  t: 10,
  animation: 1,
  reverse: false,
};
const state = {
  robotIP: "localhost",
  roboConnectionStatus: false,
  ros: new ROSLIB.Ros(),
  vel_pub: null,
  eyes_pub: null,
  focus_light_pub: null,
  lcd_pub: null,
  body_ws2812b_pub: null,
  left_ws2812b_pub: null,
  right_ws2812b_pub: null,
  eyes: "neutral",
  focusLight: {
    left: false,
    right: false,
  },
  lcd: {
    message: "",
    row: 0,
  },
  body_ws2812b: {
    front: { ...strip },
    rear: { ...strip },
    left: { ...strip },
    right: { ...strip },
    front_left: { ...strip },
    front_right: { ...strip },
    rear_left: { ...strip },
    rear_right: { ...strip },
    global_anim: false,
    body: { ...strip },
  },
  left_ws2812b: { ...strip },
  right_ws2812b: { ...strip },
  nodesList: {
    nodes: [],
    nodesCount: 0,
  },
  topicsList: {
    topics: [],
    topicsCount: 0,
  },
  servicesList: {
    services: [],
    servicesCount: 0,
  },
  actionsServersList: {
    servers: [],
    serversCount: 0,
  },
  paramsList: {
    params: [],
    paramsCount: 0,
  },
  running_map_node: false,
  running_nav_node: false,
  image_topic_name: "/raspicam_node/image/compressed",
  logs: [],
  max_allowed_linear_vel: 3.0,
  max_allowed_angular_vel: 3.0,
  min_allowed_linear_vel: 0.1,
  min_allowed_angular_vel: 0.05,
  max_linear_vel: 0.5,
  max_angular_vel: 1.0,
  api_start_service_name: "/tortoisebot_launcher_api_start",
  api_stop_service_name: "/tortoisebot_launcher_api_stop",
  api_srv_type: "tortoisebot_launcher_api/TortoisebotApi"
};
export default {
  state,
  getters,
  mutations,
  actions,
};
