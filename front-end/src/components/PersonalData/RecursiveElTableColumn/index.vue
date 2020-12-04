<template>
  <el-table-column
    :label="dataStructure.columnName"
    width="150px"
  >
    <TableInput
      v-if="needInput"
      slot-scope="scope"
      :scope-data="scope"
      :activeRow="activeRow"
      :path="path"
      @change-value="onChangeValue($event)"
    />
    <RecursiveElTableColumn
      v-for="(value, key) in nextData"
      :data-structure="value"
      :key="`${path.join('-')}-${key}`"
      :path="[...path, key]"
      :activeRow="activeRow"
      @change-value="onChangeValue($event)"
    />
  </el-table-column>
</template>

<script>
import TableInput from '../TableInput/index.vue'

export default {
  components: {
    TableInput
  },
  name: 'RecursiveElTableColumn',
  props: {
    dataStructure: {
      type: Object,
      default: () => ({})
    },
    path: {
      type: Array,
      default: () => []
    },
    activeRow: {
      type: Number,
      default: -1
    }
  },
  computed: {
    nextData() {
      return this.lodash.omit(this.dataStructure, ['columnName', 'value'])
    },
    needInput() {
      return !Object.keys(this.nextData).length
    }
  },
  methods: {
    onChangeValue(e) {
      this.$emit('change-value', e)
    }
  },
}
</script>

<style lang="scss" module>
</style>