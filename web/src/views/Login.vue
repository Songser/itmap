<template>
  <v-app id="inspire">
    <v-content>
      <v-container fluid fill-height grid-list-md>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>用户登录</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form ref="loginForm">
                  <v-text-field v-model="username" prepend-icon="person" name="username" label="姓名" type="text"></v-text-field>
                  <v-text-field v-model="password" prepend-icon="lock" name="password" label="密码" type="password"></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions px-5 >
                 <v-btn color="primary" @click="handleLogin">登录</v-btn>
                 <v-spacer></v-spacer>
                <v-btn fab small color="primary">
                  <v-icon >fab fa-github</v-icon>
                </v-btn>
                <v-btn fab small color="primary">
                  <v-icon >fab fa-weixin</v-icon>
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { isvalidUsername } from "@/utils/validate";
import SocialSign from "@/components/SocialSignin";
import { setToken } from "@/utils/auth";
import { login } from "@/api/user";

export default {
  components: { SocialSign },
  name: "Login",
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!isvalidUsername(value)) {
        callback(new Error("Please enter the correct user name"));
      } else {
        callback();
      }
    };
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error("The password can not be less than 6 digits"));
      } else {
        callback();
      }
    };
    return {
      username: "",
      password: "",
      loginRules: {
        username: [
          { required: true, trigger: "blur", validator: validateUsername }
        ],
        password: [
          { required: true, trigger: "blur", validator: validatePassword }
        ]
      },
      passwordType: "password",
      loading: false,
      showDialog: false
    };
  },
  methods: {
    forget() {
      this.$router.push("forget");
    },
    register() {
      this.$router.push("register");
    },
    showPwd() {
      if (this.passwordType === "password") {
        this.passwordType = "";
      } else {
        this.passwordType = "password";
      }
    },
    handleLogin() {
      this.loading = true;
      login(this.username, this.password).then(response => {
        let data = response.data;
        setToken(data.access_token);
        this.$store.commit("setUser", {
          name: data.name,
          id: data.user_id,
          email: data.email,
          active: data.active,
          token: data.access_token
        });
        this.$router.push("index");
        this.loading = false;
      });
    }
  }
};
</script>

<style scoped>
.card__actions .btn {
  margin: 0 20px;
}
</style>
