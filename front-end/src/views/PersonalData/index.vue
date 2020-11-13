<template>
  <div :class="$style.root">
    <!-- <table :class="$style.studentsTabel">
      <thead>
        <tr :class="$style.studentsTabelHead">
          <td :class="$style.studentsTabelHeadItem">Фамилия</td>
          <td :class="$style.studentsTabelHeadItem">Имя</td>
          <td :class="$style.studentsTabelHeadItem">Отчество</td>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="({
            fullName,
            id,
          }, index) in data"
          :key="id"
          :class="$style.student"
        >
          <td
            v-for="(value, key) in fullName"
            :key="key"
            :class="$style.studentNameInputWrapper"
          >
            <component
              :is="index === changingElementIndex ? 'el-input' : 'span'"
              ::class="$style.index === changingElementIndex ? 'studentNameInput' : 'studentNameSpan'"
              v-model="fullName[key]"
              minlength="1"
            >
              {{value}}
              <i
                v-if="index === changingElementIndex"
                :class="$style.el-icon-refresh el-input__icon"
                slot="suffix"
                @click="abortChangeInfoField(index, 'fullName', key)">
              </i>
            </component>
          </td>
          <td :class="$style.controls">
            <el-button
              :type="changingElementIndex === index ? 'success' : 'primary'"
              :icon="changingElementIndex === index ? 'el-icon-check' : 'el-icon-edit'"
              circle
              @click="changingElementIndex === index ? commitChangeInfoSingle() : startChangeInfoSingle(index)"
            />
            <el-button
              type="danger"
              icon="el-icon-delete"
              circle
              v-if="changingElementIndex === index"
              @click="abortChangeInfoSingle(index)"
            />
          </td>
        </tr>
      </tbody>
    </table> -->
    <el-table
      :data="data"
      height="90vh"
    >
      <el-table-column
        fixed="right"
        width="100"
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
      <RecursiveColumn :data-structure="data[0]" :data="data" />
    </el-table>
  </div>
</template>

<script>
import {data as pd} from './test-data.json';
import RecursiveColumn from '@/components/RecursiveElTableColumn/index.vue';

export default {
  components: {RecursiveColumn},
  data() {
    return {
      data: pd,
      changingElementIndex: -1,
      infoBackUp: null,
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