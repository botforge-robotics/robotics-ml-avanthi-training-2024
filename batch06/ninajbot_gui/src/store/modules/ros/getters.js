export const isRoboConnected = (state) => {
  return state.roboConnectionStatus && state.ros.isConnected;
};
export const ros = (state) => {
  return state.ros;
};
export const robotIP = (state) => {
  return state.robotIP;
};
export const vel_pub = (state) => {
  return state.vel_pub;
};
export const eyes_pub = (state) => {
  return state.eyes_pub;
};
export const focus_light_pub = (state) => {
  return state.focus_light_pub;
};
export const lcd_pub = (state) => {
  return state.lcd_pub;
};
export const body_ws2812b_pub = (state) => {
  return state.body_ws2812b_pub;
};
export const left_ws2812b_pub = (state) => {
  return state.left_ws2812b_pub;
};
export const right_ws2812b_pub = (state) => {
  return state.right_ws2812b_pub;
};
export const eyes = (state) => {
  return state.eyes;
};
export const focusLight = (state) => {
  return state.focusLight;
};
export const lcd = (state) => {
  return state.lcd;
};
export const body_ws2812b = (state) => {
  return state.body_ws2812b;
};
export const left_ws2812b = (state) => {
  return state.left_ws2812b;
};
export const right_ws2812b = (state) => {
  return state.right_ws2812b;
};
export const nodesList = (state) => {
  return state.nodesList;
};
export const topicsList = (state) => {
  return state.topicsList;
};
export const servicesList = (state) => {
  return state.servicesList;
};
export const actionsServersList = (state) => {
  return state.actionsServersList;
};
export const paramsList = (state) => {
  return state.paramsList;
};
export const running_map_node = (state) => {
  return state.running_map_node;
};
export const running_nav_node = (state) => {
  return state.running_nav_node;
};
export const image_topic_name = (state) => {
  return state.image_topic_name;
};
export const logs = (state) => {
  return state.logs;
};
export const max_allowed_linear_vel = (state) => {
  return state.max_allowed_linear_vel;
};
export const max_allowed_angular_vel = (state) => {
  return state.max_allowed_angular_vel;
};
export const min_allowed_linear_vel = (state) => {
  return state.min_allowed_linear_vel;
};
export const min_allowed_angular_vel = (state) => {
  return state.min_allowed_angular_vel;
};
export const max_linear_vel = (state) => {
  return state.max_linear_vel;
};
export const max_angular_vel = (state) => {
  return state.max_angular_vel;
};
export const api_start_service_name = (state) => {
  return state.api_start_service_name;
};
export const api_stop_service_name = (state) => {
  return state.api_stop_service_name;
};
export const api_srv_type = (state) => {
  return state.api_srv_type;
};
