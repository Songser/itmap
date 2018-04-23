<template>
  <div class="social-signup-container">
    <div class="sign-btn" @click="wechatHandleClick('wechat')">
      <span class="wx-svg-container"><svg-icon icon-class="wechat" class="icon"></svg-icon></span>
    </div>
    <div class="sign-btn" @click="githubHandleClick('tencent')">
      <span class="github-svg-container"><svg-icon icon-class="github" class="icon"></svg-icon></span>
    </div>
    <div class="sign-btn" @click="weiboHandleClick('tencent')">
      <span class="weibo-svg-container"><svg-icon icon-class="weibo" class="icon"></svg-icon></span>
    </div>
  </div>
</template>

<script>
import openWindow from '@/utils/openWindow'
export default {
  name: 'social-signin',
  methods: {
    wechatHandleClick (thirdpart) {
      this.$store.commit('SET_AUTH_TYPE', thirdpart)
      const appid = 'xxxxx'
      const redirectUri = encodeURIComponent('xxx/redirect?redirect=' + window.location.origin + '/authredirect')
      const url = 'https://open.weixin.qq.com/connect/qrconnect?appid=' + appid + '&redirect_uri=' + redirectUri + '&response_type=code&scope=snsapi_login#wechat_redirect'
      openWindow(url, thirdpart, 540, 540)
    },
    githubHandleClick (thirdpart) {
      this.$store.commit('SET_AUTH_TYPE', thirdpart)
      const clientId = 'xxxxx'
      const redirectUri = encodeURIComponent('xxx/redirect?redirect=' + window.location.origin + '/authredirect')
      const url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=' + clientId + '&redirect_uri=' + redirectUri
      openWindow(url, thirdpart, 540, 540)
    },
    weiboHandleClick (thirdpart) {
      this.$store.commit('SET_AUTH_TYPE', thirdpart)
      const clientId = 'xxxxx'
      const redirectUri = encodeURIComponent('xxx/redirect?redirect=' + window.location.origin + '/authredirect')
      const url = 'https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=' + clientId + '&redirect_uri=' + redirectUri
      openWindow(url, thirdpart, 540, 540)
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .social-signup-container {
    margin-left: 0px;
    .sign-btn {
      display: inline-block;
      cursor: pointer;
    }
    .icon {
      color: #fff;
      font-size: 30px;
      margin-top: 6px;
    }
    .wx-svg-container,
    .github-svg-container,
    .weibo-svg-container {
      display: inline-block;
      width: 40px;
      height: 40px;
      line-height: 40px;
      padding-top: 0px;
      border-radius: 4px;
      margin-bottom: 10px;
      margin: 0px 20px;

    }
    .wx-svg-container {
      background-color: #8dc349;
    }
    .github-svg-container {
      background-color: #ffffff;
    }
    .weibo-svg-container {
      background-color: #d81e06
    }
  }
</style>
