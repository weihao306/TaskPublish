<template>
  <el-menu mode="horizontal" default-active="activeIndex" @select="handleSelect">
    <el-menu-item index="1" key=""></el-menu-item>

    <el-submenu
      v-for="(submenus, index) in menus"
      :index="index + 1"
      :key="submenus.key"
    >
      <template slot="title">{{ submenus.title }}</template>
      <el-menu-item
        v-for="(item, subIndex) in submenus.menus"
        :index="index + 1 + '-' + (subIndex + 1)"
        :key="item.key"
      >
        {{ item.title }}
      </el-menu-item>
    </el-submenu>
  </el-menu>
</template>

<script>
export default {
  data() {
    return {
        menus:[],

    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    },
  },
};
</script>

<style>
</style>