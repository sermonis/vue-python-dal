<template>
  <div :class="$style.root">
    <el-table
      :data="data"
      height="90vh"
    >
      <RecursiveColumn
        v-for="(value, key) in data[0]"
        :key="key"
        :data-structure="value"
        v-model="data"
        :path="[key]"
        :activeRow="changingElementIndex"
      />
      <el-table-column
        fixed="right"
        width="110"
      >
        <template slot-scope="scope">
          <div :class="$style.controls">
            <el-button
              :type="changingElementIndex === scope.$index ? 'success' : 'primary'"
              :icon="changingElementIndex === scope.$index ? 'el-icon-check' : 'el-icon-edit'"
              circle
              @click="changingElementIndex === scope.$index ? commitChangeInfoSingle() : startChangeInfoSingle(scope.$index)"
            />
            <el-button
              type="danger"
              icon="el-icon-delete"
              circle
              v-if="changingElementIndex === scope.$index"
              @click="abortChangeInfoSingle(scope.$index)"
            />
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import {data as pd} from './test-data.json';
import RecursiveColumn from '@/components/PersonalData/RecursiveElTableColumn/index.vue';

export default {
  name: 'Table',
  components: {RecursiveColumn},
  data() {
    return {
      data: pd,
      changingElementIndex: -1,
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
      this.changingElementIndex = -1;
      this.infoBackUp = null;
    },
    abortChangeInfoSingle(index) {
      this.data[index] = this.infoBackUp;
      this.changingElementIndex = -1;
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
    formatter(row, col, val, i) {
      console.log('row:', row)
      console.log('col:', col)
      console.log('vaval:',val)
      console.log('i:', i)
      return 'qwert'
    },
    test(e) {
      console.log(e)
      this.$emit('value-input', e)
    }
  },
  filters: {
    test(scope) {
      return scope.row.fullName.firstName;
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
  // display: flex;
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