<template>
    <v-list dense>
      <v-list-tile>
        <v-list-tile-action>
          <v-icon>home</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>Home</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-list-tile>
        <v-list-tile-action>
          <v-icon>contact_mail</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>Contact</v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
    </v-list>
</template>

<script>
import { mapState } from 'vuex'
export default {
  name: 'app-left',
  data () {
    return {
      drawer: this.$store.state.leftDrawer
    }
  }
  // computed: {
  //   ...mapState({
  //     drawer: 'leftDrawer'
  //   })
  // }
};
</script>

<style>
</style>
