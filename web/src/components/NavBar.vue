<template>
  <el-menu class="navbar" mode="horizontal">

    <div class=logo-container>
      <img class="user-avatar" :src="avatar">
    </div>
    <div class="button-container">
      <el-row>
      <el-card class="box-card">
        <div>
          <el-col :span="4" class="text-center">
            <router-link class="pan-btn blue-btn" to="/components/index">Components</router-link>
          </el-col>
          <el-col :span="4" class="text-center">
            <router-link class="pan-btn light-blue-btn" to="/charts/index">Charts</router-link>
          </el-col>
          <el-col :span="4" class="text-center">
            <router-link class="pan-btn pink-btn" to="/excel/download">Excel</router-link>
          </el-col>
          <el-col :span="4" class="text-center">
            <router-link class="pan-btn green-btn" to="/example/table/complex-table">Table</router-link>
          </el-col>
          <el-col :span="4" class="text-center">
            <router-link class="pan-btn tiffany-btn" to="/form/edit-form">Form</router-link>
          </el-col>
          <el-col :span="4" class="text-center">
            <router-link class="pan-btn yellow-btn" to="/theme/index">Theme</router-link>
          </el-col>
        </div>
      </el-card>
      </el-row>
    </div>
    <div class="right-menu">
    <el-dropdown class="avatar-container right-menu-item" trigger="click">
        <div class="avatar-wrapper">
          <img class="user-avatar" :src="avatar">
           <!-- <svg-icon icon-class="user" /> -->
          <i class="el-icon-caret-bottom"></i>
        </div>
        <el-dropdown-menu slot="dropdown">
          <router-link to="/">
            <el-dropdown-item>
              首页设置
            </el-dropdown-item>
          </router-link>
          <a target='_blank' href="https://github.com/PanJiaChen/vue-element-admin/">
            <el-dropdown-item>
              个人图谱
            </el-dropdown-item>
          </a>
          <el-dropdown-item divided>
            <span @click="logout" style="display:block;">退出登陆</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </el-menu>
</template>
<style rel="stylesheet/scss" lang="scss" scoped>

.navbar {
  width: 100%;
  height: 100%;
  background-color: #F0F8FF;
  border-bottom-width: 0px;
  text-align: left;
  .logo-container {
    float: left;
    margin-top: 10px;
    img {
      height: 40px;
      width: 40px;
    }
  }
  .button-container {
    float: left;
    margin-left: 60px;
    margin-top: 20px;
  }
  .right-menu {
    float: right;
    height: 100%;
    &:focus{
     outline: none;
    }
    .right-menu-item {
      display: inline-block;
      margin: 0 8px;
    }
    .theme-switch {
      vertical-align: 15px;
    }
    .avatar-container {
      height: 50px;
      margin-right: 30px;
      .avatar-wrapper {
        cursor: pointer;
        margin-top: 5px;
        position: relative;
        .user-avatar {
          width: 40px;
          height: 40px;
          border-radius: 10px;
        }
        .el-icon-caret-bottom {
          position: absolute;
          right: -20px;
          top: 25px;
          font-size: 12px;
        }
      }
    }
  }
  
}
</style>

<script>
import logo from '@/assets/logo.png'
import PanThumb from '@/components/PanThumb'
export default {
  name: 'nav-bar',
  components: {
    PanThumb
  },
  data () {
    return {
      avatar: logo
    }
  },
  computed: {
  },
  methods: {
    logout () {

    }
  }
}
</script>
