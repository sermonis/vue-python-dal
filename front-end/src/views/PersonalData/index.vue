<template>
  <div :class="$style.root">
    <el-table
      :data="data"
      height="90vh"
    >
      <RecursiveColumn
        v-for="(value, key) in tableStructure"
        :key="key"
        :data-structure="value"
        :path="[key]"
        :activeRow="changingElementIndex"
        @change-value="onChangeValue($event)"
      />
      <el-table-column
        fixed="right"
        width="160"
      > 
        <template
          slot-scope="scope"
          slot="header"
        >
          <el-button
            icon="el-icon-plus"
            circle
            :disabled="changingElementIndex > -1"
            @click="addEntry"
          />
        </template>
        <template slot-scope="scope">
          <div :class="$style.controls">
            <el-button
              :type="changingElementIndex === scope.$index
                ? 'success'
                : 'primary'
              "
              :icon="changingElementIndex === scope.$index
                ? 'el-icon-check'
                : 'el-icon-edit'
              "
              circle
              @click="changingElementIndex === scope.$index
                ? commitChangeInfoSingle()
                : startChangeInfoSingle(scope.$index)
              "
            />
            <el-button
              type="danger"
              icon="el-icon-close"
              circle
              v-if="changingElementIndex === scope.$index"
              @click="abortChangeInfoSingle(scope.$index)"
            />
            <el-button
              type="info"
              icon="el-icon-delete"
              v-if="changingElementIndex === scope.$index && !isNewItem"
              circle
              @click="deleteItem(scope.$index)"
            />
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import RecursiveColumn from '@/components/PersonalData/RecursiveElTableColumn/index.vue';
import { STATES } from '@/constants/personalData'
import {data as pd} from './testData';


export default {
  name: 'Table',
  components: {RecursiveColumn},
  data() {
    return {
      data: pd.tableData,
      tableStructure: pd.tableStructure,
      changingElementIndex: -1,
      isNewItem: false,
      infoBackUp: null,
      sct: {}
    }
  },
  methods: {
    startChangeInfoSingle(index) {
      this.changingElementIndex = index;
      this.infoBackUp = this.lodash.cloneDeep(this.data[index]);
    },
    commitChangeInfoSingle() {
      this.changingElementIndex = STATES.success
      this.infoBackUp = null
      this.isNewItem = false
    },
    abortChangeInfoSingle(index) {
      this.changingElementIndex = STATES.abort
      if (this.isNewItem) {
        this.isNewItem = false
        this.data.shift()
      } else {
        this.data[index] = this.infoBackUp
      }
    },
    abortChangeInfoField(index, ...keys) {
      const dataContainer = keys.slice(0, keys.length - 2).reduce(
        (memo, key) => memo[key],
        this.data[index]
      );
      const value = keys.reduce((memo, key) => memo[key], this.infoBackUp);
      console.log('dataContainer', dataContainer)
      console.log('value', value)
      dataContainer[keys[keys.length - 2]] = {
        ...dataContainer[keys[keys.length - 2]],
        [keys[keys.length - 1]]: value
      };
    },
    addEntry() {
      console.log(this.lodash.cloneDeep(this.tableStructure));
      this.data.unshift(this.lodash.cloneDeep(this.tableStructure))
      this.changingElementIndex = 0
      this.isNewItem = true
      this.$forceUpdate()
    },
    deleteItem(index) {
      this.data.splice(index, 1)
      this.changingElementIndex = STATES.success;
    },
    onChangeValue(e) {
      this.lodash.update(this.data, [...e.path, 'value'], () => e.value)
    }
  }
}
</script>

<style lang="scss" module>
.root {
  padding: 20px;
  max-width: 1200px;
  margin: auto;
}

.studentsTabel {
  &, & > thead, & > tbody {
    width: 100%;
  }

  &Head {
    &Item {
      padding: 5px;
      line-height: 40px;
      widows: auto;
    }
  }
}

.student {
  border: 1px solid #dbdde6;
  border-radius: 5px;
  padding: 5px;
  width: 100%;

  &Name {  
    &Input {
      width: auto;
      min-width: 0;
    }

    &Span {
      line-height: 40px;
      padding: 5px;
    }
  }
}
.controls {
  display: flex;
}
</style>