<template>
  <v-app id="inspire">
    <v-content class='content'>
      <v-container fluid fill-height grid-list-md>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>用户注册</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form ref="loginForm">
                  <v-text-field v-model="username" :rules="loginRules.username" prepend-icon="person" name="username" label="姓名" type="text"></v-text-field>
                  <v-text-field v-model="email" :rules="loginRules.email" prepend-icon="email" name="email" label="邮箱" type="text"></v-text-field>
                  <v-text-field v-model="password" prepend-icon="lock" name="password" label="密码" type="password"></v-text-field>
                  <v-text-field v-model="password" prepend-icon="lock" name="password" label="确认密码" type="password"></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions px-5 >
                <v-btn block dark :loading="loading" color="primary" @click="handleLogin">登录</v-btn>
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
    return {
      username: "",
      email: "",
      password: "",
      retryPwd: "",
      loginRules: {
        username: [
          v => !!v || '不能为空',
          v => v.length >= 4 || '不能小于6个字节'
        ],
        password: [
          v => !!v || '不能为空',
        ],
        email: [
          v => !!v || '不能为空',
          v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || '邮箱格式无效'
        ]
      },
      loading: false,
    };
  },
  methods: {
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
      }, response => {
        this.loading = false;
      });
    }
  }
};
</script>

<style lang='scss' scoped>
@import '../styles/mixin.scss';
.card__actions .btn {
  margin: 0px 10px 20px 10px;
}
.content {
 @include realbg()
}
</style>
