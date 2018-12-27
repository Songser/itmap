<template>
  <v-app>
    <v-navigation-drawer v-model="leftDrawer" :permanent="leftDrawer" fixed app>
      <app-left />
    </v-navigation-drawer>
    <app-header @openLeftDrawer="openLeftDrawer" @openRightDrawer="openRightDrawer">
    </app-header>
    <v-navigation-drawer v-model="rightDrawer" right fixed app clipped :temporary='true'>
      <app-right @closeRightDrawer="closeRightDrawer" />
    </v-navigation-drawer>
    <v-content>
      <router-view />
    </v-content>
    <v-snackbar :timeout="5000" color="error" :top="true" v-model="snackbar">
      {{snackbarContent}}
    </v-snackbar>
    <v-dialog v-model="addNodeDialog" max-width="600px" persistent>
      <add-node @closeAddNodeDialog="closeAddNodeDialog" @openAddNodeDialog="openAddNodeDialog" />
    </v-dialog>
    <v-dialog  v-model="detailDialog" fullscreen hide-overlay scrollable transition="dialog-bottom-transition">
      <node-info @closeDetailDialog="closeDetailDialog" @openDetailDialog="openDetailDialog" />
    </v-dialog>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'

import AppHeader from '@/views/AppHeader'
import AppLeft from '@/views/AppLeft'
import AppRight from '@/views/AppRight'
import AddNode from '@/views/AddNode'
import NodeInfo from '@/views/NodeInfo'
export default {
  name: 'layout',
  components: {
    AppHeader,
    AppLeft,
    AppRight,
    AddNode,
    NodeInfo
  },
  data () {
    return {
      leftDrawer: true,
      rightDrawer: false,
      addNodeDialog: false,
      detailDialog: false,
      mini: false
    }
  },
  created () {
    this.$root.eventHub.$on('openLeftDrawer', () => {
      this.openLeftDrawer()
    })
    this.$root.eventHub.$on('openRightDrawer', target => {
      this.openRightDrawer()
    })
  },
  computed: {
    ...mapState({
      snackbar: state => state.snackbar,
      snackbarContent: state => state.snackbarContent
    })
  },
  methods: {
    openLeftDrawer () {
      this.leftDrawer = !this.leftDrawer
    },
    openRightDrawer () {
      this.rightDrawer = true
    },
    closeAddNodeDialog () {
      this.addNodeDialog = false
    },
    openAddNodeDialog () {
      this.addNodeDialog = true
    },
    closeDetailDialog () {
      this.detailDialog = false
    },
    closeRightDrawer () {
      this.rightDrawer = false
    },
    openDetailDialog () {
      this.detailDialog = true
    }
  }
}
</script>
