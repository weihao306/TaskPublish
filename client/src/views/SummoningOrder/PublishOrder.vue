<template>
  <v-container grid-list-xs fluid>
    <v-row justify="center">
      <v-col>
        <v-btn fixed color="white" x-small fab :to="{ name: 'Master' }"
          ><v-icon>mdi-arrow-left</v-icon></v-btn
        >
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="11" sm="10" md="8" lg="6">
        <v-card class="mx-auto my-auto elevation-8" outlined>
          <v-card-text>
            <v-row justify="center">
              <blockquote
                class="text-center text-justify text-h6 font-weight-bold mb-3"
              >
                召集令信息
              </blockquote>
              <v-col cols="12">
                <v-text-field
                  outlined
                  name="name"
                  v-model="publishOrderInfo.name"
                  placeholder="召集令标题"
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  :items="orderType"
                  v-model="publishOrderInfo.type"
                  placeholder="召集令类型"
                  outlined
                  hide-details
                  class="mb-3"
                  :menu-props="{ maxHeight: '10rem' }"
                ></v-select>
              </v-col>
            </v-row>
            <v-textarea
              color="black"
              placeholder="填写召集令信息"
              auto-grow
              filled
              outlined
              counter="200"
              maxlength="200"
              v-model="publishOrderInfo.info"
              :rules="[
                () => publishOrderInfo.info.length <= 200 || '最多200字',
              ]"
            >
            </v-textarea>
          </v-card-text>

          <v-layout row wrap justify-center class="my-3">
            <v-flex xs12 sm5 md4>
              <v-layout row wrap class="justify-center my-1">
                <blockquote class="text-justify text-h6 font-weight-bold">
                  召集最大人数
                </blockquote>
              </v-layout>
            </v-flex>
            <v-flex xs8 sm4 md4 class="justify-center align-center my-1">
              <v-row no-gutters justify="center" align-content="center">
                <v-col cols="3">
                  <v-btn
                    ma-0
                    small
                    dark
                    block
                    width="1"
                    color="primary"
                    class="white--text align-self-center"
                    @click="
                      () => {
                        publishOrderInfo.maximumSummoningCount = parseInt(
                          publishOrderInfo.maximumSummoningCount
                        );
                        publishOrderInfo.maximumSummoningCount -=
                          publishOrderInfo.maximumSummoningCount > 0 ? 1 : 0;
                      }
                    "
                  >
                    <v-icon>mdi-minus</v-icon>
                  </v-btn>
                </v-col>
                <v-col cols="6">
                  <v-text-field
                    v-model="publishOrderInfo.maximumSummoningCount"
                    dense
                    type="Number"
                    messages="max 200"
                    hint="max 200"
                    d-flex
                    @change="
                      publishOrderInfo.maximumSummoningCount = parseInt(
                        publishOrderInfo.maximumSummoningCount
                      )
                    "
                    max-width="2rem"
                    class="Height_24"
                    oninput="if(parseInt(value)>200)value=200;if(parseInt(value)<0)value=0;"
                    :rules="[]"
                  >
                  </v-text-field>
                </v-col>
                <v-col cols="3">
                  <v-btn
                    small
                    dark
                    block
                    width="1"
                    color="red"
                    class="white--text align-self-center"
                    @click="
                      () => {
                        publishOrderInfo.maximumSummoningCount = parseInt(
                          publishOrderInfo.maximumSummoningCount
                        );
                        publishOrderInfo.maximumSummoningCount +=
                          publishOrderInfo.maximumSummoningCount < 200 ? 1 : 0;
                      }
                    "
                  >
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </v-flex>
          </v-layout>

          <v-layout row wrap justify-center>
            <v-flex xs8 sm4 md4 class="align-center my-1">
              <v-menu
                ref="menu"
                v-model="menu"
                :close-on-content-click="false"
                :return-value.sync="date"
                transition="scale-transition"
                offset-y
                max-width="30rem"
                min-width="16rem"
                class="col-8"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                    name="time"
                    label="活动截止时间"
                    v-model="publishOrderInfo.end_date"
                    style="text-align-last: center"
                    prepend-icon="mdi-calendar"
                    readonly
                    v-bind="attrs"
                    v-on="on"
                    outlined
                    dense
                  ></v-text-field>
                </template>
                <v-date-picker v-model="publishOrderInfo.end_date" scrollable>
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="menu = false">
                    取消
                  </v-btn>
                  <v-btn
                    text
                    color="primary"
                    @click="$refs.menu.save(publishOrderInfo.end_date)"
                  >
                    OK
                  </v-btn>
                </v-date-picker>
              </v-menu>
            </v-flex>
          </v-layout>

          <v-layout row wrap justify-center class="mt-6">
            <v-flex xs10 sm4>
              <nav
                class="text-justify text-h6 font-weight-bold"
                style="text-align-last: center"
              >
                上传照片
              </nav>
            </v-flex>
            <v-flex xs10 sm4>
              <v-file-input
                dense
                counter
                multiple
                show-size
                small-chips
                :truncate-length="modifyTruncateLength()"
                outlined
                accept="image/*"
                v-model="uploadPhotos"
                full-width
                @change="getPhotoUrls(uploadPhotos)"
                clearable
                clear-icon="mdi-close-thick"
              >
              </v-file-input>
            </v-flex>
          </v-layout>

          <v-layout row wrap justify-center>
            <v-flex xs11>
              <!-- <v-carousel v-model="selectedPhoto" height="50vh">
                <v-carousel-item v-for="img of imgs" :key="img.key" :src="img">
                </v-carousel-item>
              </v-carousel> -->

              <!-- <img v-for="img of imgs" :key="img.key" :src="img"> -->
              <v-window v-model="onboarding">
                <v-window-item
                  v-for="(img, n1) of publishOrderInfo.photos"
                  :key="`card-${n1}`"
                >
                  <v-card class="mx-auto my-auto elevation-8">
                    <v-img contain :src="img" height="30vh"> </v-img>
                    <!-- <v-card-title primary-title> </v-card-title> -->
                  </v-card>
                </v-window-item>
              </v-window>
              <v-item-group
                v-model="onboarding"
                mandatory
                class="text-center justify-center"
              >
                <v-item
                  v-for="(img, n2) of publishOrderInfo.photos"
                  :key="`btn-${n2}`"
                >
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
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="success" @click="publishNewOrder()">发布召集令</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import OrderInfo from "@/classes/OrderInfo";
export default {
  mounted() {
    this.publishOrderInfo.maximumSummoningCount = 0;
    this.publishOrderInfo.master_id = this.$store.state.userInfo.uid;
  },
  data() {
    return {
      onboarding: 0,

      publishOrderInfo: new OrderInfo(),

      maximumCount: 0,
      uploadPhotos: [],
      imgs: [],
      orderType: [
        { text: "技术交流", value: 0 },
        { text: "学业探讨", value: 1 },
        { text: "社会实践", value: 2 },
        { text: "公益志愿者", value: 3 },
        { text: "游玩", value: 4 },
      ],
      orderSelectedType: undefined,
      selectedPhoto: 0,
      photoUrls: [],
      colors: ["red", "success", "warning", "primary"],
    };
  },
  methods: {
    modifyTruncateLength: function () {
      const width = window.screen.width;
      if (width <= 380) {
        return 1;
      } else if (width <= 420) {
        return 2;
      } else if (width <= 768) {
        return 6;
      } else {
        return 10;
      }
    },
    getPhotoUrls(files) {
      console.log(files);
      let fr = new FileReader();
      let url = undefined;
      for (let file of files) {
        fr.readAsDataURL(file);
        fr.onload = () => {
          // url = this.result;
          // tmpUrl = this.result.substring(this.result.indexOf(",") + 1);
          // url = "data:image/*;base64," + tmpUrl;
          url = fr.result;
          console.log(url);
          this.publishOrderInfo.photos.unshift(fr.result);
        };
      }
    },
    getPhotoUrl(file) {
      let fr = new FileReader();
      let url = undefined;
      fr.readAsDataURL(file);
      fr.onloadend = (e) => {
        // url = this.result;
        // tmpUrl = this.result.substring(this.result.indexOf(",") + 1);
        // url = "data:image/*;base64," + tmpUrl;
        url = fr.result;
        this.publishOrderInfo.photos.push(fr.result);
      };
      return url;
    },
    publishNewOrder() {
      // 开始时间
      this.publishOrderInfo.start_date = new Date().toLocaleDateString().split('/').join('-');
      if (
        (this.publishOrderInfo.name !== undefined ||
          this.publishOrderInfo.name !== "") &&
        // this.publishOrderInfo.type instanceof Number &&
        this.publishOrderInfo.maximumSummoningCount > 0 &&
        (this.publishOrderInfo.end_date !== undefined ||
          this.publishOrderInfo.end_date !== "")
      ) {
        this.axios
          .post("api/tasks", {
            master_id: this.$store.state.userInfo.uid,
            task_type: this.publishOrderInfo.type,
            task_name: this.publishOrderInfo.name,
            description: this.publishOrderInfo.info,
            cur_people: this.publishOrderInfo.currentSummoningCount,
            max_people: this.publishOrderInfo.maximumSummoningCount,
            start_time: this.publishOrderInfo.start_date,
            end_time: this.publishOrderInfo.end_date,
            task_status: this.publishOrderInfo.status,
            photos: JSON.stringify(this.publishOrderInfo.photos),
          })
          .then((res) => {
            if (res.status === 200) {
              alert("发布成功");
              this.$router.push({ name: "Master" });
            }
          })
          .catch((err) => {
            console.error(err);
          });
      } else {
        alert("完整填写信息");
      }
    },

    next() {
      this.onboarding = (this.onboarding + 1) % this.length;
    },
    prev() {
      this.onboarding = (this.onboarding + this.length - 1) % this.length;
    },
  },
  watch: {
    uploadPhotos() {
      if (this.uploadPhotos.length === 0) {
        while (this.publishOrderInfo.photos.length !== 0) {
          this.publishOrderInfo.photos.pop();
        }
      }
    },
    // publishOrderInfo: {
    //   handler(oldVal, newVal) {
    //     if (
    //       !this.$data.publishOrderInfo.maximumSummoningCount instanceof Number
    //     ) {
    //       this.$data.publishOrderInfo.maximumSummoningCount = new Number(
    //         newVal
    //       );
    //     }
    //     if (newVal > 200 || newVal < 0) {
    //       this.$data.publishOrderInfo.maximumSummoningCount = oldVal;
    //     }
    //   },
    //   immediate: true,
    //   deep: true,
    // },
  },
};
</script>

<style lang="css">
/* 去除input框内的上下箭头 */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
  text-align: center;
}
.Height_24 input {
  height: 24px;
  font-size: 24px;
  text-align-last: center;
  text-align: center;
}
/* hack */
.v-messages__message {
  text-align: center;
}
</style>
