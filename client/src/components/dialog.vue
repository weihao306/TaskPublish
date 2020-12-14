<template>
  <v-container grid-list-xs fluid>
    <v-dialog
      v-model="dialog"
      scrollable
      :overlay="false"
      transition="dialog-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn v-bind="attrs" v-on="on" color="success">{{ buttonText }}</v-btn>
      </template>
      <card>
        <template v-slot:title>
          <slot name="title"></slot>
        </template>
        <template v-slot:text>
          <slot name="text"></slot>
        </template>
        <template v-slot:action>
          <slot name="action"></slot>
        </template>
      </card>
    </v-dialog>
  </v-container>
</template>

<script>
import Card from "@/components/dialog.vue";
export default {
  props: ["buttonText", "switcher"],
  components: {
    Card,
  },
};
</script>

<style>
</style>