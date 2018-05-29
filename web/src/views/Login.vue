<template>
  <v-container>
    <v-layout row justify-center mt-3>
      <v-flex xs12 sm6 md6>
        <v-card dark color="indigo" mt-3>
          <!-- <v-card-title class="white--text">登陆</v-card-title> -->
          <v-card-text>
            <v-form v-model="valid">
              <v-text-field v-model="loginForm.name" label="姓名" required></v-text-field>
              <v-text-field v-model="loginForm.password" label="密码" required></v-text-field>
              <v-btn :disabled="!valid" @click="submit">
                登录
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
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
      loginForm: {
        username: "",
        password: ""
      },
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
      login(this.loginForm.username, this.loginForm.password).then(response => {
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
    },
    created() {},
    destroyed() {}
  }
};
</script>
