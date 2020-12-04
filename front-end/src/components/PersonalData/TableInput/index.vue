<template>
  <el-input
    v-model="value"
    :disabled="!isActive"
  >
    <i
      v-if="isActive"
      class="el-icon-refresh el-input__icon"
      slot="suffix"
      @click="value = savedValue"
    >
    </i>
  </el-input>
</template>

<script>
import { STATES } from '@/constants/personalData'

export default {
  name: 'TableInput',
  props: {
    scopeData: {
      type: Object,
      required: true
    },
    activeRow: {
      type: Number,
      default: -1
    },
    path: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
      value: '',
    }
  },
  created() {
    this.value = this.savedValue
  },
  computed: {
    isActive() {
      return this.scopeData.$index === this.activeRow
    },
    savedValue() {
      return this.lodash.get(this.scopeData.row, this.path, {value: ''}).value
    }
  },
  watch: {
    isActive(nextValue, prevValue) {
      if (prevValue && !nextValue) {
        if (this.activeRow === STATES.success) {
          this.$emit('change-value', {
            value: this.value,
            path: [this.scopeData.$index, ...this.path]
          })
        } else {
          this.value = this.savedValue
        }
      }
    },
    savedValue(nextValue) {
      this.value = nextValue
    }
  }
}
</script>
