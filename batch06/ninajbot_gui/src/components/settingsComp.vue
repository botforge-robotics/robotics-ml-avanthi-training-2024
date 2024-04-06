<template>
  <div
    class="modal fade"
    id="settingsModal"
    tabindex="-1"
    aria-labelledby="settingsLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog" id="settingsModalContent">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5 fw-bold" id="settingsLabel">Settings</h1>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="card mb-4">
            <div class="card-header fs-4">Velocity</div>
            <div class="card-body">
              <h5 class="card-title">Set max velocities</h5>
              <div class="d-flex flex-row justify-content-evenly">
                <div class="w-50 ms-5 me-5">
                  <label
                    for="max_linear_vel"
                    class="form-label fs-6 fw-semibold fst-italic d-flex align-items-center"
                    >Max Linear Velocity:
                    <p class="ms-2 fs-5 fw-bold mb-0">
                      {{ max_linear_vel }}<span class="text-muted"> m/s.</span>
                    </p></label
                  >
                  <input
                    type="range"
                    class="form-range"
                    :min="min_allowed_linear_vel"
                    :max="max_allowed_linear_vel"
                    step="0.05"
                    id="max_linear_vel"
                    :value="max_linear_vel"
                    @change="set_max_linear_vel($event.target.value)"
                  />
                </div>

                <div class="w-50 ms-5 me-5">
                  <label
                    for="max_angular_vel"
                    class="form-label fs-6 fw-semibold fst-italic d-flex align-items-center"
                    >Max Angular Velocity:
                    <p class="ms-2 fs-5 fw-bold mb-0">
                      {{ max_angular_vel }}
                      <span class="text-muted"> rad/s.</span>
                    </p></label
                  >
                  <input
                    type="range"
                    class="form-range"
                    :min="min_allowed_angular_vel"
                    :max="max_allowed_angular_vel"
                    step="0.05"
                    id="max_angular_vel"
                    :value="max_angular_vel"
                    @change="set_max_angular_vel($event.target.value)"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button
            id="settings_modal_close_btn"
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
</template>

<script>
import { mapGetters, mapMutations } from "vuex";
export default {
  data() {
    return {};
  },
  components: {},
  computed: {
    ...mapGetters([
      "ros",
      "max_linear_vel",
      "max_angular_vel",
      "max_allowed_linear_vel",
      "max_allowed_angular_vel",
      "min_allowed_linear_vel",
      "min_allowed_angular_vel",
    ]),
  },
  methods: {
    ...mapMutations([
      "publishLcd",
      "set_max_linear_vel",
      "set_max_angular_vel",
    ]),
  },
  mounted() {},
};
</script>

<style>
.auxilary-page {
  padding: 20px;
  padding-top: 0;
}
#settingsModalContent {
  min-width: 65vw !important;
}
#settingsModalContent > .modal-content > .modal-body {
  max-height: 80vh;
  overflow-y: scroll;
}
.pub-btn {
  width: 100px;
  background-color: #f2771a !important;
  color: white !important;
}
.pub-btn:hover {
  background-color: #bd5404 !important;
  color: rgb(216, 216, 216) !important;
}
.form-range:focus::-webkit-slider-thumb {
  background-color: #f2771a;
  box-shadow: 0px 0px 3px 3px rgba(242, 119, 26, 0.72) !important;
}
.form-range::-webkit-slider-thumb {
  background-color: #f2771a !important;
}
label p {
  color: #f2771a;
}
select:active {
  border: #bd5404;
  box-shadow: inset 0 1px 1px rgb(242, 119, 26), 0 0 8px rgb(242, 119, 26) !important;
}
select:focus {
  border: #bd5404;
  box-shadow: inset 0 1px 1px rgb(242, 119, 26), 0 0 8px rgb(242, 119, 26) !important;
}
/* #rgbCard {
  min-height: 897px;
} */
@media screen and (max-width: 1024px) {
  .card-title {
    font-size: 14px;
    font-weight: 600;
  }
  .card-header {
    font-size: 15px;
    font-weight: 600;
  }
  label.btn {
    font-size: 12px;
    align-self: center;
  }
  .form-label {
    font-size: 12.5px !important;
  }
  .form-label p {
    font-size: 15px !important;
  }
}
</style>
