<template>
  <v-layout row>
    <v-flex xs12>
      <v-card>
        <v-img
          src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
          height="200px"
        >
        </v-img>

        <v-card-title primary-title>
          <div>
            <div class="headline">{{name}}</div>
            <span class="grey--text">{{desc}}</span>
          </div>
        </v-card-title>

        <v-card-actions>
          <v-btn flat>Share</v-btn>
          <v-btn flat color="purple">Explore</v-btn>
          <v-spacer></v-spacer>

        </v-card-actions>
      </v-card>
    </v-flex>
  </v-layout>
</template>
<script>
import { mapState } from "vuex";
export default {
  name: 'app-right',
  computed: {
    ...mapState({
      nodeId: state => state.node.id,
      name: state => state.node.name,
      desc: state => state.node.desc,
      pic: state => state.node.pic,
      create_date: state => state.node.create_date,
    })
  },
}
</script>
