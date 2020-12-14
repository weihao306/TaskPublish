<template>
  <!-- Fork of/Credit to:  https://github.com/aofdev/vue-firebase-auth-vuex/blob/master/src/components/User/Signin.vue -->
  <v-container align-center justify-center fill-height>
    <v-layout row wrap align-center justify-center>
      <v-flex xs10 sm8 mb6 lg6>
        <v-card class="elevation-8">
          <!-- ERROR MESSAGE -->
          <v-layout v-if="error" row>
            <v-flex xs12 sm6 offset-sm3>
              <app-alert :text="error.message" @dismissed="onDismissed" />
            </v-flex>
          </v-layout>

          <!-- Login/Signin -->
          <v-layout row align-center justify-center class="py-5">
            <v-form @submit.prevent="postLogin">
              <v-flex xs12>
                <h1 class="text-center mb-5">'召集令'管理</h1>
                <v-text-field
                  id="ID"
                  v-model="Admin.account"
                  name="ID"
                  label="管理员ID"
                  type="input"
                  required
                />
              </v-flex>

              <v-flex xs12>
                <v-text-field
                  id="password"
                  v-model="Admin.password"
                  name="password"
                  label="密码"
                  type="password"
                  required
                />
              </v-flex>

              <v-flex xs12 class="py-3">
                <div class="text-center">
                  <v-btn
                    type="submit"
                    dark
                    ref="submitBtn"
                    :color="loginBtn.color"
                    :outlined="loginBtn.outlined"
                    @mouseover="mouseOver"
                    @mouseleave="mouseLeave"
                    :style="submitStyle"
                  >
                    登录
                    <v-icon right> mdi-lock-open </v-icon>
                    <span slot="loader" class="custom-loader">
                      <v-icon>cached</v-icon>
                    </span>
                  </v-btn>
                </div>

                <div class="text-center mt-3">
                  <v-btn color="grey" :to="{ name: 'Home' }">
                    返回主页
                    <v-icon right> mdi-logout-variant </v-icon>
                    <span slot="loader" class="custom-loader">
                      <v-icon>cached</v-icon>
                    </span>
                  </v-btn>
                </div>
              </v-flex>
            </v-form>
          </v-layout>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
// import qs from "qs";
export default {
  name: "Login",
  // props:["title","account","password","LoginFunc"],
  data: () => ({
    Admin: {
      account: undefined,
      password: undefined,
    },
    error: false,
    submitStyle: "",
    loginBtn: {
      color: "black",
      outlined: true,
    },
  }),
  methods: {
    postLogin: function () {
      this.axios
        .post("api/user/login", this.Admin)
        .then((res) => {
          // respone the Admin
          const Admin = res.data;
          console.log(Admin);
          if (res.status === 200) {
            if (res.data.status === 300001) {
              alert("用户名未注册");
            } else if (res.data.status === 300002) {
              alert("密码错误");
            } else {
              alert("登录成功");
              this.$store.dispatch("loginAction", Admin).then(() => {
                this.$router.push({
                  name: "Admin",
                  params: { uid: Admin.uid },
                });
              });
            }
          }
        })
        .catch((err) => {
          console.error(err);
        });
    },
    mouseOver: function () {
      this.loginBtn.color = "majorColor";
      this.loginBtn.outlined = false;
    },
    mouseLeave: function () {
      this.loginBtn.color = "black";
      this.loginBtn.outlined = true;
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
