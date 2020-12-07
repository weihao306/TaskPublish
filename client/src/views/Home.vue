<template>
  <v-main class="home">
    <Header
      :Pages="List"
      :SlideBarToggle="SlideBarToggleState"
      @switchToggle="SlideBarToggleState = $event"
    ></Header>
    <router-view :uid="this.$store.state.userInfo.uid"></router-view>
    <SlideBar
      :SlideBarToggle="SlideBarToggleState"
      @switchToggle="SlideBarToggleState = $event"
      :LogOutPathName="LoginPathName"
      :List="List"
      :User="this.$store.state.userInfo"
    ></SlideBar>
  </v-main>
</template>

<script>
// @ is an alias to /src
import Header from "@/components/Header.vue";
import SlideBar from "@/components/SlideBar.vue";
export default {
  name: "Home",
  components: {
    Header,
    SlideBar,
  },
  data() {
    return {
      SlideBarToggleState: false,

      LoginPathName: "Login",

      List: [
        {
          title: "用户信息",
          icon: "mdi-desktop-mac-dashboard",
          link: "UserInfo",
        },
        {
          title: "召集令",
          icon: "mdi-door",
          link: "SummoningOrderMain",
        },
        // {
        //   title: "Aircondition",
        //   icon: "mdi-air-conditioner",
        //   link: "/Aircondition/"
        // }
      ],
    };
  },
};
</script>
