<template>
  <v-app>
    <v-navigation-drawer
      v-model="leftDrawer"
      :permanent="leftDrawer"
      fixed
      app
    >
      <app-left />
    </v-navigation-drawer>
    <app-header
      @openLeftDrawer="openLeftDrawer"
      @openRightDrawer="openRightDrawer"
    >
    </app-header>
    <v-navigation-drawer
      v-model="rightDrawer"
      right
      fixed
      app
      clipped
      :temporary='true'
    >
      <app-right @closeRightDrawer="closeRightDrawer" />
    </v-navigation-drawer>
    <v-content>
      <router-view />
    </v-content>
    <v-snackbar
      :timeout="3000"
      color="error"
      :top="true"
      :right="true"
      v-model="snackbar"
      dark
    >
      {{snackbarContent}}
      <v-icon
        size="16"
        @click="snackbar = false"
      >
        close
      </v-icon>
    </v-snackbar>
    <v-dialog
      v-model="addNodeDialog"
      max-width="600px"
      persistent
    >
      <add-node
        @closeAddNodeDialog="closeAddNodeDialog"
        @openAddNodeDialog="openAddNodeDialog"
      />
    </v-dialog>
    <v-dialog
      v-model="detailDialog"
      fullscreen
      hide-overlay
      scrollable
      transition="dialog-bottom-transition"
    >
      <node-info
        @closeDetailDialog="closeDetailDialog"
        @openDetailDialog="openDetailDialog"
      />
    </v-dialog>

  </v-app>
</template>

<script>
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
      mini: false,
      show: true,
      snackbar: false,
      snackbarContent: ''
    }
  },
  created () {
    this.$root.eventHub.$on('openLeftDrawer', () => {
      this.openLeftDrawer()
    })
    this.$root.eventHub.$on('openRightDrawer', target => {
      this.openRightDrawer()
    })
    this.$root.eventHub.$on('snackbar', target => {
      this.snackbar = true
      this.snackbarContent = target
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
<style scoped>
.v-tooltip {
  position: fixed;
  left: 50%;
}
</style>
