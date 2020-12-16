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

        <!-- <card>
          <template v-slot:title>
            <v-layout row wrap justify="center">
              <format-text size="mid" center>新的召集令</format-text>
            </v-layout>
          </template>
          <template v-slot:action>
            <v-layout row wrap justify="center">
              <v-btn
                class="TextCenter"
                color="success"
                :to="{ name: 'PublishOrder' }"
                >发布召集令</v-btn
              >
            </v-layout>
          </template>
        </card> -->

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

          <!-- text -->
          <v-card-text class="py-0">
            <v-layout column wrap>
              <v-flex xs12>
                <!-- <v-spacer></v-spacer> -->

                <v-layout row justify-space-between>
                  <v-chip
                    ref="orderStatus"
                    dark
                    class="align-self-center"
                    :color="statusColor[order.status]"
                    >{{ orderStatus[order.status] }}</v-chip
                  >
                  <v-row row wrap justify="end">
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
                          @click="getOrderRequest(order.uid)"
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
                                  申请人:{{ request.requesterName }}
                                  <v-chip
                                    class="mx-2"
                                    ref="orderStatus"
                                    dark
                                    :color="statusColor[request.state]"
                                    >{{ requestStatus[request.state] }}</v-chip
                                  >
                                </v-card-title>

                                <v-card-text
                                  class="col-12 text-justify text-h6 font-weight-bold"
                                >
                                  {{ request.msg }}
                                </v-card-text>
                                <v-card-actions v-show="request.state === 0">
                                  <v-spacer></v-spacer>
                                  <v-btn
                                    color="success"
                                    @click.stop="
                                      acceptTheRequest(index);
                                      order.requestsSwitcher = false;
                                    "
                                    >同意</v-btn
                                  >
                                  <v-btn
                                    color="error"
                                    @click.stop="
                                      denyTheRequest(index);
                                      order.requestsSwitcher = false;
                                    "
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
                          order_id: order.uid,
                          backWardRouteName: 'Master',
                        },
                      }"
                      >详细</v-btn
                    >
                  </v-row>
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
            <v-layout column wrap justify-space-between>
              <v-layout row wrap>
                <v-chip flat
                  >截止时间:{{ order.end_date }}
                </v-chip>
              </v-layout>
            </v-layout>
          </v-card-text>            
          <!-- actions -->
          <v-card-text>
            <v-layout row wrap :justify-space-between="justifyBetween()">
              <v-layout row wrap class="mb-1">
                <v-chip flat
                  >人数 {{ order.currentSummoningCount }}/{{
                    order.maximumSummoningCount
                  }}</v-chip
                >
              </v-layout>
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
                      @click="modifyOrderInit(order)"
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
                            counter="200"
                            maxlength="200"
                            :rules="[
                              () =>
                                (!!modify.info && modify.info.length <= 200) ||
                                '必须不大于200个字',
                            ]"
                          ></v-textarea>
                        </v-flex>
                        <v-flex xs11 sm9 md7>

                          <v-layout row wrap justify-center>
                            <div class="text-h6">召集令类型</div>
                          </v-layout>

                          <v-radio-group row v-model="modify.type">
                            <v-radio
                              class="my-2"
                              v-for="(selection, index) of order_types"
                              :key="index"
                              :label="selection.text"
                            ></v-radio>
                          </v-radio-group>
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
                        @click="modifyOrderAction(order, modify, index)"
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
import Card from "@/components/Card.vue";
import FormatText from "@/components/FormatText.vue";
export default {
  components: {
    // card:()=>import("@/components/Card.vue")
    Card,
    FormatText,
  },
  data() {
    return {
      trueValue: true,
      testDate: new Date("2020-12-6"),
      date: new Date(),
      orderList: [],
      requestList: [],
      orderStatus: this.$store.state.orderStatus,
      statusColor: this.$store.state.statusColor,
      requestStatus: this.$store.state.requestStatus,
      order_types: [
        { text: "技术交流", type: 0, value: false },
        { text: "学业探讨", type: 1, value: false },
        { text: "社会实践", type: 2, value: false },
        { text: "公益志愿者", type: 3, value: false },
        { text: "游玩", type: 4, value: false },
      ],
      modify: {
        name: null,
        info: null,
        type: null,
      },
    };
  },
  mounted() {
    // for (let i = 0; i < 10; i++) {
    //   this.orderList.push(
    //     new Order({
    //       uid: 123,
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
          params: { master_id: this.$store.state.userInfo.uid },
        })
        .then((res) => {
          const data = res.data;
          if (res.status === 200) {
            for (let each of data) {
              let newOrder = new Order(each);
              this.orderList.push(newOrder);
              newOrder = null;
            }
            this.$store.commit("saveOrders", this.orderList);
          }
        });
    },
    getOrderRequest(order_id) {
      this.axios
        .get("api/requests", { params: { option: "00", order_id: order_id } })
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
    modifyOrderInit(order) {
      this.modify.name = order.name;
      this.modify.info = order.info;
      this.modify.type = order.type;
      // this.order_types[order.type].value = true;
    },
    modifyOrderAction(order, putInfo, index) {
      if (putInfo.info.length > 200) {
        alert("必须不大于200个字");
      } else {
        order.modifyDialogSwitcher = false;
        this.axios
          .put("api/tasks", {
            order_id: order.uid,
            order_name: putInfo.name,
            order_description: putInfo.info,
            order_type: putInfo.type,
          })
          .then((res) => {
            if (res.status === 200) {
              order.name = putInfo.name;
              order.info = putInfo.info;
              order.type = putInfo.type;
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
        .delete("api/tasks", { params: { order_id: order.uid } })
        .then((res) => {
          if (res.status === 200) {
            this.orderList.splice(index, 1);
          } else {
            alert("删除失败");
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    acceptTheRequest(index) {
      this.updateRequest(index, 1);
    },
    denyTheRequest(index) {
      this.updateRequest(index, 0);
    },
    updateRequest(index, state) {
      let request = this.requestList[index];
      this.axios
        .put("api/requests", {
          option: "01",
          request_id: request.uid,
          state: state ? "accepted" : "denied",
          time: this.date.toLocaleDateString().split("/").join("-"),
        })
        .then((res) => {
          if (res.status === 200) {
            const requestObj = res.data;
            request.updateState(state);
            if (state) {
              this.orderList[index].currentSummoningCount++;
            }
            // console.log(requestObj);
          } else {
            console.log("发送失败");
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    updateOverTimeOrder(){

    }
  },
};
</script>

<style lang="css">
.TextCenter {
  text-align: center;
  text-align-last: center;
}
</style>