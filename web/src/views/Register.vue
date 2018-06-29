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
                  <v-text-field v-model="username"
                    :error-messages="nameErrors"
                    prepend-icon="person"
                    name="username"
                    label="姓名"
                    type="text"
                    @input="$v.username.$touch()"
                    @blur="$v.username.$touch()">
                  </v-text-field>
                  <v-text-field v-model="email"
                    :error-messages="emailErrors"
                    prepend-icon="email"
                    name="email"
                    label="邮箱"
                    type="text"
                    @input="$v.email.$touch()"
                    @blur="$v.email.$touch()">
                  </v-text-field>
                  <v-text-field v-model="password"
                    :error-messages="passwordErrors"
                    prepend-icon="lock"
                    name="password"
                    label="密码"
                    type="password"
                    @input="$v.password.$touch()"
                    @blur="$v.password.$touch()">
                  </v-text-field>
                  <v-text-field v-model="retryPwd"
                    :error-messages="retryPwdErrors"
                    prepend-icon="lock"
                    name="retryPwd"
                    label="确认密码"
                    type="password"
                    @input="$v.retryPwd.$touch()"
                    @blur="$v.retryPwd.$touch()">
                  </v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions px-5 >
                <v-btn block dark :loading="loading" color="primary" @click="handleRegister">注册</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
import { validationMixin } from 'vuelidate'
import { required, minLength, email, sameAs } from 'vuelidate/lib/validators'
import { setToken } from '@/utils/auth'
import { register } from '@/api/user'

export default {
  name: 'register',
  mixins: [validationMixin],
  validations: {
    username: { required, minLength: minLength(4) },
    email: { required, email },
    password: { required, minLength: minLength(6) },
    retryPwd: {
      required, sameAsPassword: sameAs('password')
    }
  },
  data () {
    return {
      username: '',
      email: '',
      password: '',
      retryPwd: '',
      loading: false
    }
  },
  computed: {
    nameErrors () {
      const errors = []
      if (!this.$v.username.$dirty) return errors
      !this.$v.username.minLength && errors.push('不少于5个字符')
      !this.$v.username.required && errors.push('不能为空')
      return errors
    },
    emailErrors () {
      const errors = []
      if (!this.$v.email.$dirty) return errors
      !this.$v.email.email && errors.push('邮箱格式错误')
      !this.$v.email.required && errors.push('不能为空')
      return errors
    },
    passwordErrors () {
      const errors = []
      if (!this.$v.password.$dirty) return errors
      !this.$v.password.required && errors.push('不能为空')
      return errors
    },
    retryPwdErrors () {
      const errors = []
      if (!this.$v.retryPwd.$dirty) return errors
      !this.$v.retryPwd.required && errors.push('不能为空')
      !this.$v.retryPwd.sameAsPassword && errors.push('两次输入密码不相同')
      return errors
    }
  },
  methods: {
    handleRegister (formName) {
      if (!this.$v.$invalid) {
        this.loading = true
        register(this.username, this.password, this.email)
          .then((response) => {
            this.loading = false
            this.$router.push('login')
          }, (response) => {
            this.loading = false
          })
      }
    }

  }
}
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
