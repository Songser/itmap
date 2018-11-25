<template>
  <v-card tile>
    <v-toolbar card dark color="primary">
      <v-btn icon dark @click="closeDialog">
        <v-icon>close</v-icon>
      </v-btn>
      <!-- <v-toolbar-title>Settings</v-toolbar-title> -->
      <v-spacer></v-spacer>
      <v-tabs color="primary" fixed-tabs>
        <v-tab v-for="n in 3" :key="n" :href="`#tab-${n}`">
          Item {{ n }}
        </v-tab>
      </v-tabs>

    </v-toolbar>
    <v-tabs-items >
      <v-tab-item v-for="i in 3" :id="`tab-${i}`" :key="i">

      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>
<script>
export default {
  name: "node-info",
  data () {
    return {
      text: 'fff',
      model: true,
    }
  },
  methods: {
    closeDialog() {
      this.$emit("closeDetailDialog");
    }
  }
};
</script>
