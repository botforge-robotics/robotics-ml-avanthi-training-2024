<template>
  <div class="omni_bar conatiner-fluid">
    <div class="main_text">
      <h1 class="text-center speed_text align-middle">
        {{ speed }}<span>m/s</span>
      </h1>
      <p class="text-center align-middle">{{ omni_title }}</p>
    </div>
  </div>
</template>

<script>
export default {
  components: {},
  props: ["speed", "omni_title"],
};
</script>

<style>
.main_text {
  width: 100%;
}
.main_text > p {
  color: green;
  font-size: 23px;
  font-weight: bold;
  margin-bottom: 0;
}
.speed_text {
  margin: 0;
  font-size: 28px;
  font-weight: bold;
  color: #f2771a;
  margin: auto;
}
.speed_text > span {
  font-weight: 400;
  font-size: 20px;
  opacity: 80%;
}
.omni_bar {
  display: flex;
  flex-direction: row;
  align-items: center;
  left: calc(50% - 26vw / 2);
  position: fixed;
  bottom: 30px;
  width: 26vw;
  min-height: 90px;
  border-radius: 80px;
  background-color: #1c1919;
}
</style>
