<template>
  <el-table-column
    :label="dataStructure.columnName"
    width="150px"
  >
    <TableInput
      v-if="dataStructure.value || dataStructure.value === ''"
      slot-scope="scope"
      :scope-data="scope"
      :data="data"
      :activeRow="activeRow"
      :path="path"
    />
    <RecursiveElTableColumn
      v-for="(value, key) in nextData"
      :data-structure="value"
      :key="key"
      :path="[...path, key]"
      :activeRow="activeRow"
      :data="data"
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
  model: {
    prop: 'data',
    event: 'change-value'
  },
  props: {
    dataStructure: {
      type: Object,
      default: () => ({})
    },
    data: {
      type: Array,
      default: () => []
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