<template>
  <v-toolbar app color="blue">
    <v-toolbar-side-icon @click.stop="openLeftDrawer"></v-toolbar-side-icon>
    <v-toolbar-title>ITMAP</v-toolbar-title>
    <v-layout row align-center ml-5 mr-3 style="max-width: 200px">
      <v-text-field placeholder="Search..." single-line append-icon="search" color="white" hide-details></v-text-field>
    </v-layout>
    <v-chip color='green'>
      <v-avatar @click.stop="addNode">
        <v-icon medium>fas fa-plus-circle</v-icon>
      </v-avatar>
      <span @click.stop="showDetail">{{node}}</span>
    </v-chip>
    <v-spacer></v-spacer>
    <v-chip close @click="showUser" @input="logout">
      <v-avatar>
        <img :src="avatar" alt="trevor" :onerror="defaultImage">
      </v-avatar>
      <span v-if="name">{{name}}</span>
      <span v-else>登录</span>
    </v-chip>
    <v-btn icon @click="openRightDrawer">
      <v-icon>more_vert</v-icon>
    </v-btn>
    <v-dialog v-model="addNodeDialog" max-width="600px" lazy persistent>
      <add-node @closeAddNodeDialog="closeAddNodeDialog"/>
    </v-dialog>
    <v-dialog v-model="detailDialog" fullscreen hide-overlay scrollable transition="dialog-bottom-transition">
      <node-info @closeDetailDialog="closeDetailDialog"/>
    </v-dialog>
  </v-toolbar>
</template>
<script>
import { mapState } from 'vuex'
import AddNode from '@/views/AddNode'
import NodeInfo from '@/views/NodeInfo'
export default {
  name: 'app-header',
  components: {
    AddNode,
    NodeInfo
  },
  data () {
    return {
      addNodeDialog: false,
      detailDialog: false,
      defaultImage: 'this.src="' + require('../assets/logo.png') + '"'
    }
  },
  computed: {
    ...mapState({
      user_id: state => state.user.id,
      name: state => state.user.name,
      avatar: state => state.user.avatar,
      node: state => state.node.name
    })
  },
  methods: {
    openLeftDrawer () {
      this.$emit('openLeftDrawer')
    },
    openRightDrawer () {
      this.$emit('openRightDrawer')
    },
    showUser () {
      if (!this.user_id) {
        this.$router.push('login')
      }
    },
    addNode () {
      this.addNodeDialog = true
    },
    logout () {
      console.log('fffff')
    },
    closeAddNodeDialog () {
      this.addNodeDialog = false
    },
    showDetail () {
      this.detailDialog = true
    },
    closeDetailDialog () {
      this.detailDialog = false
    }

  }
}
</script>
<style scoped>
.chip .avatar {
  cursor: pointer
}
.chip span {
  cursor: pointer
}
.avatar {
  cursor: pointer;
}
</style>
