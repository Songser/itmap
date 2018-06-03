<template>
  <v-app>
    <v-navigation-drawer v-model="leftDrawer" app fixed persistent>
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
  </v-app>
</template>

<script>
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
