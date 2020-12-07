<template>
  <v-container grid-list-xs fluid>
    <v-row justify="center">
      <v-col>
        <v-btn fixed color="white" x-small fab :to="{ name: 'Masses' }"
          ><v-icon>mdi-arrow-left</v-icon></v-btn
        >
      </v-col>
    </v-row>
    <v-layout row wrap justify-center>
      <v-flex xs11>
        <v-select
          chips
          light
          solo
          multiple
          :items="selectOptions"
          :menu-props="{ maxHeight: '10rem' }"
          v-model="selectedType"
          label="召集令类型"
        >
          <v-slot max-height="3rem"></v-slot>
        </v-select>
      </v-flex>
      <v-flex xs11>
        <v-card
          v-for="order of orderList.filter((obj) =>
            selectedType.length > 0 ? selectedType.includes(obj.type) : true
          )"
          :key="order.key"
          class="my-3"
        >
          <v-card-title>
            <nav class="mr-2">
              {{ order.name }}
            </nav>
            <v-layout column wrap justify-center>
              <v-layout row wrap>
                <v-chip flat color="grey" class="mr-2 align-self-center"
                  >人数:{{ order.currentSummoningCount }}/{{
                    order.maximumSummoningCount
                  }}</v-chip
                >
                <v-chip
                  label
                  :color="color[order.type % color.length]"
                  class="align-self-center"
                >
                  {{ selectOptions[order.type].text }}
                </v-chip>

                <v-spacer></v-spacer>
                <v-btn
                  color="success"
                  :to="{
                    name: 'OrderInfo',
                    params: {
                      order_id: order.uid,
                      backWardRouteName: 'SeekOrder',
                    },
                  }"
                  >详细</v-btn
                >
              </v-layout>
            </v-layout>
          </v-card-title>
          <v-card-text class="col-12 text-sm-body-2 text-truncate-20">
            召集令概述:
            {{ order.info }}
          </v-card-text>
          <v-card-title>
            <v-spacer></v-spacer>

            <v-dialog
              v-model="order.switcher"
              scrollable
              :overlay="false"
              max-width="35rem"
              transition="dialog-transition"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  color="primary"
                  v-show="
                    !ordersBeenRequest_uids.includes(order.uid) &&
                    order.currentSummoningCount < order.maximumSummoningCount
                  "
                  >{{ "申请加入" }}</v-btn
                >
              </template>

              <v-card>
                <v-card-title class="headline grey lighten-2">
                  召集令申请
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-textarea
                    label="加入理由"
                    textarea
                    class="pt-12"
                    outlined
                    v-model="requestMsg"
                  ></v-textarea>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-text>
                  <v-row justify="center">
                    <v-btn
                      color="primary"
                      @click="
                        requestJoin(order);
                        order.switcher = false;
                      "
                      >提交</v-btn
                    >
                  </v-row>
                </v-card-text>
              </v-card>
            </v-dialog>
            <v-chip
              color="grey"
              label
              v-show="ordersBeenRequest_uids.includes(order.uid)"
              >{{ "已申请" }}</v-chip
            >
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Order from "@/classes/Order.js";
export default {
  // beforeUpdate(){
  //   localStorage.setItem('ordersBeenRequest_uids',JSON.parse(this.ordersBeenRequest_uids));
  // },
  watch: {},
  mounted() {
    // window.onbeforeunload = (e) => {
    //   localStorage.setItem(
    //     "ordersBeenRequest_uids",
    //     JSON.parse(this.ordersBeenRequest_uids)
    //   );
    // };
    // console.log(this.$store.state.requests.map(el => el.uid));
    this.getAllOrder();
    // if (this.ordersBeenRequest_uids === undefined) {
    //   this.ordersBeenRequest_uids = localStorage.getItem(
    //     "ordersBeenRequest_uids"
    //   );
    // }
    // console.log(this.selectedTypeKeys)
  },
  computed: {},
  data() {
    return {
      ordersBeenRequest_uids: this.$store.state.requests.map(
        (el) => el.order_id
      ),

      selectedType: new Array(),
      selectOptions: [
        { text: "技术交流", value: 0 },
        { text: "学业探讨", value: 1 },
        { text: "社会实践", value: 2 },
        { text: "公益志愿者", value: 3 },
        { text: "游玩", value: 4 },
      ],
      requestMsg: "",
      // selectypes:["社会实践", "公益志愿者"],
      // selectOptions: ["技术交流", "学业探讨", "社会实践", "公益志愿者", "游玩"],

      // selectOptions: {"技术交流":0, "学业探讨":1, "社会实践":2, "公益志愿者":3, "游玩":4},
      color: ["error", "warning", "success", "primary"],
      orderList: new Array(),
    };
  },
  methods: {
    selectionFilter(obj) {
      if (this.selectedTypeKeys.length > 0) {
        return this.selectedTypeKeys.includes(obj);
      }
      return true;
    },
    getAllOrder() {
      this.axios
        .get("api/tasks", {
          params: { all: true },
        })
        .then((res) => {
          if (res.status === 200) {
            const dataList = res.data;
            this.orderList = new Array();
            for (let each of dataList) {
              this.orderList.push(new Order(each));
            }
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    requestJoin(order) {
      this.axios
        .post("api/requests", {
          option: "10",
          order_id: order.uid,
          slave_id: this.$store.state.userInfo.uid,
          request_msg: this.requestMsg,
          requester_name: this.$store.state.userInfo.nick_name,
        })
        .then((res) => {
          if (res.status === 200) {
            const requestData = res.data;
            alert("申请成功");
            this.ordersBeenRequest_uids.push(order.uid);
            this.$store.commit("appendRequest", requestData);
          } else if (res.status === 400) {
            alert("召集人数已满");
            // alert(res.data.toString());
            order.currentSummoningCount = order.maximumSummoningCount;
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style>
</style>