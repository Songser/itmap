<template>
  <v-toolbar>
    <v-toolbar-side-icon @click.stop="openLeftDrawer"></v-toolbar-side-icon>
    <v-toolbar-title>ITMAP</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon>
      <v-icon>search</v-icon>
    </v-btn>
    <v-chip close @click="showUser" @input="logout">
      <v-avatar>
        <img :src="avatar" alt="trevor" :onerror="defaultImage">
      </v-avatar>
      {{name}}
    </v-chip>
    <v-btn icon @click="openRightDrawer">
      <v-icon>more_vert</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "app-header",
  data () {
    return {
      defaultImage: 'this.src="' + require('../assets/logo.png') + '"'
    }
  },
  computed: {
    ...mapState({
      user_id: state => state.user.id,
      name: state => state.user.name,
      avatar: state => state.user.avatar
    })
  },
  methods: {
    openLeftDrawer() {
      this.$emit("openLeftDrawer");
    },
    openRightDrawer() {
      this.$emit("openRightDrawer")
    },
    showUser () {
      if (!this.user_id){
        this.$router.push("login");
      }
    },
    logout () {
      console.log('fffff')
    }
  },
};
</script>
