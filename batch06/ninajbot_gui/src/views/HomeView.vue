<template>
  <div class="home-page">
    <div id="map_container"></div>
    <div id="noMapContainer" v-if="!running_map_node && !running_nav_node">
      <font-awesome-icon
        :icon="['fas', 'map-location-dot']"
        size="lg"
        style="color: #000000"
      />
    </div>
    <image-view></image-view>
    <joy-stick></joy-stick>
    <omnibar :speed="speed" :omni_title="omniTitle"></omnibar>
    <!-- buttons nav,map, save -->
    <div
      class="d-flex flex-column justify-content-between align-items-start mt-4 map_btns"
    >
      <div class="d-flex flex-column justify-content-evenly">
        <button
          type="button"
          data-bs-toggle="modal"
          data-bs-target="#savemap"
          class="btn text-white btn_black icon-btn"
          style="backgroundcolor: green"
          v-show="!running_nav_node && running_map_node"
        >
          <font-awesome-icon
            :icon="['fas', 'floppy-disk']"
            size="lg"
            style="color: #ffffff"
          />
        </button>
      </div>
    </div>
    <div
      class="d-flex flex-column justify-content-between align-items-start mt-4 navgation_btns"
    >
      <button
        type="button"
        class="btn icon-btn"
        :class="{
          btn_orange: !running_map_node,
          'btn-danger': running_map_node,
        }"
        @click="mapStartStop"
        :disabled="map_btn_busy"
        v-if="!running_nav_node"
      >
        <span
          class="spinner-grow spinner-grow-sm"
          role="status"
          aria-hidden="true"
          v-if="map_btn_busy"
        ></span>
        <font-awesome-icon
          :icon="['fas', 'map-location-dot']"
          size="lg"
          style="color: #ffffff"
          v-if="!map_btn_busy && !running_map_node"
        />
        <font-awesome-icon
          :icon="['fas', 'arrow-right-from-bracket']"
          size="lg"
          style="color: #ffffff"
          v-if="!map_btn_busy && running_map_node"
        />
      </button>
      <button
        type="button"
        class="btn icon-btn"
        data-bs-toggle="modal"
        data-bs-target="#navStartModal"
        :class="{
          btn_orange: !running_nav_node,
          'btn-danger': running_nav_node,
        }"
        v-if="!running_map_node"
      >
        <font-awesome-icon
          :icon="['fas', 'route']"
          size="lg"
          style="color: #ffffff"
          v-if="!running_nav_node"
        />
        <font-awesome-icon
          :icon="['fas', 'arrow-right-from-bracket']"
          size="lg"
          style="color: #ffffff"
          v-if="running_nav_node"
        />
      </button>

      <button
        type="button"
        class="btn text-white btn_orange icon-btn"
        data-bs-toggle="modal"
        data-bs-target="#settingsModal"
      >
        <font-awesome-icon
          :icon="['fas', 'gears']"
          size="lg"
          style="color: #ffffff"
        />
      </button>
    </div>
    <!-- Map Modal -->
    <div
      class="modal fade"
      id="savemap"
      tabindex="-1"
      aria-labelledby="savemapLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="savemapLabel">Save map?</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="row align-items-center">
              <div class="col-auto">
                <label for="mapName" class="col-form-label me-2"
                  >Map Name:</label
                >
              </div>
              <div class="col-auto">
                <input
                  id="map_name"
                  class="form-control"
                  v-model="map_name"
                  @input="v$.map_name.$touch()"
                />
              </div>
              <div class="col-auto">
                <span id="mapNameHelpInline" class="form-text">
                  Must be only alphabets, Min Length 4, Max Length 10.
                </span>
              </div>
            </div>

            <p v-if="v$.map_name.$error" class="text-danger fs-6">
              Invalid name!
            </p>
          </div>
          <div class="modal-footer">
            <button
              id="map_modal_close_btn"
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn btn_orange"
              :disabled="map_save_btn_busy || v$.map_name.$error"
              @click="saveMap"
            >
              <span
                class="spinner-grow spinner-grow-sm"
                role="status"
                aria-hidden="true"
                v-if="map_save_btn_busy"
              ></span>
              {{ map_save_btn_busy ? "Saving" : "save" }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- Nav Modal -->
    <div
      class="modal fade"
      id="navStartModal"
      tabindex="-1"
      aria-labelledby="navStartModalLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="navStartModalLabel">
              {{ running_nav_node ? "Stop navigation?" : "Start navigation?" }}
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body" v-if="!running_nav_node">
            <div class="d-flex flex-row align-items-center">
              <div class="col-auto mb-2">
                <label for="navMapName" class="col-form-label me-3"
                  >Map Name:
                </label>
              </div>
              <div class="col-auto">
                <input
                  id="navMapName"
                  class="form-control"
                  v-model="navMapName"
                  @input="v$.navMapName.$touch()"
                />
              </div>
            </div>
            <p v-if="v$.navMapName.$error" class="text-danger fs-6">
              Invalid name!
            </p>
          </div>
          <div class="modal-body" v-if="running_nav_node">...</div>
          <div class="modal-footer">
            <button
              id="nav_modal_close_btn"
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn me-5"
              @click="navStartStop"
              :disabled="v$.navMapName.$error"
              :class="{
                btn_orange: !running_nav_node,
                'btn-danger': running_nav_node,
              }"
            >
              <span
                class="spinner-grow spinner-grow-sm"
                role="status"
                aria-hidden="true"
                v-if="nav_btn_busy"
              ></span>
              {{
                nav_btn_busy
                  ? running_nav_node
                    ? "Stopping"
                    : "Starting"
                  : running_nav_node
                  ? "Stop Navigation"
                  : "Start Navigation"
              }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <settingsComp></settingsComp>
    <toast-comp></toast-comp>
  </div>
</template>

<script>
/* eslint-disable */
import imageView from "../components/imageView.vue";
import joyStick from "../components/joystickComp.vue";
import { mapGetters, mapMutations } from "vuex";
import { useVuelidate } from "@vuelidate/core";
import { required, alpha, minLength, maxLength } from "@vuelidate/validators";
import ROSLIB from "roslib/src/RosLib";
import omnibar from "../components/omniBar.vue";
import settingsComp from "../components/settingsComp.vue";
import toastComp from "../components/toastComp.vue";
export default {
  setup: () => ({ v$: useVuelidate() }),
  data() {
    return {
      map_btn_busy: false,
      startServiceClient: null,
      stopServiceClient: null,
      map_save_btn_busy: null,
      map_name: "play_arena",
      laser_listener: null,
      baseLink_tf_client: null,
      poseListner: null,
      nav_btn_busy: false,
      navMapName: "play_arena",
      navGoal: null,
      localPlannerName: "dwa",
      navRobotType: "real",
      base_footprint_tf: null,
      goalMarker: null,
      goalContainer: null,
      moveBaseActionClient: null,
      teb_local_path_topic: "/move_base/TebLocalPlannerROS/local_plan",
      teb_global_path_topic: "/move_base/TebLocalPlannerROS/global_plan",
      dwa_local_path_topic: "/move_base/DWAPlannerROS/local_plan",
      dwa_global_path_topic: "/move_base/DWAPlannerROS/global_plan",
      global_path_topic: "/move_base/NavfnROS/plan",
      global_path_shape: null,
      local_path_shape: null,
      global_path: null,
      local_path: null,
      poseEstimateBtn: false,
      initialPosePub: false,
      zoom_btn: false,
      pan_btn: false,
      goal_checkbox_btn: true,
      speed: 0.0,
      vel_sub: null,
    };
  },
  computed: {
    ...mapGetters([
      "ros",
      "running_map_node",
      "running_nav_node",
      "api_start_service_name",
      "api_stop_service_name",
      "api_srv_type",
    ]),
    omniTitle() {
      if (this.running_nav_node) return "Navigation";
      else if (this.running_map_node) return "Mapping";
      else return "Teleop";
    },
  },
  validations() {
    return {
      map_name: {
        required,
        alpha,
        minLengthValue: minLength(4),
        maxLengthValue: maxLength(10),
      },
      navMapName: {
        required,
        alpha,
        minLengthValue: minLength(4),
        maxLengthValue: maxLength(10),
      },
    };
  },
  components: {
    imageView,
    joyStick,
    omnibar,
    settingsComp,
    toastComp,
  },
  methods: {
    ...mapMutations([
      "updateMappingNodeStatus",
      "showToast",
      "updateNavNodeStatus",
    ]),
    saveMap() {
      this.map_save_btn_busy = true;
      var request = new ROSLIB.ServiceRequest({
        file: "map_saver",
        args: "map_name:=" + this.map_name.toLocaleLowerCase(),
      });
      let vm = this;
      this.startServiceClient.callService(request, function (result) {
        vm.map_save_btn_busy = false;
        let msg = "";
        if (result.success) {
          msg = `Saved ${vm.map_name} map!`;
          const modal_cl_btn = document.getElementById("map_modal_close_btn");
          modal_cl_btn.click();
        } else {
          msg = `Failed to save ${vm.map_name} map!`;
        }
        vm.showToast({
          time: Date.now().toString(),
          message: msg,
        });
      });
    },
    mapStartStop() {
      this.map_btn_busy = true;
      if (!this.running_map_node) {
        var request = new ROSLIB.ServiceRequest({
          file: "map",
          args: "scan_topic:=/scan",
        });
        let vm = this;
        this.startServiceClient.callService(request, function (result) {
          vm.map_btn_busy = false;
          let msg = "";
          if (result.success) {
            msg = "Started mapping!";
            vm.updateMappingNodeStatus(true);
          } else {
            msg = "failed Start mapping!!";
          }
          vm.showToast({
            time: Date.now().toString(),
            message: msg,
          });
        });
      } else {
        var request = new ROSLIB.ServiceRequest({
          file: "map",
          args: "scan_topic:=/scan",
        });
        let vm = this;
        this.stopServiceClient.callService(request, function (result) {
          vm.map_btn_busy = false;
          let msg = "";
          if (result.success) {
            msg = "Stopped mapping!";
            vm.updateMappingNodeStatus(false);
          } else {
            msg = "failed Stop mapping!!";
          }
          vm.showToast({
            time: Date.now().toString(),
            message: msg,
          });
        });
      }
    },
    startNavigation(file, args) {
      var request = new ROSLIB.ServiceRequest({
        file: file,
        args: args,
      });
      let vm = this;
      this.startServiceClient.callService(request, function (result) {
        vm.nav_btn_busy = false;
        let msg = "";
        if (result.success) {
          msg = "Started navigation!";
          vm.updateNavNodeStatus(true);
          const modal_cl_btn = document.getElementById("nav_modal_close_btn");
          modal_cl_btn.click();
          vm.global_path = new ROSLIB.Topic({
            ros: vm.ros,
            name:
              vm.localPlannerName == "teb"
                ? vm.teb_global_path_topic
                : vm.dwa_global_path_topic,
            messageType: "nav_msgs/Path",
            throttle_rate: 100,
          });
          vm.global_path.subscribe((path) => {
            vm.global_path_shape.setPath(path);
          });
          // vm.local_path = new ROSLIB.Topic({
          //   ros: vm.ros,
          //   name:
          //     vm.localPlannerName == "teb"
          //       ? vm.teb_local_path_topic
          //       : vm.dwa_local_path_topic,
          //   messageType: "nav_msgs/Path",
          //   throttle_rate: 100,
          // });
          // vm.local_path.subscribe((path) => {
          //   vm.local_path_shape.setPath(path);
          // });
        } else {
          msg = "failed start navigation!!";
        }
        vm.showToast({
          time: Date.now().toString(),
          message: msg,
        });
      });
    },
    stopNavigation(file, args) {
      var request = new ROSLIB.ServiceRequest({
        file: file,
        args: args,
      });
      let vm = this;
      this.stopServiceClient.callService(request, function (result) {
        vm.nav_btn_busy = false;
        let msg = "";
        if (result.success) {
          msg = "Stoppped navigation!";
          vm.updateNavNodeStatus(false);
          const modal_cl_btn = document.getElementById("nav_modal_close_btn");
          modal_cl_btn.click();
          vm.global_path.unsubscribe();
          // vm.local_path.unsubscribe();
        } else {
          msg = "failed stop navigation!!";
        }
        vm.showToast({
          time: Date.now().toString(),
          message: msg,
        });
      });
    },
    navStartStop() {
      this.nav_btn_busy = true;
      if (this.running_nav_node)
        this.stopNavigation(
          this.navRobotType == "simulation" ? "nav" : "real_nav",
          `gui:=false map_file:=${this.navMapName} localPlanner:=${this.localPlannerName}`
        );
      else
        this.startNavigation(
          this.navRobotType == "simulation" ? "nav" : "real_nav",
          `gui:=false map_file:=${this.navMapName} localPlanner:=${this.localPlannerName}`
        );
    },
    sendGoal(pos) {
      let vm = this;
      var moveBaseGoal = new ROSLIB.Goal({
        actionClient: this.moveBaseActionClient,
        goalMessage: {
          target_pose: {
            header: {
              frame_id: "map",
            },
            pose: pos,
          },
        },
      });
      this.global_path_shape.visible = true;
      this.local_path_shape.visible = true;
      // moveBaseGoal.on("result", function () {
      //   console.log("ok");
      //   vm.goalContainer.removeChild(vm.goalMarker);
      // });
      moveBaseGoal.send();
    },
  },
  beforeRouteLeave(to, from, next) {
    if (this.running_map_node || this.running_nav_node) {
      alert(this.running_map_node ? "Stop Mapping" : "Stop Navigation");
      next(false);
    } else {
      next();
    }
  },
  mounted() {
    let vm = this;
    vm.vel_sub = new ROSLIB.Topic({
      ros: vm.ros,
      name: "odom",
      messageType: "nav_msgs/Odometry",
    });
    vm.vel_sub.subscribe(function (msg) {
      let vel = parseFloat(msg.twist.twist.linear.x).toFixed(2);
      if (vel == -0.0) vel = 0.0;
      vm.speed = vel;
    });

    // register service clients
    this.startServiceClient = new ROSLIB.Service({
      ros: this.ros,
      name: this.api_start_service_name,
      serviceType: this.api_srv_type,
    });
    this.stopServiceClient = new ROSLIB.Service({
      ros: this.ros,
      name: this.api_stop_service_name,
      serviceType: this.api_srv_type,
    });
    function getYawFromQuat(q) {
      var quat = new THREE.Quaternion(q.x, q.y, q.z, q.w);
      var yaw = new THREE.Euler().setFromQuaternion(quat);
      return yaw["_z"] * (180 / Math.PI);
    }
    // Create the main viewer.
    var viewer = new ROS2D.Viewer({
      divID: "map_container",
      width: document.getElementById("map_container").offsetWidth,
      height: document.getElementById("map_container").offsetHeight,
      background: "#e9ecef",
    });
    // Add zoom to the viewer.
    var zoomView = new ROS2D.ZoomView({
      rootObject: viewer.scene,
    });
    // Add panning to the viewer.
    var panView = new ROS2D.PanView({
      rootObject: viewer.scene,
    });

    // Setup the map client.
    var gridClient = new ROS2D.OccupancyGridClient({
      ros: this.ros,
      rootObject: viewer.scene,
      continuous: true,
    });
    // setup the actionlib client
    this.moveBaseActionClient = new ROSLIB.ActionClient({
      ros: this.ros,
      actionName: "move_base_msgs/MoveBaseAction",
      serverName: "/move_base",
    });

    // Add navigation goal
    this.navGoal = new ROS2D.NavGoal({
      ros: this.ros,
      rootObject: gridClient.rootObject,
    });
    // Add planned path
    this.global_path_shape = new ROS2D.PathShape({
      strokeSize: 0.3,
      strokeColor: createjs.Graphics.getRGB(0, 0, 255, 1),
    });
    // Add planned path
    this.local_path_shape = new ROS2D.PathShape({
      strokeSize: 0.3,
      strokeColor: createjs.Graphics.getRGB(0, 255, 0, 1),
    });

    gridClient.rootObject.addChild(this.local_path_shape);
    gridClient.rootObject.addChild(this.global_path_shape);
    this.global_path_shape.scaleX = 1.0 / gridClient.rootObject.scaleX;
    this.global_path_shape.scaleY = 1.0 / gridClient.rootObject.scaleY;
    this.local_path_shape.scaleX = 1.0 / gridClient.rootObject.scaleX;
    this.local_path_shape.scaleY = 1.0 / gridClient.rootObject.scaleY;

    // Initial pose publisher
    this.initialPosePub = new ROSLIB.Topic({
      ros: this.ros,
      name: "/initialpose",
      messageType: "geometry_msgs/PoseWithCovarianceStamped",
    });
    // Scale the canvas to fit to the map
    gridClient.on("change", function () {
      viewer.scaleToDimensions(
        gridClient.currentGrid.width,
        gridClient.currentGrid.height
      );
      viewer.shift(
        gridClient.currentGrid.pose.position.x,
        gridClient.currentGrid.pose.position.y
      );
      vm.navGoal.initScale();
      vm.global_path_shape.scaleX = 1.0 / gridClient.rootObject.scaleX;
      vm.global_path_shape.scaleY = 1.0 / gridClient.rootObject.scaleY;
      vm.local_path_shape.scaleX = 1.0 / gridClient.rootObject.scaleX;
      vm.local_path_shape.scaleY = 1.0 / gridClient.rootObject.scaleY;
    });
    this.goalMarker = new ROS2D.NavigationImage({
      size: 0.3,
      pulse: true,
      image: require("../assets/navTriangle.png"),
    });

    this.goalContainer = new createjs.Container();
    gridClient.rootObject.addChild(this.goalContainer);

    function registerMouseHandlers() {
      // Setup mouse event handlers
      var mouseDown = false;
      var zoomKey = false;
      var panKey = false;
      var startPos = new ROSLIB.Vector3();

      createjs.Touch.enable(viewer.scene);
      viewer.scene.addEventListener("stagemousedown", function (event) {
        if (event.nativeEvent.ctrlKey === true || vm.zoom_btn) {
          zoomKey = true;
          zoomView.startZoom(event.stageX, event.stageY);
        } else if (event.nativeEvent.shiftKey === true || vm.pan_btn) {
          panKey = true;
          panView.startPan(event.stageX, event.stageY);
        } else {
          var pos = viewer.scene.globalToRos(event.stageX, event.stageY);
          vm.navGoal.startGoalSelection(pos);
        }
        startPos.x = event.stageX;
        startPos.y = event.stageY;
        mouseDown = true;
      });

      viewer.scene.addEventListener("stagemousemove", function (event) {
        if (mouseDown === true) {
          if (zoomKey === true) {
            var dy = event.stageY - startPos.y;
            var zoom =
              1 + (10 * Math.abs(dy)) / viewer.scene.canvas.clientHeight;
            if (dy < 0) zoom = 1 / zoom;
            zoomView.zoom(zoom);
          } else if (panKey === true) {
            panView.pan(event.stageX, event.stageY);
          } else {
            var pos = viewer.scene.globalToRos(event.stageX, event.stageY);
            vm.navGoal.orientGoalSelection(pos);
          }
        }
      });

      viewer.scene.addEventListener("stagemouseup", function (event) {
        if (mouseDown === true) {
          if (zoomKey === true) {
            zoomKey = false;
          } else if (panKey === true) {
            panKey = false;
          } else {
            var pos = viewer.scene.globalToRos(event.stageX, event.stageY);
            var goalPose = vm.navGoal.endGoalSelection(pos);
            if (
              vm.poseEstimateBtn &&
              vm.running_nav_node &&
              !vm.goal_checkbox_btn
            ) {
              var poseMsg = new ROSLIB.Message({
                header: {
                  frame_id: "map",
                },
                pose: {
                  pose: goalPose,
                  covariance: [
                    0.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                    0.06853892326654787,
                  ],
                },
              });
              vm.initialPosePub.publish(poseMsg);
            } else if (
              !vm.poseEstimateBtn &&
              vm.running_nav_node &&
              vm.goal_checkbox_btn
            ) {
              //  Robot pose marker
              vm.goalContainer.addChild(vm.goalMarker);
              vm.goalMarker.x = goalPose.position.x;
              vm.goalMarker.y = -goalPose.position.y;
              vm.goalMarker.rotation = -getYawFromQuat(
                goalPose.orientation
              ).toFixed(2);
              // vm.goalMarker.scaleX = 1.0/gridClient.rootObject.scaleX;
              // vm.goalMarker.scaleY =1.0/gridClient.rootObject.scaleY;
              vm.sendGoal(goalPose);

              vm.showToast({
                time: Date.now().toString(),
                message: "Sending Goal!",
              });
            }
          }
          mouseDown = false;
        }
      });
    }

    // Laser scanner
    function displayLaserScan() {
      vm.baseLink_tf_client = new ROSLIB.TFClient({
        ros: vm.ros,
        fixedFrame: "map",
        angularThres: 0.01,
        transThres: 0.01,
      });
      vm.baseLink_tf_client.subscribe("/base_link", function (tf) {
        vm.base_footprint_tf = tf;
      });

      let marker_radius = 0.06;
      let marker_fill_color = createjs.Graphics.getRGB(255, 0, 0, 1.0);
      let prev_markers = null;

      vm.laser_listener = new ROSLIB.Topic({
        ros: vm.ros,
        name: "/scan",
        messageType: "sensor_msgs/LaserScan",
      });
      vm.laser_listener.subscribe(function (msg) {
        const num = msg.ranges.length;
        const angles = Array.from(
          { length: num },
          (_, i) => msg.angle_min + ((msg.angle_max - msg.angle_min) / num) * i
        );

        const poses_2d = angles.flatMap((angle, index) => {
          const range = msg.ranges[index];
          if (range > msg.range_min && range < msg.range_max) {
            return [[Math.cos(angle) * range, Math.sin(angle) * range, -angle]];
          }
          return []; // Skip this point
        });
        if (vm.base_footprint_tf === null) {
          return;
        }
        // TODO: We might be able to apply the tf transform to the container itself, and dont have to do it on each pose.
        // Init the graphics component
        const scan_markers = new createjs.Container();
        const graphics = new createjs.Graphics()
          .beginFill(marker_fill_color)
          .drawCircle(0, 0, marker_radius)
          .endFill();

        // Transform each point and add it to the graphics
        poses_2d.forEach((pt) => {
          // pt[2] += Math.PI / 2
          const pose = new ROSLIB.Pose({
            position: new ROSLIB.Vector3({
              x: pt[0],
              y: pt[1],
              z: 0,
            }),
            orientation: new ROSLIB.Quaternion({
              x: 0,
              y: 0,
              z: Math.cos(pt[2]),
              w: Math.sin(pt[2]),
            }),
          });
          pose.applyTransform(vm.base_footprint_tf);
          const marker = new createjs.Shape(graphics);
          marker.x = pose.position.x;
          marker.y = -pose.position.y;
          marker.rotation = -getYawFromQuat(pose.orientation).toFixed(2);
          scan_markers.addChild(marker);
        });

        // TODO: Just update the old one, dont make new ones everytime
        if (this.prev_markers !== null) {
          viewer.scene.removeChild(prev_markers);
        }
        viewer.addObject(scan_markers);
        prev_markers = scan_markers;
      });
    }

    //  Robot pose marker
    var robotMarker = new ROS2D.NavigationImage({
      size: 0.2,
      pulse: false,
      image: require("../assets/navRobo.png"),
    });
    gridClient.rootObject.addChild(robotMarker);
    this.poseListner = new ROSLIB.Topic({
      ros: vm.ros,
      name: "robot_pose",
      messageType: "geometry_msgs/Pose",
    });
    this.poseListner.subscribe(function (msg) {
      robotMarker.x = msg.position.x;
      robotMarker.y = -msg.position.y;
      robotMarker.rotation = -getYawFromQuat(msg.orientation).toFixed(2);
    });

    displayLaserScan();
    registerMouseHandlers();
  },
  unmounted() {
    this.laser_listener.unsubscribe();
    this.baseLink_tf_client.unsubscribe("/base_link");
    this.poseListner.unsubscribe();
  },
};
</script>

<style scoped>
.home-page {
  padding: 20px;
  padding-top: 0;
  position: relative;
}
#map_container {
  position: fixed;
  min-height: 100vh;
  min-width: 100vw;
  z-index: 0;
  top: 0;
  left: 0;
  background-color: #7e7e7e;
}
#noMapContainer {
  position: fixed;
  min-height: 100vh;
  min-width: 100vw;
  z-index: 0;
  top: 0;
  left: 0;
  background-color: #e7e7e7;
  display: flex;
  align-items: center;
  justify-content: center;
}
#noMapContainer > svg {
  height: 15vw;
  opacity: 0.1;
}
#noMapContainer > svg:hover {
  color: black !important;
}
.map_btns {
  position: fixed;
  bottom: 30px;
  left: 10px;
  height: auto;
}
.navgation_btns {
  position: fixed;
  top: 60px;
  right: 10px;
  height: auto;
}
.navgation_btns > button {
  margin-bottom: 5px;
}
.map_btns > div > button {
  margin-bottom: 5px;
}
@media screen and (max-width: 1024px) {
  .sec-title {
    font-size: 21px !important;
  }
}
</style>
