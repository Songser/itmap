<template>
  <v-card>
    <v-card-title>
      <p class="title">用户设置</p>
    </v-card-title>
    <v-card-text>
      <v-form>
        <v-layout row>
          <v-flex xs2>
            头像
          </v-flex>
          <v-flex xs10>
            <v-avatar size="150" style="width:29px" color="grey lighten-4" @click="imagecropperShow=true">
              <img :src="avatar" alt="avatar" v-show="avatar" :onerror="defaultImage">
            </v-avatar>
            <image-cropper :width="200" :height="200" :field="field" @close='close' @cropSuccess="cropSuccess" langType="zh" v-show="imagecropperShow">
            </image-cropper>
          </v-flex>
        </v-layout>
        <v-text-field v-model="name" label="姓名" autofocus></v-text-field>
        <v-select
          v-model="gender"
          :items="genders"
          item-text="abbr"
          item-value="state"
          label="性别"
        ></v-select>
        <v-menu
        ref="menu"
        :close-on-content-click="false"
        v-model="menu"
        :nudge-right="40"
        :return-value.sync="birthday"
        lazy
        transition="scale-transition"
        offset-y
        full-width
        min-width="290px"
      >
        <v-text-field
          slot="activator"
          v-model="birthday"
          label="出生日期"
          readonly
        ></v-text-field>
        <v-date-picker v-model="birthday" no-title scrollable locale="zh-cn">
          <v-spacer></v-spacer>
          <v-btn flat color="primary" @click="menu = false">取消</v-btn>
          <v-btn flat color="primary" @click="$refs.menu.save(birthday)">确认</v-btn>
        </v-date-picker>
      </v-menu>
        <!-- <v-text-field v-model="birthday" label="出生日期"></v-text-field> -->
        <v-text-field v-model="email" label="邮箱"></v-text-field>
        <v-text-field v-model="phone" label="手机号" ></v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="onSubmit">更新</v-btn>
      <v-btn color="primary" @click="cancel">关闭</v-btn>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="logout">注销</v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import { mapState } from 'vuex'
import { removeToken } from '@/utils/auth'
import {
  getUserApi,
  updateUserApi,
  uploadUserPicApi } from '@/api/user'
import ImageCropper from '@/components/ImageCropper'
import data2blob from '@/utils/data2blob.js'

export default {
  name: 'user',
  components: {
    ImageCropper
  },
  data () {
    return {
      menu: false,
      name: '',
      gender: {state: 'male', abbr: '男'},
      birthday: '',
      email: '',
      phone: '',
      avatar: '',
      mime: '',
      genders: [{state: 'male', abbr: '男'}, {state: 'female', abbr: '女'}],
      field: 'avatar',
      imagecropperShow: false,
      defaultImage: 'this.src="' + require('../assets/logo.png') + '"'
    }
  },
  computed: {
    ...mapState({
      userId: state => state.user.id,
      uploadUrl: state => '/api/v1_0/users/' + state.user.id + '/avatar'
    })
  },
  created () {
    if (this.userId > 0){
      getUserApi(this.userId).then(response => {
        console.log(response.data)
        let data = response.data
        this.name = data.name
        this.email = data.email
        this.phone = data.phone
        this.gender = data.gender
        this.birthday = data.birthday
        this.avatar = process.env.BASE_API + '/avatars/' + data.avatar
      })
    }
  },
  methods: {
    close () {
      this.imagecropperShow = false
    },
    cropSuccess (createImgUrl, field, mime, ki) {
      this.avatar = createImgUrl
      this.mime = mime
    },
    cancel () {
      this.$emit('closeUserDialog')
    },
    onSubmit () {
      let data = {
        name: this.name,
        email: this.email,
        phone: this.phone,
        gender: this.gender,
        birthday: this.birthday
      }
      console.log(data)
      updateUserApi(this.userId, data).then(response => {
        console.log(response)
        this.$emit('closeUserDialog')
        this.handlerUpload()
      })
    },
    handlerUpload () {
      if (!this.avatar) {
        return
      }
      let index = this.avatar.indexOf('data:image')
      if (index !== 0) {
        return
      }
      let form = new FormData()
      form.append(this.field, data2blob(this.avatar, this.mime))
      uploadUserPicApi(form, this.userId)
    },
    logout () {
      removeToken()
      window.location.reload()
    }
  }
}
</script>
