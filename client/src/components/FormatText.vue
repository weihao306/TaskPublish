<template>
  <nav
    v-bind:class="{
      TextCenter: center,
      'text-h3': large,
      'text-h5': mid,
      'text-body-1': small,
    }"
    class="text-justify font-weight-bold"
  >
    <slot></slot>
  </nav>
</template>

<script>
export default {
  computed: {
    center: (vm) =>
       vm.$attrs.center === undefined || vm.$attrs.center === "false"
        ? false
        : true,
    large: (vm) => (vm.$attrs.size === "large" ? true : false),
    mid: (vm) => (vm.$attrs.size === "mid" ? true : false),
    small: (vm) => (vm.$attrs.size === "small" ? true : false),
  },
//   data() {
//     return {
//     };
//   },
  methods: {
    isLarge() {
      return this.$$attrs.size === "large" ? true : false;
    },
    isMiddle() {
      return this.$$attrs.size === "mid" ? true : false;
    },
    isSmall() {
      return this.$$attrs.size === "small" ? true : false;
    },
  },
};
</script>

<style lang="css">
.TextCenter {
  text-align: center;
  text-align-last: center;
}
</style>