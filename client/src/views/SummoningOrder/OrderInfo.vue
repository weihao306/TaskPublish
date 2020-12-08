<template>
  <v-container grid-list-xs fluid>
    <v-row justify="center">
      <v-col>
        <v-btn color="white" x-small fab fixed :to="{ name: backWardRouteName }"
          ><v-icon>mdi-arrow-left</v-icon></v-btn
        >
      </v-col>
    </v-row>
    <v-card
      class="mx-auto my-auto elevation-8"
      outlined
      v-show="orderInfo !== undefined"
    >
      <v-card-title class="text-h4">
        <v-row justify="center">
          <nav class="my-auto">
            {{ orderInfo.name }}
          </nav>
          <v-chip
            class="mx-2 align-self-center"
            ref="orderStatus"
            dark
            :color="statusColor[orderInfo.status]"
            >{{ orderStatus[orderInfo.status] }}</v-chip
          >
          <v-chip flat class="align-self-center"
            >人数 {{ orderInfo.currentSummoningCount }}/{{
              orderInfo.maximumSummoningCount
            }}</v-chip
          >
        </v-row>
      </v-card-title>
      <v-card-text>
        <v-row justify="center">
          <nav>召集令概述:</nav>
          <blockquote class="col-11 text-body-1">
            {{ orderInfo.info }}
          </blockquote>
        </v-row>
      </v-card-text>
      <!-- <v-card-text>
        <v-carousel v-model="selectedPhoto">
          <v-carousel-item
            v-for="(photoUrl, i) of photoUrls"
            :key="photoUrl.key"
          >
            <v-sheet
              :color="summoningTypeColors[i % summoningTypeColors.length]"
              height="100%"
              tile
            >
              <v-row class="fill-height" align="center" justify="center">
                <div class="display-3">Slide {{ i + 1 }}</div>
              </v-row>
            </v-sheet>
          </v-carousel-item>
        </v-carousel>
      </v-card-text> -->
    </v-card>
    <v-layout row wrap justify-center>
      <v-flex xs11>
        <v-window v-model="onboarding">
          <v-window-item v-for="(img, n1) of imgs" :key="`card-${n1}`">
            <v-card class="mx-auto my-auto elevation-8">
              <v-img contain :src="img" height="30vh"> </v-img>
            </v-card>
          </v-window-item>
        </v-window>
        <v-item-group
          v-model="onboarding"
          mandatory
          class="text-center justify-center"
        >
          <v-item v-for="(img, n2) of imgs" :key="`btn-${n2}`">
            <v-btn
              slot-scope="{ active, toggle }"
              :input-value="active"
              @click="toggle"
              icon
            >
              <v-icon>mdi-record</v-icon>
            </v-btn>
          </v-item>
        </v-item-group>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import OrderInfo from "@/classes/OrderInfo.js";
export default {
  mounted() {
    this.getOrderInfo(this.$props.order_id);
  },
  props: {
    order_id: Number,
    // backWardRouteName: String,
  },
  computed: {
    backWardRouteName: (vm) => {
      // 路由组件传入属性来决定返回键对应页面
      if (vm.$attrs.backWardRouteName !== undefined) {
        sessionStorage.setItem(
          "backWardRouteName",
          vm.$attrs.backWardRouteName
        );
        return vm.$attrs.backWardRouteName;
      } else {
        return sessionStorage.getItem("backWardRouteName");
      }
    },
  },
  data() {
    return {
      onboarding:0,
      orderInfo: new OrderInfo(),
      selectedPhoto: 0,
      orderStatus: ["等待同意", "响应", "拒绝"],
      statusColor: ["warning", "success", "error"],
      summoningTypeColors: ["red", "success", "warning", "primary"],
      photoUrls: [],
      imgs:[]
    };
  },
  methods: {
    getOrderInfo(order_id) {
      this.axios
        .get("api/tasks", {
          params: { task_id: order_id },
        })
        .then((res) => {
          const orderInfoObj = res.data;
          console.log(orderInfoObj);
          this.orderInfo = new OrderInfo(orderInfoObj);
          console.log(this.orderInfo);
          // setphotoUrls();
        });
    },
    setphotoUrls() {
      for (let photo of this.orderInfo.photos) {
        this.photoUrls.push(urlCreator.createObjectURL(photo));
      }
    },
  },
};
</script>

<style>
</style>