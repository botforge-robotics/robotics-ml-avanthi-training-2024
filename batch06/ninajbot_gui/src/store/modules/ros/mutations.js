import ROSLIB from "roslib";
import store from "@/store";
export const changeRoboConnectionStatus = (state, payload) => {
  state.roboConnectionStatus = payload;
};
export const vel_pub = (state) => {
  state.vel_pub = state.ros.Topic({
    ros: state.ros,
    name: "/cmd_vel",
    messageType: "geometry_msgs/Twist",
  });
};
export const eyes_pub = (state) => {
  state.eyes_pub = state.ros.Topic({
    ros: state.ros,
    name: "/ninjabot/eyes",
    messageType: "ninjabot_msgs/Eyes",
  });
};
export const focus_light_pub = (state) => {
  state.focus_light_pub = state.ros.Topic({
    ros: state.ros,
    name: "/ninjabot/focus_lights",
    messageType: "ninjabot_msgs/Focus_lights",
  });
};
export const lcd_pub = (state) => {
  state.lcd_pub = state.ros.Topic({
    ros: state.ros,
    name: "/ninjabot/lcd",
    messageType: "ninjabot_msgs/Lcd",
  });
};
export const body_ws2812b_pub = (state) => {
  state.body_ws2812b_pub = state.ros.Topic({
    ros: state.ros,
    name: "/ninjabot/body_strip",
    messageType: "ninjabot_msgs/Ws2812b_strip",
  });
};
export const left_ws2812b_pub = (state) => {
  state.left_ws2812b_pub = state.ros.Topic({
    ros: state.ros,
    name: "/ninjabot/left_strip",
    messageType: "ninjabot_msgs/Ws2812b",
  });
};
export const right_ws2812b_pub = (state) => {
  state.right_ws2812b_pub = state.ros.Topic({
    ros: state.ros,
    name: "/ninjabot/right_strip",
    messageType: "ninjabot_msgs/Ws2812b",
  });
};
export const publishVel = (state, payload) => {
  var twist = new ROSLIB.Message({
    linear: {
      x: Number(payload.linear),
      y: 0,
      z: 0,
    },
    angular: {
      x: 0,
      y: 0,
      z: Number(payload.angular),
    },
  });
  state.vel_pub.publish(twist);
};
export const publishEyes = (state, payload) => {
  var msg = new ROSLIB.Message({ type: String(payload.data) });
  state.eyes_pub.publish(msg);
  store.commit("showToast", {
    time: Date.now().toString(),
    message: `Eyes message published! > "${payload.data}".`,
  });
};
export const publishFocuslights = (state, payload) => {
  var msg = new ROSLIB.Message({
    right_light: Boolean(payload.right),
    left_light: Boolean(payload.left),
  });
  state.focus_light_pub.publish(msg);
  store.commit("showToast", {
    time: Date.now().toString(),
    message: `Focus lights message published! "Left:"${payload.left ? "ON" : "OFF"
      },"Right:"${payload.right ? "ON" : "OFF"}`,
  });
};
export const publishLcd = (state, payload) => {
  var msg = new ROSLIB.Message({
    message: String(payload.message == "" ? " " : payload.message),
    row: Number(payload.row),
  });
  state.lcd_pub.publish(msg);
  store.commit("showToast", {
    time: Date.now().toString(),
    message: `Lcd message published! "${payload.message}" to line ${payload.row}.`,
  });
};
export const publishBodyStrip = (state, payload) => {
  var msg = new ROSLIB.Message({ ...payload });
  state.body_ws2812b_pub.publish(msg);
  store.commit("showToast", {
    time: Date.now().toString(),
    message: `Body strip message published!.`,
  });
};

export const publishLeftStrip = (state, payload) => {
  var msg = new ROSLIB.Message({ ...payload });
  state.left_ws2812b_pub.publish(msg);
  store.commit("showToast", {
    time: Date.now().toString(),
    message: `Left strip message published!.`,
  });
};

export const publishRightStrip = (state, payload) => {
  var msg = new ROSLIB.Message({ ...payload });
  state.right_ws2812b_pub.publish(msg);
  store.commit("showToast", {
    time: Date.now().toString(),
    message: `Right strip message published!.`,
  });
};

export const updateRobotIP = (state, payload) => {
  state.robotIP = payload.data;
};

export const updateEyes = (state, payload) => {
  state.eyes = payload.data;
};
export const updateFocusLight = (state, payload) => {
  state.focusLight.left = payload.left;
  state.focusLight.right = payload.right;
};
export const updateLcd = (state, payload) => {
  state.lcd.message = payload.message;
  state.lcd.row = payload.row;
};
export const updateBodyStrip = (state, payload) => {
  state.body_ws2812b = { ...payload };
};
export const updateLeftStrip = (state, payload) => {
  state.left_ws2812b = { ...payload };
};
export const updateRightStrip = (state, payload) => {
  state.right_ws2812b = { ...payload };
};
export const updateNodesList = (state, payload) => {
  state.nodesList = { ...payload };
};
export const updateTopicsList = (state, payload) => {
  state.topicsList = { ...payload };
};
export const updateServicesList = (state, payload) => {
  state.servicesList = { ...payload };
};
export const updateActionServersList = (state, payload) => {
  state.actionsServersList = { ...payload };
};
export const updateParamsList = (state, payload) => {
  state.paramsList = { ...payload };
};
export const updateMappingNodeStatus = (state, payload) => {
  state.running_map_node = payload;
};
export const updateNavNodeStatus = (state, payload) => {
  state.running_nav_node = payload;
};
export const updateImageTopicName = (state, payload) => {
  state.image_topic_name = payload;
};
export const addToLogs = (state, payload) => {
  state.logs.unshift({ ...payload });
  if (state.logs.length > 100) state.logs.pop();
};
export const set_max_allowed_linear_vel = (state, payload) => {
  state.max_allowed_linear_vel = payload;
};
export const set_max_allowed_angular_vel = (state, payload) => {
  state.max_allowed_angular_vel = payload;
};
export const set_max_linear_vel = (state, payload) => {
  state.max_linear_vel = payload;
};
export const set_max_angular_vel = (state, payload) => {
  state.max_angular_vel = payload;
};
