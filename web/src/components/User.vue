<template>
  <el-form ref="form" :model="form" label-width="80px">
    <el-form-item>
        <div class="avatar">
        <pan-thumb class="panThumb"  :image="form.avatar"></pan-thumb>
        <el-button type="primary" size="small" icon="upload" @click="imagecropperShow=true">上传头像
        </el-button>
        <image-cropper :width="300" :height="300" :url="uploadUrl" @close='close' @crop-upload-success="cropSuccess" langType="en"
      :key="imagecropperKey" v-show="imagecropperShow"></image-cropper>
        </div>
    </el-form-item>
    <el-form-item label="姓名">
        <el-input v-model="form.name"></el-input>
    </el-form-item>
    <el-form-item label="性别">
        <el-radio v-model="form.gender" label="male">男</el-radio>
        <el-radio v-model="form.gender" label="female">女</el-radio>
    </el-form-item>
    <el-form-item label="出生日期">
        <el-date-picker
            v-model="form.birthday"
            type="date"
            placeholder="选择日期">
        </el-date-picker>
    </el-form-item>
    <el-form-item label="邮箱">
        <el-input v-model="form.email"></el-input>
    </el-form-item>
    <el-form-item label="手机号">
        <el-input v-model="form.mobile"></el-input>
    </el-form-item>
    <el-form-item label="微信">
        <el-input v-model="form.wechat"></el-input>
    </el-form-item>
  </el-form>
</template>
<script>
import { mapState } from 'vuex'
import {getUserApi} from '@/api/user'
import PanThumb from '@/components/PanThumb'
import ImageCropper from '@/components/ImageCropper'
export default {
  name: 'user',
  components: {
    PanThumb,
    ImageCropper
  },
  data () {
    return {
      form: {
        name: '',
        email: '',
        sex: '',
        birthday: '',
        mobile: '',
        wechat: '',
        avatar: 'https://wpimg.wallstcn.com/577965b9-bb9e-4e02-9f0c-095b41417191',
      },
      imagecropperKey: 0,
      imagecropperShow: false,
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
          this.form.name = data.name
          this.form.email = data.email
      })
  },
  methods: {
      close() {

      },
      cropSuccess () {

      }
  }
}
</script>
<style lang="scss" scoped>
.el-form {
    text-align: left;
}
.avatar {
    height: 70px!important;
    width: 100%;
    .el-button {
        margin-left: 120px;
    }
}
.panThumb {
    z-index: 100;
    height: 70px!important;
    width: 70px!important;
    position: absolute!important;
    top: -25px;
    left: 0px;
    border: 5px solid #ffffff;
    background-color: #fff;
    box-shadow: none!important;
    /deep/ .pan-info {
      box-shadow: none!important;
    }
  }
</style>
