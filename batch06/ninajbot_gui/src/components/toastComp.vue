<template>
  <div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div
      class="toast"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
      v-for="(toast, index) in toasts"
      :key="index"
      :id="'toast' + index"
    >
      <div class="toast-header">
        <img src="../assets/logo.png" class="me-2" alt="..." />
        <strong class="me-auto">Tortoisebot</strong>
        <small>{{ toast.time }}</small>
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="toast"
          :data-bs-target="'#toast' + index"
          aria-label="Close"
          @click="deleteToast(index)"
        ></button>
      </div>
      <div class="toast-body">
        {{ toast.message }}
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
  computed: {
    ...mapGetters(["toasts"]),
  },
  methods: {
    ...mapMutations(["deleteToast"]),
  },
};
</script>

<style>
.toast-header img {
  width: 17px;
}
.toast-container {
  z-index: 5;
}
</style>
