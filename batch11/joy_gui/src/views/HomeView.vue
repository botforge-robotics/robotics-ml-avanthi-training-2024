/* eslint-disable */
<template>
  <div class="home">
    <div class="info_container">
      <div class="badge battery-badge">
        <div>
          <p>Battery</p>
          <h1>{{ this.voltage_percent_smooth.toFixed(2) }} %</h1>
        </div>
      </div>
      <div class="badge temperature-badge">
        <div>
          <p>Temperature</p>
          <h1>{{ temperature }} °c</h1>
        </div>
      </div>
      <div class="badge humidity-badge">
        <div>
          <p>Humidity</p>
          <h1>{{ humidity }} %</h1>
        </div>
      </div>
    </div>
    <div class="middle-section">
      <img :src="stream_link" />
      <div class="task-section">
        <h1 class="tasks-heading">Tasks</h1>
        <div class="tasks-conatiner">
          <div class="d-flex flex-row justify-content-between mb-2">
            <div class="d-flex flex-row w-100">
              <p class="m-0 col-4 fw-bold text-white">Reminder</p>
              <p class="m-0 col-4 fw-bold text-white">Person</p>
              <p class="m-0 col-4 fw-bold text-white">Time</p>
            </div>
          </div>
          <div v-if="tasks.length > 0">
            <div
              v-for="(task, index) in tasks"
              :key="index"
              class="d-flex flex-row justify-content-between mb-2"
            >
              <div class="d-flex flex-row w-100">
                <p class="m-0 col-4 text-nowrap text-truncate text-white">
                  {{ task.reminder }}
                </p>
                <p class="m-0 col-4 text-white">{{ task.person }}</p>
                <p class="m-0 col-4 text-white">
                  {{ task.hour + ":" + task.minute + " hrs." }}
                </p>
              </div>
            </div>
          </div>
          <P v-else class="text-white pt-4">No Tasks. Add one!</P>
        </div>
        <div class="buttons-container">
          <div class="face-btn">
            <div
              class="icon-btn add-face-btn d-flex align-items-center justify-content-center me-3"
            >
              <font-awesome-icon
                type="button"
                data-bs-toggle="modal"
                data-bs-target="#addface"
                @click="v$.person_name.$touch()"
                :icon="['fas', 'user-plus']"
                size="lg"
                style="color: white"
              />
            </div>
            <div
              class="icon-btn remove-face-btn d-flex align-items-center justify-content-center me-3"
            >
              <font-awesome-icon
                type="button"
                data-bs-toggle="modal"
                data-bs-target="#deleteface"
                @click="getPersonsinDataBase"
                :icon="['fas', 'user-minus']"
                size="lg"
                style="color: white"
              />
            </div>

            <div
              class="icon-btn add-task-btn d-flex align-items-center justify-content-center me-3"
            >
              <font-awesome-icon
                data-bs-toggle="modal"
                data-bs-target="#addtask"
                type="button"
                :icon="['fas', 'calendar-plus']"
                size="lg"
                style="color: white"
                @click="
                  v$.task_name.$touch();
                  getPersonsinDataBase();
                "
              />
            </div>
            <div
              c
              class="icon-btn remove-task-btn d-flex align-items-center justify-content-center"
            >
              <font-awesome-icon
                data-bs-toggle="modal"
                data-bs-target="#deletetask"
                type="button"
                :icon="['fas', 'calendar-minus']"
                size="lg"
                style="color: white"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      v-if="user_chat_text != ''"
      class="chat-section d-flex align-items-center justify-content-center"
    >
      <h1>user:</h1>
      <p>{{ user_chat_text }}</p>
    </div>
    <div
      v-if="robo_chat_text != ''"
      class="chat-section d-flex align-items-start justify-content-center"
    >
      <h1>Snowboy:</h1>
      <p>{{ robo_chat_text }}</p>
    </div>
    <!-- add face -->
    <div
      class="modal fade"
      id="addface"
      tabindex="-1"
      aria-labelledby="addfaceLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="addfaceLabel">Register face?</h1>
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
                <label for="personName" class="col-form-label me-2"
                  >Person Name:</label
                >
              </div>
              <div class="col-auto">
                <input
                  id="person_name"
                  class="form-control"
                  v-model="person_name"
                  @input="v$.person_name.$touch()"
                />
              </div>
              <div class="col-auto">
                <span id="personNameHelpInline" class="form-text">
                  Must be only alphabets, Min Length 4, Max Length 10.
                </span>
              </div>
            </div>

            <p v-if="v$.person_name.$error" class="text-danger fs-6">
              Invalid name!
            </p>
          </div>
          <div class="modal-footer">
            <button
              id="register_person_modal_close_btn"
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn btn-success"
              :disabled="v$.person_name.$error"
              @click="registerPerson"
            >
              Register
            </button>
            <SimpleKeyboard
              @onChange="
                (input) => {
                  this.person_name = input;
                  v$.person_name.$touch();
                }
              "
              :keyboardClass="'faceaddkeyboard'"
              :input="person_name"
            />
          </div>
        </div>
      </div>
    </div>
    <!-- delete face modal -->
    <div
      class="modal fade"
      id="deleteface"
      tabindex="-1"
      aria-labelledby="deleteface"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="deletefaceLabel">Delete face?</h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div
              class="d-flex flex-row align-items-center"
              v-if="deleting_face"
            >
              <span
                class="spinner-grow spinner-grow-sm"
                role="status"
                aria-hidden="true"
              ></span>
              <p class="m-0 p-0 ms-2">Deleting..</p>
            </div>

            <div v-if="!deleting_face">
              <div
                v-for="(person, index) in facesInDatabase"
                :key="index"
                class="d-flex flex-row justify-content-between mb-2"
              >
                <p>{{ person }}</p>
                <button
                  type="button"
                  class="btn btn-sm btn-danger"
                  @click="deleteFace(person)"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button
              id="delete_person_modal_close_btn"
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <!-- add task -->
    <div
      class="modal fade"
      id="addtask"
      tabindex="-1"
      aria-labelledby="addtaskLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="addtaskLabel">Add reminder?</h1>
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
                <label for="taskName" class="col-form-label me-2"
                  >Reminder:</label
                >
              </div>
              <div class="col-auto">
                <input
                  id="task_name"
                  class="form-control"
                  v-model="task_name"
                  @input="v$.task_name.$touch()"
                />
              </div>
            </div>

            <div class="row align-items-center mt-3">
              <div class="col-auto">
                <label for="hour" class="col-form-label me-2">Hour:</label>
              </div>
              <div class="col-auto">
                <select id="hour" class="form-select" v-model="selectedHour">
                  <option
                    v-for="(hour, index) in 24"
                    :value="hour - 1"
                    :key="index"
                  >
                    {{ hour - 1 }}
                  </option>
                </select>
              </div>
            </div>

            <div class="row align-items-center mt-3">
              <div class="col-auto">
                <label for="minute" class="col-form-label me-2">Minute:</label>
              </div>
              <div class="col-auto">
                <select
                  id="minute"
                  class="form-select"
                  v-model="selectedMinute"
                >
                  <option
                    v-for="(minute, index) in 60"
                    :value="minute - 1"
                    :key="index"
                  >
                    {{ minute - 1 }}
                  </option>
                </select>
              </div>
            </div>

            <div class="row align-items-center mt-3">
              <div class="col-auto">
                <label for="faces" class="col-form-label me-2">Face:</label>
              </div>
              <div class="col-auto">
                <select id="faces" class="form-select" v-model="selectedPerson">
                  <option
                    v-for="(face, index) in facesInDatabase"
                    :value="face"
                    :key="index"
                  >
                    {{ face }}
                  </option>
                </select>
              </div>
            </div>

            <p
              v-if="
                v$.task_name.$error ||
                v$.selectedPerson.$error ||
                v$.selectedHour.$error ||
                v$.selectedMinute.$error
              "
              class="text-danger fs-6"
            >
              fill all fields.
            </p>
          </div>
          <div class="modal-footer">
            <button
              id="add_task_modal_close_btn"
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
            <button
              type="button"
              class="btn btn-success"
              :disabled="
                v$.task_name.$error ||
                v$.selectedPerson.$error ||
                v$.selectedHour.$error ||
                v$.selectedMinute.$error
              "
              @click="addTask"
            >
              Add
            </button>
            <SimpleKeyboard
              @onChange="
                (input) => {
                  this.task_name = input;
                  v$.task_name.$touch();
                }
              "
              :keyboardClass="'taskaddkeyboard'"
              :input="task_name"
            />
          </div>
        </div>
      </div>
    </div>
    <!-- delete tasks modal -->
    <div
      class="modal fade"
      id="deletetask"
      tabindex="-1"
      aria-labelledby="deletetask"
      aria-hidden="true"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="deletetaskLabel">
              Delete reminder?
            </h1>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div>
              <div class="d-flex flex-row justify-content-between mb-2">
                <div class="d-flex flex-row w-100">
                  <p class="m-0 col-4 fw-bold">Reminder</p>
                  <p class="m-0 col-4 fw-bold">Person</p>
                  <p class="m-0 col-4 fw-bold">Time</p>
                </div>
                <div class="col-2"></div>
              </div>
              <div v-if="tasks.length > 0">
                <div
                  v-for="(task, index) in tasks"
                  :key="index"
                  class="d-flex flex-row justify-content-between mb-2"
                >
                  <div class="d-flex flex-row w-100">
                    <p class="m-0 col-4 text-nowrap text-truncate">
                      {{ task.reminder }}
                    </p>
                    <p class="m-0 col-4">{{ task.person }}</p>
                    <p class="m-0 col-4">
                      {{ task.hour + ":" + task.minute + " hrs." }}
                    </p>
                  </div>
                  <button
                    type="button"
                    class="btn btn-sm btn-danger col-2"
                    @click="deleteTask(index)"
                  >
                    Delete
                  </button>
                </div>
              </div>
              <p v-else class="text-black pt-4">No Tasks. Add one!</p>
            </div>
          </div>
          <div class="modal-footer">
            <button
              id="delete_task_modal_close_btn"
              type="button"
              class="btn btn-secondary"
              data-bs-dismiss="modal"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ROSLIB from "roslib";
import SimpleKeyboard from "../components/SimpleKeyboard.vue";

import { useVuelidate } from "@vuelidate/core";
import { required, alpha, minLength, maxLength } from "@vuelidate/validators";
export default {
  name: "HomeView",
  components: {
    SimpleKeyboard,
  },
  setup: () => ({ v$: useVuelidate() }),
  data: () => ({
    input: "",
    person_name: "",
    ros: new ROSLIB.Ros(),
    temperature_sub: null,
    temperature: 0.0,
    humidity_sub: null,
    humidity: 0.0,
    min_voltage: 6.8,
    max_voltage: 8.4,
    voltage: 6.8,
    voltage_percent: 0,
    voltage_percent_buffer: [],
    voltage_percent_smooth: 0,
    voltage_sub: null,
    windowSize: 150,
    imageSub: null,
    stream_link: "http://",
    robotIP: "0.0.0.0",
    user_chat_text: "",
    robo_chat_text: "",
    chat_user_sub: "",
    chat_robot_sub: "",
    facesInDatabase: [],
    task_name: null,
    selectedPerson: null,
    selectedHour: null,
    selectedMinute: null,
    deleting_face: false,
    tasks: [],
  }),
  validations() {
    return {
      person_name: {
        required,
        alpha,
        minLengthValue: minLength(4),
        maxLengthValue: maxLength(10),
      },
      task_name: {
        required,
        minLengthValue: minLength(4),
      },
      selectedPerson: {
        required,
        minLengthValue: minLength(1),
      },
      selectedHour: {
        required,
        minLengthValue: minLength(1),
      },
      selectedMinute: {
        required,
        minLengthValue: minLength(1),
      },
    };
  },
  methods: {
    addTask() {
      this.tasks.push({
        reminder: this.task_name,
        person: this.selectedPerson,
        hour: this.selectedHour,
        minute: this.selectedMinute,
      });
      localStorage.setItem("tasks", JSON.stringify(this.tasks));
      const modal_cl_btn = document.getElementById("add_task_modal_close_btn");
      modal_cl_btn.click();
    },
    deleteTask(index) {
      this.tasks.splice(index, 1);
      localStorage.setItem("tasks", JSON.stringify(this.tasks));
    },
    registerPerson() {
      var request = new ROSLIB.ServiceRequest({
        name: this.person_name,
        samples: 20,
      });
      let registerFaceClient = new ROSLIB.Service({
        ros: this.ros,
        name: "register_person",
        serviceType: "TrainPerson",
      });
      let vm = this;
      const modal_cl_btn = document.getElementById(
        "register_person_modal_close_btn"
      );
      modal_cl_btn.click();
      registerFaceClient.callService(request, function (result) {
        if (result.success) {
          vm.getPersonsinDataBase();
        }
      });
    },
    getPersonsinDataBase() {
      var request = new ROSLIB.ServiceRequest({});
      let getFacesClient = new ROSLIB.Service({
        ros: this.ros,
        name: "list_of_person_in_model",
        serviceType: "RecognisePersonsOnce",
      });
      let vm = this;
      getFacesClient.callService(request, function (result) {
        if (result.success) {
          vm.facesInDatabase = result.persons;
          // const modal_cl_btn = document.getElementById("map_modal_close_btn");
          // modal_cl_btn.click();
        }
      });
    },
    deleteFace(face) {
      this.deleting_face = true;
      var request = new ROSLIB.ServiceRequest({ name: face });
      let deleteFaceClient = new ROSLIB.Service({
        ros: this.ros,
        name: "delete_person",
        serviceType: "DeletePerson",
      });
      let vm = this;
      deleteFaceClient.callService(request, function (result) {
        if (result.success) {
          vm.deleting_face = false;
        } else {
          vm.deleting_face = false;
        }
        vm.getPersonsinDataBase();
      });
    },
    executeAtStartOfNextMinute() {
      var now = new Date();
      var secondsUntilNextMinute = 60 - now.getSeconds(); // Calculate seconds until next minute
      var self = this;
      setTimeout(function () {
        var now = new Date();
        let hour = now.getHours();
        let minute = now.getMinutes();
        let task = null;
        let vm = self;
        for (let i = 0; i < vm.tasks.length; i++) {
          if (vm.tasks[i].hour === hour && vm.tasks[i].minute === minute) {
            task = vm.tasks[i];
            break;
          }
        }
        if (task != null) {
          var request = new ROSLIB.ServiceRequest({
            name: task.person,
            reminder: task.reminder,
          });
          let reminderClient = new ROSLIB.Service({
            ros: self.ros,
            name: "reminder",
            serviceType: "Reminder",
          });

          reminderClient.callService(request, function (result) {
            if (result.success) {
              for (let i = 0; i < vm.tasks.length; i++) {
                if (
                  vm.tasks[i].hour === hour &&
                  vm.tasks[i].minute === minute
                ) {
                  vm.deleteTask(i);
                  break;
                }
              }
            } else {
              for (let i = 0; i < vm.tasks.length; i++) {
                if (
                  vm.tasks[i].hour === hour &&
                  vm.tasks[i].minute === minute
                ) {
                  if (vm.tasks[i].minute === 59) {
                    // If minute is 59, increment hour and set minute to 0
                    vm.tasks[i].hour = (vm.tasks[i].hour + 1) % 24; // Increment hour, consider 24-hour format
                    vm.tasks[i].minute = 0;
                  } else {
                    // Otherwise, just increment minute
                    vm.tasks[i].minute++;
                  }
                  break; // Exit loop after updating the time
                }
              }
            }
            localStorage.setItem("tasks", JSON.stringify(vm.tasks));
          });
        }
        self.executeAtStartOfNextMinute(); // Schedule the next callback
      }, secondsUntilNextMinute * 1000); // Convert seconds to milliseconds
    },
  },
  mounted() {
    this.ros.connect("ws://" + this.robotIP + ":9090");
    this.stream_link =
      "http://" +
      this.robotIP +
      ":9000/stream?topic=/camera/image&type=ros_compressed";
    this.temperature_sub = new ROSLIB.Topic({
      ros: this.ros,
      name: "/temperature",
      messageType: "std_msgs/Float32",
      throttle_rate: 100,
    });
    this.temperature_sub.subscribe((data) => {
      this.temperature = data.data.toFixed(2);
    });
    this.volatge_sub = new ROSLIB.Topic({
      ros: this.ros,
      name: "/battery_voltage",
      messageType: "std_msgs/Float32",
      throttle_rate: 100,
    });
    this.volatge_sub.subscribe((data) => {
      this.voltage = data.data.toFixed(2);
      this.voltage_percent =
        ((parseFloat(data.data) - this.min_voltage) /
          (this.max_voltage - this.min_voltage)) *
        100;
      this.voltage_percent_buffer.push(this.voltage_percent);
      if (this.voltage_percent_buffer.length > this.windowSize) {
        this.voltage_percent_buffer.shift();
      }
      let sum = this.voltage_percent_buffer.reduce((acc, val) => acc + val, 0);
      this.voltage_percent_smooth = sum / this.voltage_percent_buffer.length;
    });
    this.humidity_sub = new ROSLIB.Topic({
      ros: this.ros,
      name: "/humidity",
      messageType: "std_msgs/Float32",
      throttle_rate: 100,
    });

    this.humidity_sub.subscribe((data) => {
      this.humidity = data.data.toFixed(2);
    });
    this.chat_user_sub = new ROSLIB.Topic({
      ros: this.ros,
      name: "/recognized_text",
      messageType: "std_msgs/String",
    });

    this.chat_user_sub.subscribe((data) => {
      this.user_chat_text = data.data;
      this.robo_chat_text = "";
    });
    this.chat_robot_sub = new ROSLIB.Topic({
      ros: this.ros,
      name: "/text_to_say",
      messageType: "std_msgs/String",
    });

    this.chat_robot_sub.subscribe((data) => {
      this.robo_chat_text = data.data;
    });
    this.ros.on("connection", function () {
      console.log("Connected to websocket server.");
    });
    this.ros.on("error", function (error) {
      console.log("Error connecting to websocket server: ", error);
    });

    this.ros.on("close", function () {
      console.log("Connection to websocket server closed.");
    });
    let temp_tasks = JSON.parse(localStorage.getItem("tasks"));
    if (temp_tasks == null) {
      this.tasks = [];
    } else {
      this.tasks = temp_tasks;
    }
    this.executeAtStartOfNextMinute();
  },
  unmounted() {
    this.temperature_sub.unsubscribe();
    this.volatge_sub.unsubscribe();
    this.humidity_sub.unsubscribe();
    this.chat_robot_sub.unsubscribe();
    this.chat_user_sub.unsubscribe();
  },
};
</script>

<style scoped>
.info_container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px;
  margin-bottom: 15px;
}
.info_container > .badge {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-evenly;
  padding: 10px;
  border-radius: 10px;
  width: 90px;
  height: 40px;
}
.info_container > .badge > div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.info_container > .badge > div > h1 {
  font-size: 15px;
  margin: 0;
  color: white;
}
.info_container > .badge > div > p {
  font-size: 13px;
  margin: 0 0 0 0;
  color: rgb(236, 236, 236);
}
.battery-badge {
  background-color: #df6e1e;
}
.temperature-badge {
  background-color: #2e6a65;
}
.humidity-badge {
  background-color: #4c276a;
}
img {
  width: 140px;
  height: 187px;
  background-color: white;
  transform: rotate(180deg);
}
.middle-section {
  display: flex;
  justify-content: space-evenly;
}
.modal-body {
  max-height: 50vh;
  overflow-y: scroll;
}
.task-section {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.tasks-conatiner {
  width: 100%;
  min-height: 120px;
  overflow-y: scroll;
  padding-right: 17px; /* Increase/decrease this value for cross-browser compatibility */
  box-sizing: content-box; /* So the width will be 100% + 17px */
}

.chat-section {
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
}
.chat-section > h1 {
  font-size: 15px;
  margin: 0 5px 0 0;
  opacity: 0.6;
}
.chat-section > p {
  font-size: 15px;
  margin: 0;
  text-overflow: ellipsis;
  max-width: 90vw;
  white-space: nowrap;
  overflow: hidden;
}
.tasks-heading {
  font-size: 17px;
  color: white;
  opacity: 0.7;
  margin-bottom: 5px;
}
.face-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-bottom: 5px;
}

.add-btn {
  border: none;
  background-color: #2e6a2e;
  color: white;
  margin-right: 5px;
  width: 70px;
}
.icon-btn {
  width: 40px;
  height: 40px;
  border-radius: 30px;
}
.add-face-btn {
  background-color: #2e6a2e;
}
.remove-face-btn {
  background-color: red;
}
.add-task-btn {
  background-color: #2e6a2e;
}
.remove-task-btn {
  background-color: red;
}
.remove-btn {
  border: none;
  background-color: red;
  color: white;
  width: 95px;
}
</style>
