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
      <v-card-title class="text-h4"
        >{{ orderInfo.name }}
        <v-chip
          class="mx-2"
          ref="orderStatus"
          dark
          :color="statusColor[orderInfo.status]"
          >{{ orderStatus[orderInfo.status] }}</v-chip
        >
        <v-chip flat
          >人数 {{ orderInfo.currentSummoningCount }}/{{
            orderInfo.maximumSummoningCount
          }}</v-chip
        >
      </v-card-title>
      <v-card-text>
        <v-row>
          <blockquote class="col-12 text-body-1">
            召集令概述:
            {{ orderInfo.info }}
          </blockquote>
        </v-row>
      </v-card-text>
      <v-card-text>
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
                <!-- <v-img>

                </v-img> -->
                <div class="display-3">Slide {{ i + 1 }}</div>
              </v-row>
            </v-sheet>
          </v-carousel-item>
        </v-carousel>
      </v-card-text>
    </v-card>
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
    backWardRouteName: vm => {
      if (vm.$attrs.backWardRouteName !== undefined){
        sessionStorage.setItem("backWardRouteName",vm.$attrs.backWardRouteName);
        return vm.$attrs.backWardRouteName;
      }else{
        return sessionStorage.getItem("backWardRouteName");
      }
    },
  },
  data() {
    return {
      orderInfo: new OrderInfo(),
      selectedPhoto: 0,
      orderStatus: ["等待同意", "响应", "拒绝"],
      statusColor: ["warning", "success", "error"],
      summoningTypeColors: ["red", "success", "warning", "primary"],
      photoUrls: [],
    };
  },
  methods: {
    getOrderInfo(order_id) {
      this.axios
        .get("api/tasks", {
          params: { order_id: order_id },
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