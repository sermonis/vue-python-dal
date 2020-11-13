<template>
  <div>
    <template v-for="key in keys">
      <template v-if="dataStructure[key].columnName">
        <el-table-column
          :key="key"
          :label="dataStructure[key].columnName"
          :width="key === 'fix' ? 0 : null"
        >
          <template slot-scope="scope">
            <el-input
              v-model="getValue(scope)[key].value"
            />
          </template>
        </el-table-column>
      </template>
      <template v-else>
        <RecursiveElTableColumn
          :key="key"
          :data-structure="dataStructure[key]"
          :data="data"
          :path="[...path, key]"
        />
      </template>
    </template>
  </div>
</template>

<script>
export default {
  name: 'RecursiveElTableColumn',
  props: {
    dataStructure: {
      type: Object,
      default: () => ({})
    },
    data: {
      type: [Object, Array],
      default: () => ({})
    },
    path: {
      type: Array,
      default: () => []
    },
  },
  computed: {
    keys() {
      return Object.keys(this.dataStructure)
    }
  },
  methods: {
    isObj(obj) {
      return this.lodash.isPlainObject(obj)
    },
    getValue(scope) {
      return this.path.reduce((memo, key) => memo[key], this.data[scope.$index])
    }
  }
}
</script>

<style lang="scss" module>
</style>