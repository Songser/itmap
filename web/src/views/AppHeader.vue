<template>
  <v-toolbar>
    <v-toolbar-side-icon @click.stop="openLeftDrawer"></v-toolbar-side-icon>
    <v-toolbar-title>ITMAP</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn icon>
      <v-icon>search</v-icon>
    </v-btn>
    <v-btn icon>
      <v-icon>more_vert</v-icon>
    </v-btn>
  </v-toolbar>

</template>

<script>
import { mapMutations } from 'vuex'
export default {
  name: "app-header",
  methods: {
    openLeftDrawer () {
      this.$emit('openLeftDrawer')
    }
  }
};
</script>
