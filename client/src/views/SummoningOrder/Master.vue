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
                <v-btn color="success" :to="{ name: 'PublishOrder' }"
                  >发布召集令</v-btn
                >
              </v-card-actions>
            </v-flex>
          </v-layout>
        </v-card>

        <v-card
          class="mx-auto my-3 elevation-8"
          outlined
          v-for="(order, index) of orderList"
          :key="order.key"
        >
          <v-card-title class="headline lighten-2">
            <nav class="text-h5 font-weight-bold">
              {{ order.name }}
            </nav>
          </v-card-title>

          <v-card-text>
            <v-layout column wrap>
              <v-flex xs12>
                <!-- <v-spacer></v-spacer> -->

                <v-layout row justify-end>
                  <v-chip
                    ref="orderStatus"
                    dark
                    :color="statusColor[order.status]"
                    >{{ orderStatus[order.status] }}</v-chip
                  >
                  <v-spacer></v-spacer>
                  <v-dialog
                    v-model="order.requestsSwitcher"
                    :overlay="false"
                    max-width="35rem"
                    transition="dialog-transition"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        dark
                        color="warning"
                        v-bind="attrs"
                        v-on="on"
                        class="mr-2"
                        @click="getOrderRequest(order.uuid)"
                      >
                        申请情况
                      </v-btn>
                    </template>

                    <v-card>
                      <v-card-title class="headline grey lighten-2">
                        申请情况
                      </v-card-title>
                      <v-divider></v-divider>
                      <v-card-text>
                        <v-layout row wrap>
                          <v-flex xs12>
                            <v-card
                              class="mx-auto my-3 elevation-8"
                              outlined
                              v-for="(request, index) of requestList"
                              :key="request.key"
                            >
                              <v-card-title
                                class="text-justify text-h5 font-weight-bold"
                              >
                                {{ request.name }}

                                <v-chip
                                  class="mx-2"
                                  ref="orderStatus"
                                  dark
                                  :color="statusColor[request.state]"
                                  >{{ requestStatus[request.state] }}</v-chip
                                >
                              </v-card-title>

                              <v-card-text>
                                <blockquote
                                  class="text-justify text-h5 font-weight-bold"
                                >
                                  申请人:{{ request.requestUserName }}
                                </blockquote>
                              </v-card-text>
                              <v-card-actions v-show="request.state === 0">
                                <v-spacer></v-spacer>
                                <v-btn
                                  color="success"
                                  @click.stop="acceptTheRequest(index)"
                                  >同意</v-btn
                                >
                                <v-btn
                                  color="error"
                                  @click.stop="denyTheRequest(index)"
                                  >拒绝</v-btn
                                >
                              </v-card-actions>
                            </v-card>
                          </v-flex>
                        </v-layout>
                      </v-card-text>
                      <!-- <v-divider></v-divider>
                          <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn
                              color="primary"
                              @click="order.requestsSwitcher = false"
                              text
                              >完成</v-btn
                            >
                          </v-card-actions> -->
                    </v-card>
                  </v-dialog>

                  <v-btn
                    color="success"
                    dark
                    d-flex
                    max-width="5rem"
                    :to="{
                      name: 'OrderInfo',
                      params: {
                        order_id: order.uuid,
                        backWardRouteName: 'Master',
                      },
                    }"
                    >详细</v-btn
                  >
                </v-layout>
              </v-flex>
            </v-layout>
            <v-flex xs12>
              <v-row>
                <blockquote class="col-12 text-sm-body-2 text-truncate-20">
                  召集令概述:
                  {{ order.info }}
                </blockquote>
              </v-row>
            </v-flex>
          </v-card-text>
          <!-- actions -->
          <v-card-text>
            <v-layout row wrap :justify-space-between="justifyBetween()">
              <v-chip flat
                >人数 {{ order.currentSummoningCount }}/{{
                  order.maximumSummoningCount
                }}</v-chip
              >
              <v-spacer></v-spacer>
              <v-layout
                row
                wrap
                justify-end
                v-show="order.currentSummoningCount === 0"
              >
                <v-dialog
                  v-model="order.modifyDialogSwitcher"
                  scrollable
                  persistent
                  :overlay="false"
                  transition="dialog-transition"
                  max-width="35rem"
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      d-flex
                      max-width="5rem"
                      color="grey"
                      dark
                      v-bind="attrs"
                      v-on="on"
                      @click.stop="modifyInfoInit(order)"
                    >
                      修改信息
                    </v-btn>
                  </template>

                  <v-card>
                    <v-card-title class="headline grey lighten-2">
                      召集令信息修改
                    </v-card-title>

                    <v-card-text>
                      <v-layout row wrap justify-center>
                        <v-flex xs11 sm9 md7>
                          <v-text-field
                            v-model="modify.name"
                            label="召集令标题"
                          ></v-text-field>
                        </v-flex>
                        <v-flex xs11 sm9 md7>
                          <v-textarea
                            v-model="modify.info"
                            label="召集令信息"
                            type="input"
                            required
                            outlined
                            auto-grow
                            counter="20"
                            maxlength="20"
                            :rules="[
                              () =>
                                (!!modify.info && modify.info.length <= 20) ||
                                '必须不大于20个字',
                            ]"
                          ></v-textarea>
                        </v-flex>
                      </v-layout>
                    </v-card-text>

                    <v-divider></v-divider>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="primary"
                        text
                        @click="order.modifyDialogSwitcher = false"
                      >
                        取消
                      </v-btn>
                      <v-btn
                        color="primary"
                        text
                        @click="modifyInfoAction(order, modify, index)"
                      >
                        完成
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>

                <v-dialog
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
                      删除
                    </v-btn>
                  </template>

                  <v-card>
                    <v-card-title class="headline grey lighten-2">
                      确认是否删除 {{ order.name }} 召集令?
                    </v-card-title>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="error"
                        @click="deleteInfoAction(order, index)"
                      >
                        确认删除
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-layout>
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
  data() {
    return {
      date: new Date(),
      orderList: [],
      requestList: [],
      orderStatus: { 0: "等待召集", 1: "召集中" },
      statusColor: { 0: "warning", 1: "success", 2: "error" },
      requestStatus: { 0: "等待处理", 1: "同意", 2: "拒绝" },
      modify: {
        name: null,
        info: null,
      },
    };
  },
  mounted() {
    // for (let i = 0; i < 10; i++) {
    //   this.orderList.push(
    //     new Order({
    //       uuid: 123,
    //       name: "test " + i,
    //       info: "testingdasuhduahdhasdhsaklhduikjahduaikshndukasjh",
    //       currentSummoningCount: 0,
    //       maximumSummoningCount: 32,
    //       status: 0,
    //     })
    //   );
    // this.requestList.push();
    // }
    this.getOrderList();
  },
  methods: {
    justifyBetween() {
      return this.$vuetify.breakpoint.name === "xs";
    },
    getOrderList() {
      this.axios
        .get("api/tasks", {
          params: { master_id: this.$store.state.userInfo.uuid },
        })
        .then((res) => {
          const data = res.data;
          for (let each of data) {
            let newOrder = new Order(each);
            this.orderList.push(newOrder);
            newOrder = null;
          }
          this.$store.commit("saveOrders", this.orderList);
        });
    },
    getOrderRequest(order_id) {
      this.axios
        .get("api/requests", { params: { order_id: order_id } })
        .then((res) => {
          if (res.status === 200) {
            this.requestList = [];
            const tmpList = res.data;
            console.log(tmpList);
            for (let each of tmpList) {
              this.requestList.push(new Request(each));
            }
          }
        });
    },
    modifyInfoInit(order) {
      this.modify.name = order.name;
      this.modify.info = order.info;
    },
    modifyInfoAction(order, putInfo, index) {
      if (putInfo.info.length > 20) {
        alert("必须不大于20个字");
      } else {
        order.modifyDialogSwitcher = false;
        this.axios
          .put("api/tasks", {
            params: {
              uuid: order.uuid,
              name: putInfo.name,
              info: putInfo.info,
            },
          })
          .then((res) => {
            if (res.status === 200) {
              order.name = this.modify.name;
              order.info = this.modify.info;
            }
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
    deleteInfoAction(order, index) {
      order.deleteInfo = false;
      this.axios
        .delete("api/tasks", {
          params: { uuid: order.uuid },
        })
        .then((res) => {
          if (res.status === 200) {
            this.orderList.splice(index, 1);
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    acceptTheRequest(index) {
      let request = this.requestList[index];
      this.axios
        .put("api/requests", {
          params: {
            option: "01",
            request_id: request.uuid,
            state: 1,
            time: this.date.toLocaleDateString(),
          },
        })
        .then((res) => {
          if (res.status === 200) {
            const requestObj = res.data;
            request.updateState(requestObj["state"]);
            console.log(requestObj);
          } else {
            console.log("发送失败");
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    denyTheRequest(index) {
      const request = this.requestList[index];
      this.axios
        .put("api/requests", {
          params: {
            option: "01",
            request_id: request.uuid,
            state: 0,
            time: this.date.toLocaleDateString(),
          },
        })
        .then((res) => {
          if (res.status === 200) {
            const requestObj = res.data;
            request.updateState(requestObj["state"]);
            console.log(requestObj);
          } else {
            console.log("发送失败");
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