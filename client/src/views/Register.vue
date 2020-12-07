<template>
  <!-- Fork of/Credit to:  https://github.com/aofdev/vue-firebase-auth-vuex/blob/master/src/components/User/Signin.vue -->
  <v-container fill-height>
    <v-layout row wrap justify-center>
      <v-flex xs11 sm10 md8>
        <v-card class="mx-auto elevation-8">
          <!-- ERROR MESSAGE -->
          <v-layout v-if="error" row>
            <v-flex xs12 sm8 offset-sm2>
              <app-alert :text="error.message" @dismissed="onDismissed" />
            </v-flex>
          </v-layout>

          <!-- Login/Signin -->
          <v-layout row align-center justify-center class="py-5">
            <v-form @submit.prevent="postLogin">
              <v-flex xs12 md10>
                <h1 class="text-center mb-5">欢迎来到'召集令'</h1>
                <v-text-field
                  name="ID"
                  label="ID"
                  type="input"
                  required
                  v-model="userInfo.account"
                />
              </v-flex>

              <v-flex xs12 md10>
                <v-text-field
                  name="password"
                  label="密码"
                  type="password"
                  required
                  v-model="userInfo.password"
                />
              </v-flex>

              <v-flex xs12 md10>
                <v-text-field
                  name="nick_name"
                  label="昵称"
                  type="input"
                  required
                  v-model="userInfo.nick_name"
                />
              </v-flex>

              <v-flex xs12 md10>
                <v-text-field
                  name="telephone"
                  label="电话"
                  type="number"
                  required
                  v-model="userInfo.telephone"
                ></v-text-field>
              </v-flex>

              <v-flex xs12 md10>
                <v-textarea
                  name="introduction"
                  label="用户简介"
                  type="input"
                  required
                  outlined
                  v-model="userInfo.introduction"
                ></v-textarea>
              </v-flex>

              <v-flex xs12 md10>
                <v-text-field
                  name="city"
                  label="城市"
                  type="input"
                  required
                  v-model="userInfo.city"
                ></v-text-field>
              </v-flex>

              <v-flex xs12 md10>
                <v-checkbox
                  label="二代身份证"
                  :value="!userInfo.cert_type"
                  @change="userInfo.cert_type = 0"
                ></v-checkbox>
                <v-checkbox
                  label="护照"
                  :value="userInfo.cert_type"
                  @change="userInfo.cert_type = 1"
                ></v-checkbox>
                <v-text-field
                  name="cert_number"
                  label="证件号码"
                  type="input"
                  required
                  v-model="userInfo.cert_number"
                ></v-text-field>
              </v-flex>

              <v-flex xs12 md10 class="py-3">
                <div class="text-center">
                  <v-btn
                    type="submit"
                    dark
                    ref="submitBtn"
                    @mouseover="mouseOver"
                    @mouseleave="mouseLeave"
                    :style="submitStyle"
                  >
                    注册
                    <v-icon right> mdi-key-variant </v-icon>
                    <span slot="loader" class="custom-loader">
                      <v-icon>cached</v-icon>
                    </span>
                  </v-btn>
                </div>

                <!-- <div class="text-center mt-3">
                  <v-btn color="grey" to="Home">
                    返回主页
                    <v-icon right> mdi-logout-variant </v-icon>
                    <span slot="loader" class="custom-loader">
                      <v-icon>cached</v-icon>
                    </span>
                  </v-btn>
                </div> -->
              </v-flex>
            </v-form>
          </v-layout>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn outlined :to="{ name: 'Login' }">返回登录</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: "Login",
  data: () => ({
    userInfo: {
      account: undefined,
      password: undefined,
      nick_name: undefined,
      telephone: undefined,
      introduction: undefined,
      cert_type: undefined,
      cert_number: undefined,
      city: undefined,
    },
    error: false,
    submitStyle: "",
  }),
  methods: {
    postLogin: function () {
      this.axios
        .post("api/user/register", this.userInfo)
        .then((res) => {
          const RecvData = res.data;
          if (res.status === 200) {
            alert("注册成功");
            this.$router.push({
              name: "Login",
            });
          } else {
            alert("注册失败");
            // if (RecvData.username !== localStorage.getItem("username")) {
            //   alert("用户名未注册");
            // } else if (RecvData.password !== localStorage.getItem("password")) {
            //   alert("注册失败");
            // }
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    mouseOver: function () {
      this.$refs.submitBtn.color = "majorColor";
      this.$refs.submitBtn.outlined = false;
    },
    mouseLeave: function () {
      this.$refs.submitBtn.color = "black";
      this.$refs.submitBtn.outlined = true;
    },
  },
};
</script>

<style lang="sass" scoped>
.block
  margin-top: 4rem

.login :hover
  color: yellow
</style>
