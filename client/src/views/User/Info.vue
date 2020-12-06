<template>
  <v-container grid-list-xs fill-height>
    <v-layout row wrap justify-center class="mt-5">
      <v-flex xs11 sm10 md8>
        <v-card>
          <v-layout row justify-center align-content-center wrap>
            <v-flex xs11 sm9 md7>
              <h1 class="text-center mb-5">个人信息</h1>
            </v-flex>
            <v-flex xs11 sm9 md7>
              <v-text-field
                id="ID"
                v-model="userInfo.account"
                name="ID"
                label="ID"
                type="input"
                required
                readonly
                justify-center
              />
            </v-flex>
            <v-flex xs11 sm9 md7>
              <v-text-field
                v-model="userInfo.nick_name"
                name="nick_name"
                label="昵称"
                type="nick_name"
                required
                readonly
              />
            </v-flex>

            <v-flex xs11 sm9 md7>
              <v-text-field
                v-model="userInfo.telephone"
                name="telephone"
                label="电话"
                type="number"
                required
                readonly
              ></v-text-field>
            </v-flex>

            <v-flex xs11 sm9 md7>
              <v-textarea
                v-model="userInfo.introduction"
                name="introduction"
                label="用户简介"
                type="input"
                required
                outlined
                readonly
              ></v-textarea>
            </v-flex>

            <v-flex xs11 sm9 md7>
              <v-checkbox
                v-model="userInfo.cert_type"
                label="二代身份证"
                readonly
              ></v-checkbox>

              <v-checkbox
                :value="!userInfo.cert_type"
                label="护照"
                v-show="!userInfo.cert_type"
                readonly
              ></v-checkbox>

              <v-text-field
                :value="userInfo.cert_number"
                v-show="userInfo.cert_type"
                name="cert_number"
                label="证件号码"
                type="input"
                required
                readonly
              ></v-text-field>
            </v-flex>

            <v-flex xs11 sm9 md7 class="py-3">
              <v-layout row justify-center>
                <v-dialog v-model="modifyInfoSwitcher" max-width="40rem">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      v-bind="attrs"
                      v-on="on"
                      dark
                      @click.native.stop="
                        modifyInfoSwitcher = true;
                        modifyInfoInit(userInfo);
                      "
                    >
                      修改信息
                      <v-icon right> mdi-wrench-outline </v-icon>
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title class="headline grey lighten-2">修改信息</v-card-title>
                    <v-divider></v-divider>
                    <v-card-text>
                      <v-layout row justify-center align-center wrap>
                        <v-flex xs11 sm9 md7>
                          <v-text-field
                            v-model="modifyInfo.password"
                            name="password"
                            label="密码"
                            type="password"
                            required
                          />
                        </v-flex>
                        <v-flex xs11 sm9 md7>
                          <v-text-field
                            v-model="modifyInfo.repeatPassword"
                            name="password"
                            label="重复密码"
                            type="input"
                            required
                            :rules="[
                              () =>
                                modifyInfo.password ===
                                  modifyInfo.repeatPassword ||
                                '请输入相同的密码',
                            ]"
                          />
                        </v-flex>

                        <v-flex xs11 sm9 md7>
                          <v-text-field
                            v-model="modifyInfo.telephone"
                            name="telephone"
                            label="电话"
                            type="number"
                            required
                          ></v-text-field>
                        </v-flex>

                        <v-flex xs11 sm9 md7>
                          <v-textarea
                            v-model="modifyInfo.introduction"
                            name="introduction"
                            label="用户简介"
                            type="input"
                            required
                            outlined
                          ></v-textarea>
                        </v-flex>
                      </v-layout>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn
                        color="success"
                        @click.native="modifyInfoSwitcher=false;confirmModifyInfo();"
                        >确认修改</v-btn
                      >
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-layout>
            </v-flex>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import User from "@/classes/User.js";
export default {
  // computed(){
  //   uuid(){
  //     return this.$store.state.userInfo.uuid;
  //   };
  // },
  mounted() {
    // console.log(this.$props.uuid);
    console.log(this.$store.state.userInfo.nick_name);
    console.log(this.$store.state.userInfo.uuid);
    console.log(this.$props.uuid)
    this.getUserInfo();
  },
  props: {
    uuid: Number,
  },
  data() {
    return {
      modifyInfoSwitcher: false,
      // userInfo: {
      //   uuid:undefined,
      //   nick_name:undefined,
      //   account:undefined,
      //   password:undefined,
      //   introduction:undefined,
      //   cert_type:undefined,
      //   cert_number:undefined,
      // }, // User class
      userInfo:new User(),
      modifyInfo: {
        password: undefined,
        repeatPassword: undefined,
        telephone: undefined,
        introduction: undefined,
      },
    };
  },
  methods: {
    getUserInfo() {
      this.axios
        .get("api/user/info", {
          params: { uuid: this.$store.state.userInfo.uuid },
        })
        .then((res) => {
          const info = res.data;
          this.userInfo = new User(info);
        });
    },
    confirmModifyInfo() {
      if (this.modifyInfo.password == this.modifyInfo.repeatPassword) {
        this.axios
          .put("api/user/info", {
            params: {
              uuid: this.uuid,
              password: this.modifyInfo.password,
              telephone: this.modifyInfo.telephone,
              introduction: this.modifyInfo.introduction,
            },
          })
          .then((res) => {
            alert("修改信息成功");
            modifyInfoSwitcher = false;
            this.userInfo.updateInfo(this.modifyInfo);
          });
      } else {
        alert("密码必须一致");
      }
    },
    modifyInfoInit(userInfo) {
      // this.modifyInfo.nick_name = userInfo.nick_name;
      this.modifyInfo.password = userInfo.password;
      this.modifyInfo.repeatPassword = "";
      this.modifyInfo.telephone = userInfo.telephone;
      this.modifyInfo.introduction = userInfo.introduction;
    },
  },
};
</script>

<style>
</style>