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
        <v-text-field v-model="gender" label="性别"></v-text-field>
        <v-text-field v-model="birthday" label="出生日期"></v-text-field>
        <v-text-field v-model="email" label="邮箱"></v-text-field>
        <v-text-field v-model="mobile" label="手机号" ></v-text-field>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="onSubmit">更新</v-btn>
      <v-btn color="primary" @click="cancel">关闭</v-btn>
    </v-card-actions>
  </v-card>
</template>
<script>
import { mapState } from 'vuex'
import { getUserApi, updateUserApi } from '@/api/user'
import ImageCropper from '@/components/ImageCropper'

export default {
  name: 'user',
  components: {
    ImageCropper
  },
  data () {
    return {
      name: '',
      gender: '',
      birthday: '',
      email: '',
      mobile: '',
      avatar: '',
      mime: '',
      field: 'user_pic',
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
    getUserApi(this.userId).then(response => {
      console.log(response.data)
      let data = response.data
      this.name = data.name
      this.email = data.email
      this.avatar = BASE_URL + '/avatars/' + data.avatar
    })
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
      updateUserApi(this.userId, data).then(response => {

      })
    }
  }
}
</script>
