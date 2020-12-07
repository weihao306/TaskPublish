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
          v-for="(request,index) of requestList"
          :key="request.key"
        >
          <v-card-title
            primary-title
            class="text-justify text-h5 font-weight-bold pb-1"
          >
            {{ request.order_name }}
          </v-card-title>
          <v-card-title class="py-1">
            <v-chip
              ref="requestStatus"
              dark
              :color="statusColor[request.state]"
              >{{ requestStatus[request.state] }}</v-chip
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
                <v-card-text class="pt-12">
                  <v-textarea
                    label="加入理由"
                    outlined
                    v-model="modifyRequest.msg"
                  ></v-textarea>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-title>
                  <v-spacer></v-spacer>
                  <v-btn
                    color="success"
                    @click="
                      modifyRequestAction(request, modifyRequest);
                      request.switcher = false;
                    "
                    >提交</v-btn
                  >
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
                @click="deleteRequestAction(request,index)"
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
                    ref="requestStatus"
                    dark
                    :color="statusColor[order.status]"
                    >{{ requestStatus[order.status] }}</v-chip
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
                        order_id: order.uid,
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
  // computed: {
  //   ordersBeenRequest_uids: (vm) => [
  //     ...vm.$store.state.requestList.map((obj) => obj.order_id),
  //   ],
  // },
  data() {
    return {
      orderList: [],
      requestList: [],
      // requestStatus: ["等待同意", "响应", "拒绝"],
      requestStatus: { 0: "等待同意", 1: "同意", 2: "拒绝" },
      orderStatus: { 0: "等待召集", 1: "召集中" ,2:"已删除",3:"逾期"},
      statusColor: ["warning", "success", "error"],
      joinRequests: [
        {
          order_uid: undefined,
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
    // for (let i = 0; i < 10; i++) {
    //   this.orderList.push(
    //     new Order({
    //       uid: 111,
    //       name: "test " + i,
    //       info:
    //         "testingjdialsjdialshdhaisdsahjnikdsahjikdjhasjdlasjildjalinljdiasildaskjdialsjdiajdaslijdajdlikjislajdilajlik",
    //       currentSummonginCount: 1,
    //       maximumSummonginCount: 32,
    //       status: 0,
    //     })
    //   );
    // }
    // this.getOrderList();
    this.getRequestList(this.$store.state.userInfo.uid);
  },
  methods: {
    getOrderList() {
      this.axios
        .get("api/tasks", { params: { slave_id: this.$store.state.uid } })
        .then((res) => {
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
            this.requestList = [];
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
    modifyOrderAction(order, index) {
      order.modifyInfo = false;
    },
    deleteOrderAction(order, index) {
      order.deleteInfo = false;
      this.axios
        .delete("api/tasks", { uid: order.uid })
        .then((res) => {
          this.orderList.splice(index, 1);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    modifyRequestAction(request, putInfo) {
      this.axios
        .put("api/requests", {
          option: "11",
          request_id: request.uid,
          request_name: putInfo.name,
          request_msg: putInfo.msg,
        })
        .then((res) => {
          if (res.status === 200) {
            console.log(res.data);
            // const newRequestObj = {
            //   "name":res.data['requester_name'],
            //   "msg":res.data['description']
            // }
            const newRequestObj = res.data;
            request.updateMsg(newRequestObj["msg"]);
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    deleteRequestAction(request, index) {
      this.axios
        .delete("api/requests", {
          params: { option: '13', request_id: request.uid },
        })
        .then((res) => {
          if(res.status===200){
            console.log("delete request OK")
            this.requestList.splice(index,1);
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>

<style>
</style>