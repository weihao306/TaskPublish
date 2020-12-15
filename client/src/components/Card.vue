<template>
  <v-card-title class="mx-auto my-3 elevation-8" outlined>
    <v-card-title>
      <slot name="title"></slot>
    </v-card-title>
    <v-card-text>
      <slot name="text"></slot>
    </v-card-text>
    <v-card-actions>
      <slot name="action"></slot>
    </v-card-actions>
  </v-card-title>
</template>

<script>
export default {
  props: ["cardHeight", "cardWidth", "justifyProperty"],
  data() {
    return {
      // cardHeight:"10rem",
      // cardWidth:"35rem",
      // justifyProperty:"center"
    };
  },
};
</script>

<style>
</style>