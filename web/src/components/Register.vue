<template>
  <div class="login-container">
    <el-form class="login-form" autoComplete="on" :model="loginForm" :rules="loginRules" ref="loginForm" label-position="left">
      <div class="title-container">
        <h3 class="title">用户注册</h3>
      </div>
      <el-form-item prop="username">
        <span class="svg-container svg-container_login">
          <svg-icon icon-class="user" />
        </span>
        <el-input name="username" type="text" v-model="loginForm.username" autoComplete="on" placeholder="用户名" />
      </el-form-item>

      <el-form-item prop="email">
        <span class="svg-container svg-container_login">
          <svg-icon icon-class="email" />
        </span>
        <el-input name="email" type="text" v-model="loginForm.email" autoComplete="on" placeholder="邮箱" />
      </el-form-item>

      <el-form-item prop="password">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input name="password" :type="passwordType" v-model="loginForm.password" autoComplete="on" placeholder="输入秘密" />
        <span class="show-pwd" @click="showPwd">
          <svg-icon icon-class="eye" />
        </span>
      </el-form-item>
      <el-form-item prop="retrypassword">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input name="retrypassword" :type="passwordType" v-model="loginForm.retrypassword" autoComplete="on" placeholder="重新输入秘密" />
        <span class="show-pwd" @click="showPwd">
          <svg-icon icon-class="eye" />
        </span>
      </el-form-item>
      <!-- <el-col :span="17">
      <el-form-item prop="verificationCode">
        <span class="svg-container">
          <svg-icon icon-class="code" />
        </span>
        <el-input type="number" name="verificationCode" v-model.number="loginForm.verificationCode" autoComplete="on" placeholder="验证码" />
      </el-form-item>
      </el-col>
      <el-col :span="7">
         <el-button type="success" class="send-code" @click="sendCode" :disabled="sendCodeDisabled">
           <span v-show="!sendCodeDisabled">发送验证码</span>
            <countTo v-show="sendCodeDisabled" ref="timer" :useEasing="false" :startVal='startVal' :autoplay='false' :endVal='_endVal' :duration='duration' v-on:callback="timerCallback"  :suffix="s"></countTo>
         </el-button>
      </el-col> -->
      <el-button type="primary" style="width:100%;margin-bottom:30px;" :loading="loading" @click.native.prevent="handleRegister('loginForm')">注册</el-button>
      </el-form>
  </div>
</template>

<script>
import { isvalidateEmail } from '@/utils/validate'
import { register } from '@/api/user'

export default {
  name: 'register',
  data () {
    const validateUsername = (rule, value, callback) => {
      if (value.length < 4) {
        callback(new Error('用户名不能小于4位'))
      } else {
        callback()
      }
    }
    var validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('秘密不能小于6位'))
      } else {
        callback()
      }
    }
    var validateEmail = (rule, value, callback) => {
      if (!isvalidateEmail(value)) {
        callback(new Error('请输入正确的邮箱'))
      } else {
        callback()
      }
    }
    var validateRetryPassword = (rule, value, callback) => {
      if (value !== this.loginForm.password) {
        callback(new Error('两次输入秘密不一致'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: '',
        email: '',
        password: '',
        retrypassword: ''
        // verificationCode: ''
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        email: [{ required: true, trigger: 'blur', validator: validateEmail }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }],
        retrypassword: [{ required: true, trigger: 'blur', validator: validateRetryPassword }]
        // verificationCode: [
        //   { required: true, message: '验证码不能为空' },
        //   { type: 'number', message: '验证码必须为数字值' },
        //   { min: 6, max: 6, message: '长度为6个字符', trigger: 'blur' }]
      },
      passwordType: 'password',
      loading: false
      // showDialog: false,
      // endVal: 0,
      // startVal: 60,
      // sendCodeDisabled: false,
      // duration: 60 * 1000,
      // s: '秒后重试'
    }
  },
  computed: {
    _endVal () {
      return this.endVal
    }
  },
  methods: {
    // timerCallback () {
    //   this.sendCodeDisabled = false
    // },
    showPwd () {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
    },
    handleRegister (formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.loading = true
          register(this.loginForm.username, this.loginForm.password, this.loginForm.email)
            .then(response => {
              this.loading = false
              this.$router.push('login')
            })
        } else {
          return false
        }
      })
    },
    created () {},
    destroyed () {}
  }

}
</script>

<style rel="stylesheet/scss" lang="scss">
$bg:#2d3a4b;
$light_gray:#eee;
/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;
    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: #fff !important;
      }
    }
  }
  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
$bg:#2d3a4d;
$dark_gray:#889aa4;
$light_gray:#eee;
.login-container {
  position: fixed;
  height: 100%;
  width: 100%;
  background-color: $bg;
  .login-form {
    position: absolute;
    left: 0;
    right: 0;
    width: 520px;
    padding: 35px 35px 15px 35px;
    margin: 30px auto;
    text-align: left;
  }
  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;
    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }
  .svg-container {
    padding: 5px 5px 5px 5px;
    color: $dark_gray;
    vertical-align: middle;
    width: 50px;
    display: inline-block;
    border-right-style: dotted;
    border-right-width: 1px;
    text-align: center;
    &_login {
      font-size: 20px;
    };
    .svg-icon {
      width: 15px;
      height: 15px;
    }
  }
  .title-container {
    position: relative;
    .title {
      font-size: 26px;
      font-weight: 400;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }
  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
  .thirdparty-button {
    position: absolute;
    right: 35px;
    bottom: 28px;
  }

  .send-code {
    margin-top: 8px;
    margin-left: 10px;
  }
}
</style>
