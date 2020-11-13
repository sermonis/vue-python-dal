<template>
  <el-input
    v-model="field.value"
    :disabled="!isActive"
    @change="onInput($event)"
  >
    <i
      v-if="isActive"
      class="el-icon-refresh el-input__icon"
      slot="suffix"
      @click="field.value = savedValue"
    >
    </i>
  </el-input>
</template>

<script>
export default {
  name: 'TableInput',
  model: {
    prop: 'data',
    event: 'change-value'
  },
  props: {
    scopeData: {
      type: Object,
      required: true
    },
    activeRow: {
      type: Number,
      default: -1
    },
    data: {
      type: Array,
      default: () => []
    },
    path: {
      type: Array,
      default: () => []
    },
  },
  data() {
    return {
      savedValue: ''
    }
  },
  created() {
    this.savedValue = this.field.value
  },
  computed: {
    isActive() {
      return this.scopeData.$index === this.activeRow
    },
    field() {
      return this.path.reduce((memo, key) => memo[key], this.data[this.scopeData.$index])
    }
  },
  methods: {
    onInput() {
      this.$emit('change-value', this.data)
    }
  },
  watch: {
    activeRow: function(prevValue, nextValue) {
      if (prevValue && !nextValue) {
        this.savedValue = this.field.value
      }
    }
  }
}
</script>
