<template>
  <span v-if="$props.isLoading" class="loader"></span>
</template>

<script>
export default {
  name: "LoadingView",
  props: {
    isLoading: {type: Boolean, default: false}
  },
}
</script>

<style scoped>
.loader {
  width: 15px;
  height: 15px;
  display: inline-block;
  position: relative;
}
.loader::after,
.loader::before {
  content: '';
  width: 24px;
  height: 24px;
  border: 2px solid black;
  position: absolute;
  left: 0;
  top: 0;
  box-sizing: border-box;
  animation: rotation 2s ease-in-out infinite;
}
.loader::after {
  border-color: #FF3D00;
  animation-delay: 1s;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>