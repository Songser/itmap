<template>
   <div class="app-wrapper">
        <!-- <el-container class="main-container">
        <el-container>
          <el-header>
            <nav-bar/>
          </el-header>
          <el-container>
           <el-aside class="left-aside">
              <app-side-bar />
            </el-aside>
            <el-main>
              <app-main/>
            </el-main>
            <el-aside  class="right-aside">
              <app-aside/>
            </el-aside>
          </el-container>
          </el-container>
        </el-container> -->
        <el-row>
          <el-col :span="24" class=""><nav-bar/></el-col>
        </el-row>
        <el-row class="main-container">
          <el-col :span="4" class="el-aside">
            <app-side-bar />
          </el-col>
          <el-col :span="14" style="height: 100%">
            <div class="el-main">
              <app-main />
            </div>
          </el-col>
          <el-col :span="6" class="el-aside">
            <app-aside/>
          </el-col>
        </el-row>
      </div>
</template>

<script>
import NavBar from '@/components/NavBar'
import AppMain from '@/components/AppMain'
import AppAside from '@/components/AppAside'
import AppSideBar from '@/components/AppSidebar'

export default {
  name: 'layout',
  components: {
    NavBar,
    AppSideBar,
    AppMain,
    AppAside
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
@import "src/styles/mixin.scss";
.app-wrapper {
  @include clearfix;
  height: 100%;
  width: 100%;
}
.main-container {
  position: fixed;
  height: 100%;
  width: 100%;
}
.el-header {
  background-color: #F0F8FF;
  width: 100%;
}
.el-main {
  background-color: #FFF;
  color: #333;
  text-align: center;
  width: 100%;
  height: 100%;
}
.el-aside {
  background-color: #E9FEFF;
  color: #333;
  height: 100%;
}
.left-aside {
  max-width: 200px;
}
.right-aside {
  max-width: 300px;
}
</style>
