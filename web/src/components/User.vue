<template>
    <div>
    <nav-bar/>
  <el-card class="box-card">
  <el-form ref="form" :model="form" label-width="80px">
    <el-form-item label="姓名">
        <el-input v-model="form.name"></el-input>
    </el-form-item>
    <el-form-item label="性别">
        <el-radio v-model="form.gender" label="1">男</el-radio>
        <el-radio v-model="form.gender" label="2">女</el-radio>
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
  </el-card>
    </div>
</template>
<script>
import NavBar from '@/components/NavBar'

export default {
  name: 'user',
  components: {
    NavBar
  },
  data () {
    return {
      form: {
        name: '',
        email: '',
        sex: '',
        birthday: '',
        mobile: '',
        wechat: ''
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.el-form {
    text-align: left;
}
</style>
