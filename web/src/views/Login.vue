<template>
  <v-app id="inspire">
    <v-content class='content'>
      <v-container fluid fill-height grid-list-md>
        <v-layout align-center justify-center>
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>用户登录</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form ref="loginForm">
                  <v-text-field v-model="username" :rules="loginRules.username" prepend-icon="person" name="username" label="姓名" type="text"></v-text-field>
                  <v-text-field v-model="password" prepend-icon="lock" name="password" label="密码" type="password"></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions px-5 >
                <v-btn block dark :loading="loading" color="primary" @click="handleLogin">登录</v-btn>
              </v-card-actions>
              <v-card-actions px-5 >
                 <v-btn flat color="indigo" to='register'>立即注册</v-btn>
                 <v-btn flat color="indigo" to='forget'>忘记密码</v-btn>
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
import SocialSign from '@/components/SocialSignin'
import { setToken } from '@/utils/auth'
import { login } from '@/api/user'

export default {
  components: { SocialSign },
  name: 'Login',
  data () {
    return {
      username: '',
      password: '',
      loginRules: {
        username: [
          v => !!v || '不能为空',
          v => v.length >= 4 || '不能小于6个字节'
        ],
        password: [
          v => !!v || '不能为空'
        ]
      },
      loading: false
    }
  },
  methods: {
    handleLogin () {
      this.loading = true
      login(this.username, this.password).then(response => {
        let data = response.data
        console.log('######', data)
        setToken(data.access_token)

        this.$store.commit('setUser', data)
        this.$router.push('index')
        this.loading = false
      }, response => {
        this.loading = false
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import '../styles/mixin.scss';
.card__actions .btn {
  margin: 0px 10px 20px 10px;
}
.content {
  @include realbg()
}
</style>
