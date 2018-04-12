<template>
  <div>
   <div class="app-wrapper">
      <div class="main-container">
        <el-container>
          <el-header>
            <nav-bar/>
          </el-header>
          <el-container>
            <el-main>
              <app-main/>
            </el-main>
            <el-aside width="300px">
              <app-aside/>
            </el-aside>
          </el-container>
        </el-container>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar'
import AppMain from '../components/AppMain'
import AppAside from '../components/AppAside'

export default {
  name: 'layout',
  components: {
    NavBar,
    AppMain,
    AppAside
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
@import "src/styles/mixin.scss";
.app-wrapper {
  @include clearfix;
  position: relative;
  height: 100%;
  width: 100%;
}
.el-header {
  background-color: #B3C0D1;
  color: #333;
  line-height: 60px;
}
.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  height: 700px;
}
.el-aside {
  background-color: #E9FEFF;
  color: #333;

}
</style>
