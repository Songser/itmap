<template>
    <node-info />
</template>
<script>
import { mapState } from 'vuex'
import NodeInfo from '@/components/NodeInfo'
export default {
  name: 'app-aside',
  components: { NodeInfo },
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
