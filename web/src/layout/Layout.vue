<template>
  <v-app>
    <v-navigation-drawer v-model="leftDrawer" :permanent="leftDrawer" fixed app>
      <app-left />
    </v-navigation-drawer>
    <app-header @openLeftDrawer="openLeftDrawer" @openRightDrawer="openRightDrawer">
    </app-header>
    <v-navigation-drawer v-model="rightDrawer" right fixed app clipped :temporary='true'>
      <app-right />
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
import AppRight from "@/views/AppRight";
export default {
  name: "layout",
  components: {
    AppHeader,
    AppLeft,
    AppRight
  },
  data () {
    return {
      leftDrawer: true,
      rightDrawer: false,
      mini: false,
    }
  },
  created() {
    this.$root.eventHub.$on('openLeftDrawer',() => {
      this.openLeftDrawer()
    });
    this.$root.eventHub.$on('openRightDrawer', (target) => {
      this.openRightDrawer()
    })
  },
  computed: {
    ...mapState({
      snackbar: state => state.snackbar,
      snackbarContent: state => state.snackbarContent,
    })
  },
  methods: {
    openLeftDrawer(){
      this.leftDrawer = !this.leftDrawer
    },
    openRightDrawer() {
      this.rightDrawer = true
    }
  }
};
</script>
