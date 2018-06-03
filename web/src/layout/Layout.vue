<template>
  <v-app>
    <v-navigation-drawer v-model="leftDrawer" app fixed enable-resize-watcher persistent>
      <app-left />
    </v-navigation-drawer>
    <v-toolbar app>
      <app-header @openLeftDrawer="openLeftDrawer" @openRightDrawer="openRightDrawer"/>
    </v-toolbar>
    <v-navigation-drawer v-model="rightDrawer" right fixed app clipped>
    </v-navigation-drawer>
    <v-content>
      <router-view />
    </v-content>
    <v-snackbar :timeout="5000" color="error" :top="true"  v-model="snackbar">
      {{snackbarContent}}
    </v-snackbar>
  </v-app>
</template>

<script>
import { mapState } from "vuex";

import AppHeader from "@/views/AppHeader";
import AppLeft from "@/views/AppLeft";
export default {
  name: "layout",
  components: {
    AppHeader,
    AppLeft
  },
  data () {
    return {
      leftDrawer: true,
      rightDrawer: false,
      mini: true,
    }
  },
  computed: {
    ...mapState({
      snackbar: state => state.snackbar,
      snackbarContent: state => state.snackbarContent,
    })
  },
  methods: {
    openLeftDrawer(){
      this.leftDrawer = true
    },
    openRightDrawer() {
      this.rightDrawer = true
    }
  }
};
</script>
