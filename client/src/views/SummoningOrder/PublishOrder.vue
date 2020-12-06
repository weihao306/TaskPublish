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
                  label="召集令标题"
                  v-model="publishOrderInfo.name"
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  :items="orderType"
                  v-model="publishOrderInfo.type"
                  label="召集令类型"
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
              hide-details
              v-model="publishOrderInfo.info"
            >
              <!-- <v-progress-linear
            slot="progress"
            value="progress"
            height="7"
            color="primary"
          ></v-progress-linear> -->
            </v-textarea>
          </v-card-text>

          <v-layout row wrap justify-center class="my-3">
            <v-flex xs12 sm4 md4>
              <v-layout row wrap class="justify-center">
                <blockquote class="text-justify text-h6 font-weight-bold">
                  召集最大人数
                </blockquote>
              </v-layout>
            </v-flex>
            <v-flex xs8 sm4 md4 class="justify-center align-center">
              <div mandatory multiple>
                <v-layout row wrap>
                  <v-flex>
                    <v-btn
                      small
                      dark
                      block
                      width="1"
                      class="white--text"
                      color="primary"
                      @click="maximumCount -= 1"
                    >
                      <v-icon>mdi-minus</v-icon>
                    </v-btn>
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      v-model="publishOrderInfo.maximumSummoningCount"
                      dense
                      hide-details
                      size="6"
                      style="text-align-last: center"
                    >
                      <!-- <v-icon slot="append" color="red"></v-icon>
                    <v-icon slot="prepend" color="primary"></v-icon>-->
                    </v-text-field>
                  </v-flex>
                  <v-flex>
                    <v-btn
                      small
                      dark
                      block
                      width="1"
                      class="white--text"
                      color="red"
                      @click="maximumCount += 1"
                    >
                      <v-icon>mdi-plus</v-icon>
                    </v-btn>
                  </v-flex>
                </v-layout>
              </div>
            </v-flex>
          </v-layout>

          <v-layout row wrap justify-center>
            <v-flex xs3 mt-1>
              <blockquote class="text-justify text-h6 font-weight-bold">
                上传照片
              </blockquote>
            </v-flex>
            <v-flex xs6>
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
              <v-carousel v-model="selectedPhoto" height="30vh">
                <v-carousel-item v-for="img of imgs" :key="img.key" :src="img">
                  <!-- <img v-for="img of imgs" :key="img.key" :src="img"> -->
                </v-carousel-item>
              </v-carousel>
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
  data() {
    return {
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
        fr.onload = (e) => {
          // url = this.result;
          // tmpUrl = this.result.substring(this.result.indexOf(",") + 1);
          // url = "data:image/*;base64," + tmpUrl;
          url = fr.result;
          console.log(url);
          this.imgs.push(fr.result);
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
        this.imgs.push(fr.result);
      };
      return url;
    },
    publishNewOrder() {
      this.axios
        .post("api/tasks",{
          master_id: this.$store.state.userInfo.uid,
          task_type: this.publishOrderInfo.type,
          task_name: this.publishOrderInfo.name,
          description: this.publishOrderInfo.info,
          cur_people: this.publishOrderInfo.currentSummoningCount,
          max_people: this.publishOrderInfo.maximumSummoningCount,
          start_time: new Date().toLocaleDateString(),
          end_time: this.publishOrderInfo.date,
          task_status: this.publishOrderInfo.status,
          photos: this.publishOrderInfo.photos,
        })
        .then((res) => {
          if (res.status === 200) {
            alert("发布成功");
            console.log(res);
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  watch: {
    uploadPhotos() {
      if (this.uploadPhotos.length === 0) {
        while (this.imgs.length !== 0) {
          this.imgs.pop();
        }
      }
    },
  },
};
</script>

<style lang="css" scoped>
</style>
