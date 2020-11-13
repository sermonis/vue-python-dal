<template>
  <el-table-column
    :label="dataStructure.columnName"
  >
    <div v-if="dataStructure.value || dataStructure.value === ''" slot-scope="scope">
      <el-input v-model="getValue(scope).value"/>
    </div>
    <RecursiveElTableColumn
      v-for="(value, key) in nextData"
      :data-structure="value"
      :key="key"
      :path="[...path, key]"
    />
  </el-table-column>
</template>

<script>
export default {
  name: 'RecursiveElTableColumn',
  props: {
    dataStructure: {
      type: Object,
      default: () => ({})
    },
    path: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    nextData() {
      return this.lodash.omit(this.dataStructure, ['columnName', 'value'])
    }
  },
  methods: {
    getValue(scope) {
      return this.path.reduce((memo, key) => memo[key], scope.row)
    }
  }
}
</script>

<style lang="scss" module>
</style>