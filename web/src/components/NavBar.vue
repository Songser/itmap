<template>
  <div>
  <el-menu class="navbar" mode="horizontal">
    <div class=logo-container>
      <img class="user-avatar" :src="avatar">
    </div>
    <div class="button-container">
      <el-row>
          <el-col :span="4" class="text-center">
            <a class="pan-btn blue-btn" @click="addNode">添加</a>
          </el-col>
          <el-col :span="4" class="text-center">
            <a class="pan-btn light-blue-btn" @click="showResource">资源</a>
          </el-col>
          <el-col :span="4" class="text-center">
            <a class="pan-btn pink-btn" @click="showArtical">文章</a>
          </el-col>
          <el-col :span="4" class="text-center">
            <a class="pan-btn green-btn" @click="showQuestion">问答</a>
          </el-col>
          <el-col :span="4" class="text-center">
            <a class="pan-btn tiffany-btn" @click="showUser">用户</a>
          </el-col>
      </el-row>
    </div>
    <div class="right-menu">
    <el-dropdown class="avatar-container right-menu-item" trigger="click">
        <div class="avatar-wrapper">
          <img class="user-avatar" :src="avatar">
        </div>

        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item >
            <span v-if="!user_id" @click="login" style="display:block;">立即登陆</span>
            <span v-if="user_id" style="display:block;">{{name}}</span>
          </el-dropdown-item>
          <router-link to="/">
            <el-dropdown-item divided>
              个人设置
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
  <div class="components-container">
    <el-dialog
    :visible.sync="addNodeDialog"
    width="500px"
    :append-to-body=true>
    <add-node @closeAddNodeDialog="addNodeClose"/>
  </el-dialog>
</div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import logo from '@/assets/logo.png'
import PanThumb from '@/components/PanThumb'
import AddNode from '@/components/AddNode'

export default {
  name: 'nav-bar',
  components: {
    PanThumb,
    AddNode
  },
  data () {
    return {
      avatar: logo,
      addNodeDialog: false,
      showResourceDialog: false,
      showArticalDialog: false,
      showQuestionDialog: false,
      showUserDialog: false
    }
  },
  computed: {
    ...mapState({
      user_id: state => state.user.id,
      name: state => state.user.name
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
    showResource () {

    },
    showArtical () {

    },
    showQuestion () {

    },
    showUser () {

    },
    addNodeClose () {
      this.addNodeDialog = false
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.el-dialog {
  z-index: 200 !important;
}
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
    margin-left: 5%;
    width: 70%;
    .el-row {
      padding-top: 10px;
      height: 100%;
      background-color: #F0F8FF;
      box-shadow: 0;
      width: 100%;
      .pan-btn {
        font-size: 16px;
        margin-right: 10px;
        padding: 7px 10px;
        width: 100%;
        height: 100%;
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
      margin: 0 8px;
    }
    .theme-switch {
      vertical-align: 15px;
    }
    .avatar-container {
      height: 50px;
      margin-right: 10px;
      .avatar-wrapper {
        cursor: pointer;
        margin-top: 10px;
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
