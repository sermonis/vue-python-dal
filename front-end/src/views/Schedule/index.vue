<template>
  <div class="app-container">
    <Schedule />
  </div>
</template>

<script>
import Schedule from "../../components/Schedule/Schedule";

export default {
  components: {
    Schedule,
  },
  data() {
    return {};
  },
  created() {
    this.fetchData();
  },
  methods: {
    fetchData() {},
  },
};
</script>
