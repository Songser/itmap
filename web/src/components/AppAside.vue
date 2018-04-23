<template>
    <graph-info />
</template>
<script>
import { mapState } from 'vuex'
import GraphInfo from '@/components/GraphInfo'
export default {
  name: 'app-aside',
  components: { GraphInfo },
  data: function () {
    return {
      nodeName: ''
    }
  },
  methods: {
    addNode () {
      this.$store.commit('addNode', this.nodeName)
    }
  },
  computed: mapState({
    node: state => state.node
  })
}
</script>
