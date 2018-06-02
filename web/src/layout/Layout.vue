<template>
  <v-app>
    <v-navigation-drawer v-model="leftDrawer" fixed app>
      <app-left />
    </v-navigation-drawer>
    <v-navigation-drawer v-model="rightDrawer" right fixed app >
      <app-left />
    </v-navigation-drawer>
    <app-header @openLeftDrawer="openLeftDrawer"/>
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
      rightDrawer: false
    }
  },
  methods: {
    openLeftDrawer(){
      this.leftDrawer = true
    }
  }
};
</script>
