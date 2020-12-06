<template>
  <v-container grid-list-xs fluid>
    <v-row justify="center">
      <v-col>
        <v-btn
          fixed
          color="white"
          x-small
          fab
          :to="{ name: 'SummoningOrderMain' }"
          ><v-icon>mdi-arrow-left</v-icon></v-btn
        >
      </v-col>
    </v-row>
    <v-row justify="center">
      <v-col cols="11" sm="11" md="8" lg="6">
        <v-card class="mx-auto mb-3 elevation-8" max-height="10rem" outlined>
          <v-layout column wrap>
            <v-flex align-self-center>
              <v-card-text>
                <blockquote class="text-justify text-h5 font-weight-bold">
                  新的召集令
                </blockquote>
              </v-card-text>
            </v-flex>
            <v-flex align-self-center>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="success"
                  :to="{
                    name: 'SeekOrder',
                    params: {
                      ordersBeenRequest_uuids: ordersBeenRequest_uuids,
                    },
                  }"
                  >寻找召集令</v-btn
                >
              </v-card-actions>
            </v-flex>
          </v-layout>
        </v-card>

        <!-- 召集令申请状况 -->
        <v-subheader class="text-justify text-h5 font-weight-bold"
          >召集令申请状况</v-subheader
        >
        <v-divider></v-divider>

        <v-card
          class="mx-auto my-3 elevation-8"
          outlined
          v-for="request of requestList"
          :key="request.key"
        >
          <v-card-title
            primary-title
            class="text-justify text-h5 font-weight-bold pb-1"
          >
            {{ request.name }}
            
          </v-card-title>
          <v-card-title class="py-1">
            <v-chip
              ref="orderStatus"
              dark
              :color="statusColor[request.state]"
              >{{ orderStatus[request.state] }}</v-chip
            >
            <v-spacer></v-spacer>

            <v-dialog
              v-model="request.switcher"
              scrollable
              :overlay="false"
              max-width="35rem"
              transition="dialog-transition"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  v-bind="attrs"
                  v-on="on"
                  color="grey"
                  v-show="request.state === 0"
                  >修改</v-btn
                >
              </template>

              <v-card>
                <v-card-title class="headline grey lighten-2">
                  申请信息
                </v-card-title>
                <v-divider></v-divider>
                <v-card-text class="pt-8">
                  <v-text-field
                    label="标题"
                    outlined
                    v-model="modifyRequest.name"
                  ></v-text-field>
                  <v-textarea
                    label="加入理由"
                    outlined
                    v-model="modifyRequest.msg"
                  ></v-textarea>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-title>
                  <v-spacer></v-spacer>
                  <v-btn color="success">提交</v-btn>
                </v-card-title>
              </v-card>
            </v-dialog>
          </v-card-title>
          <v-card-text class="text-justify text-h6 font-weight-bold">
            <nav>申请信息:</nav>
            <nav>
              {{ request.msg }}
            </nav>
          </v-card-text>
          <v-card-text>
            <v-layout row wrap justify-end>
              <v-btn
                color="error"
                v-show="request.state === 0 || request.state === 2"
                >撤回</v-btn
              >
            </v-layout>
          </v-card-text>
        </v-card>

        <!-- 已经响应的召集令 -->
        <v-subheader class="text-justify text-h5 font-weight-bold"
          >已经响应的召集令</v-subheader
        >
        <v-divider></v-divider>

        <v-card
          class="mx-auto my-3 elevation-8"
          outlined
          v-for="order of orderList"
          :key="order.key"
        >
          <v-card-title class="headline lighten-2">
            <nav class="text-justify text-h5 font-weight-bold">
              {{ order.name }}
            </nav>
          </v-card-title>
          <v-card-text>
            <v-layout column wrap>
              <v-flex xs12>
                <v-layout row wrap>
                  <v-chip
                    ref="orderStatus"
                    dark
                    :color="statusColor[order.status]"
                    >{{ orderStatus[order.status] }}</v-chip
                  >
                  <v-spacer></v-spacer>
                  <v-btn
                    color="success"
                    dark
                    d-flex
                    max-width="5rem"
                    :to="{
                      name: 'OrderInfo',
                      params: {
                        order_id: order.uuid,
                        backWardRouteName: 'Masses',
                      },
                    }"
                    >详细</v-btn
                  >
                </v-layout>
              </v-flex>
              <v-flex xs12>
                <v-row>
                  <blockquote class="col-12 text-sm-body-2 text-truncate-20">
                    召集令概述:
                    {{ order.info }}
                  </blockquote>
                </v-row>
              </v-flex>
            </v-layout>
          </v-card-text>
          <!-- actions -->
          <v-card-text>
            <v-layout row wrap>
              <v-chip flat
                >人数 {{ order.currentSummoningCount }}/{{
                  order.maximumSummoningCount
                }}</v-chip
              >
              <v-spacer></v-spacer>
              <!-- <v-dialog
                v-model="order.deleteInfo"
                scrollable
                :overlay="false"
                transition="dialog-transition"
                max-width="35rem"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    d-flex
                    max-width="5rem"
                    color="error"
                    dark
                    v-bind="attrs"
                    v-on="on"
                    class="ml-2"
                  >
                    退出
                  </v-btn>
                </template>

                <v-card>
                  <v-card-title class="headline grey lighten-2">
                    确认是否退出 {{ order.name }} 召集令?
                  </v-card-title>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                      color="error"
                      @click="deleteInfoAction(order, index)"
                    >
                      确认
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog> -->
            </v-layout>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Order from "@/classes/Order.js";
import Request from "@/classes/Request.js";
export default {
  computed: {
    ordersBeenRequest_uuids: (vm) => [
      ...vm.requestList.map((obj) => obj.order_id),
    ],
  },
  data() {
    return {
      orderList: [],
      requestList: [],
      orderStatus: ["等待同意", "响应", "拒绝"],
      statusColor: ["warning", "success", "error"],
      joinRequests: [
        {
          order_uuid: undefined,
          request_msg: undefined,
        },
      ],
      modifyRequest: {
        name: undefined,
        msg: undefined,
      },
    };
  },
  mounted() {
    for (let i = 0; i < 10; i++) {
      this.orderList.push(
        new Order({
          uuid: 111,
          name: "test " + i,
          info:
            "testingjdialsjdialshdhaisdsahjnikdsahjikdjhasjdlasjildjalinljdiasildaskjdialsjdiajdaslijdajdlikjislajdilajlik",
          currentSummonginCount: 1,
          maximumSummonginCount: 32,
          status: 0,
        })
      );
    }

    this.getRequestList(this.$store.state.userInfo.uuid);
  },
  methods: {
    getOrderList() {
      this.axios.get("api/tasks").then((res) => {
        const data = res.data;
        for (let each of data) {
          let newOrder = new Order(each);
          this.orderList.push(newOrder);
          newOrder = null;
        }
      });
    },
    getRequestList(slave_id) {
      this.axios
          .get("api/requests", {
          params: { option: "12", slave_id: slave_id },
        })
        .then((res) => {
          if (res.status === 200) {
            const requestListObj = res.data;
            console.log(requestListObj);
            for (let each of requestListObj) {
              this.requestList.push(new Request(each));
            }
            this.$store.commit("saveRequests", this.requestList);
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    modifyInfoAction(order, index) {
      order.modifyInfo = false;
    },
    deleteInfoAction(order, index) {
      order.deleteInfo = false;
      this.axios
        .delete("api/tasks", {
          params: { uuid: order.uuid },
        })
        .then((res) => {
          this.orderList.splice(index, 1);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    modifyRequestAction(request) {
      this.axios
        .put("api/requests", {
          params: {
            option: "11",
            request_id: request.uuid,
            request_msg: request.msg,
          },
        })
        .then((res) => {
          if (res.status === 200) {
            console.log(res.data);
            const newRequestObj = res.data;
            request.updateMsg(newRequestObj["msg"]);
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