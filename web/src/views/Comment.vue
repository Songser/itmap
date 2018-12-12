<template>

</template>
<script>
import { mapState } from "vuex";
export default {
  name: "app-comment",
  data() {
    return {
      nodeId: 0,
      items: [],
      page: 0,
      offsetTop: 0,
      active: -1,
    };
  },
  computed: {
    ...mapState({
      node: state => state.node
    })
  },
}
</script>
