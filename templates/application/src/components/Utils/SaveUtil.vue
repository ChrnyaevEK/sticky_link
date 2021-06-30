<template id="save-util-template">
    <span
        class="small font-weight-bold d-flex align-items-center"
        :class="io.saveUtil.type ? 'text-' + io.saveUtil.type : 'text-secondary'"
        v-show="io.saveUtil.state"
    >
        {{ io.saveUtil.state }}
    </span>
</template>
<script>
import io from "../../modules/io";

export default {
  data() {
    return {
      io,
    };
  },
};
</script>

<style scoped>
.change-sync {
  border-radius: 50%;
  width: 0.5rem;
  height: 0.5rem;
}
</style>
