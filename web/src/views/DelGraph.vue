<template>
  <section>
    <v-btn icon ripple @click="openDialog">
      <v-icon color="grey lighten-1">close</v-icon>
    </v-btn>
    <v-dialog v-model="showDialog" max-width="500px" lazy persistent>
      <v-card>
        <v-card-title>
          删除图谱
        </v-card-title>
        <v-card-text>
          确认删除图谱：{{graph.name}}
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" flat @click.stop="delGraph">确定</v-btn>
          <v-btn color="primary" flat @click.stop="showDialog=false">取消</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </section>
</template>
<script>
export default {
  name: "del-graph",
  props: ["graph"],
  data () {
    return {
      showDialog: false
    }
  },
  methods: {
    openDialog () {
      this.showDialog = true
    },
    clear () {

    }
  }
};
</script>

