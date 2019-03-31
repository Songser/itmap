<template>
  <el-menu mode="horizontal" class="navbar">
    <el-row >
      <el-col :span="4">
        <div class="logo-container">
        <img class="user-avatar" :src="logo" :onerror="defaultImage">
        </div>
      </el-col>
   <el-col :span="14">
    <div class="button-container">
      <el-row>
          <el-col :span="6" class="text-center">
            <a class="pan-btn light-blue-btn" @click="showResource">文章</a>
          </el-col>
          <el-col :span="6" class="text-center">
            <a class="pan-btn pink-btn" @click="showArtical">问答</a>
          </el-col>
          <el-col :span="6" class="text-center">
            <a class="pan-btn green-btn" @click="showQuestion">用户</a>
          </el-col>
          <el-col :span="6" class="text-center">
            <a class="pan-btn tiffany-btn" @click="showUser">书籍</a>
          </el-col>
      </el-row>
    </div>
   </el-col>
   <el-col :span="6">
    <div class="right-menu">
    <el-dropdown class="avatar-container right-menu-item" trigger="click">
        <div class="avatar-wrapper">
          <img class="user-avatar" :src="avatar" :onerror="defaultImage">
        </div>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item >
            <span v-if="!user_id" @click="login" style="display:block;">立即登陆</span>
            <span v-if="user_id" style="display:block;">{{name}}</span>
          </el-dropdown-item>
          <el-dropdown-item divided>
            <span @click="showUserSetting" style="display:block;">
              个人设置
            </span>
          </el-dropdown-item>
          <el-dropdown-item divided>
            <span @click="logout" style="display:block;">退出登陆</span>
          </el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
   </el-col>
  </el-row>
  <el-dialog
      title="个人设置"
      :visible.sync="showUserDialog"
      width="60%" :append-to-body=true>
      <user />
    </el-dialog>
  </el-menu>
</template>

<script>
import { mapState } from 'vuex'
import logo from '@/assets/it.jpg'
import PanThumb from '@/components/PanThumb'
import User from '@/components/User'

export default {
  name: 'nav-bar',
  components: {
    PanThumb,
    User
  },
  data () {
    return {
      addNodeDialog: false,
      showResourceDialog: false,
      showArticalDialog: false,
      showQuestionDialog: false,
      showUserDialog: false,
      logo: logo,
      defaultImage: 'this.src="' + require('../assets/it.jpg') + '"'
    }
  },
  computed: {
    ...mapState({
      user_id: state => state.user.id,
      name: state => state.user.name,
      avatar: state => state.user.avatar
    })
  },
  created () {

  },
  methods: {
    logout () {

    },
    login () {
      this.$router.push('login')
    },
    addNode () {
      this.addNodeDialog = true
    },
    addNodeClose () {
      this.addNodeDialog = false
    },
    showUserSetting () {
      this.showUserDialog = true
    },
    showResource () {

    },
    showArtical () {

    },
    showQuestion () {

    },
    showUser () {

    }

  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.navbar {
  width: 100%;
  background-color: #F0F8FF;
  text-align: left;
  height: 100%;
  .logo-container {
    float: left;
    padding-left: 10px;
    padding-top: 10px;
    img {
      height: 40px;
      width: 40px;
    }
  }
  .button-container {
    width: 90%;
    .el-row {
      padding-top: 10px;
      background-color: #F0F8FF;
      box-shadow: 0;
      .pan-btn {
        font-size: 16px;
        margin-right: 10px;
        padding: 8px 10px;
        width: 100%;
        text-align: center;
      }
    }
  }
  .right-menu {
    float: right;
    height: 100%;
    &:focus{
     outline: none;
    }
    .right-menu-item {
      display: inline-block;

    }
    .theme-switch {
      vertical-align: 15px;
    }
    .avatar-container {
      height: 50px;
      margin-right: 10px;
      .avatar-wrapper {
        cursor: pointer;
        padding-top: 10px;
        position: relative;
        .user-avatar {
          width: 40px;
          height: 40px;
          border-radius: 50px;
          background-color: aqua;
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
