<template>
  <div class="select-wrapper relative" ref="wrapperRef">
    <!-- 下拉框触发器 -->
    <button
      type="button"
      @click="toggleDropdown"
      class="w-full px-4 py-2.5 text-left bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200 flex items-center justify-between"
      :class="{ 'border-blue-500': isOpen }"
    >
      <span class="text-gray-700">
        <span v-if="!selectedValue" class="text-gray-400">{{ placeholder }}</span>
        <span v-else>{{ displayText }}</span>
      </span>
      <svg
        class="w-5 h-5 text-gray-400 transition-transform duration-200"
        :class="{ 'rotate-180': isOpen }"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- 下拉选项列表 -->
    <div
      v-if="isOpen"
      class="absolute z-50 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-y-auto"
    >
      <!-- 搜索框（可选） -->
      <div v-if="searchable" class="p-2 border-b border-gray-200 sticky top-0 bg-white">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="搜索..."
          class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          @click.stop
        />
      </div>

      <!-- 选项列表 -->
      <div class="py-1">
        <button
          v-for="option in filteredOptions"
          :key="getOptionValue(option)"
          type="button"
          class="w-full text-left flex items-center px-4 py-2 hover:bg-gray-50 cursor-pointer transition-colors"
          :class="{ 'bg-blue-50 text-blue-700': isSelected(option) }"
          @click.stop="selectOption(option)"
        >
          <svg
            v-if="isSelected(option)"
            class="w-4 h-4 mr-2 text-blue-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <span v-else class="w-4 h-4 mr-2"></span>
          <span class="text-sm text-gray-700">{{ getOptionLabel(option) }}</span>
        </button>
        <div v-if="filteredOptions.length === 0" class="px-4 py-2 text-sm text-gray-500 text-center">
          无匹配选项
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

interface Props {
  modelValue: string | number | null | undefined
  options: Array<{ id?: string | number; value?: string | number; label?: string; name?: string } | string | number>
  placeholder?: string
  searchable?: boolean
  optionValue?: string // 用于指定选项的value字段名，如 'id'
  optionLabel?: string // 用于指定选项的label字段名，如 'name'
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请选择',
  searchable: false,
  optionValue: 'id',
  optionLabel: 'name'
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number | null]
}>()

const isOpen = ref(false)
const searchQuery = ref('')
const wrapperRef = ref<HTMLElement | null>(null)
const selectedValue = computed(() => props.modelValue)

// 获取选项的值
const getOptionValue = (option: any): string | number => {
  if (typeof option === 'string' || typeof option === 'number') {
    return option
  }
  return option[props.optionValue] ?? option.id ?? option.value ?? option
}

// 获取选项的标签
const getOptionLabel = (option: any): string => {
  if (typeof option === 'string' || typeof option === 'number') {
    return String(option)
  }
  return option[props.optionLabel] ?? option.label ?? option.name ?? String(getOptionValue(option))
}

// 判断选项是否被选中
const isSelected = (option: any): boolean => {
  const value = getOptionValue(option)
  return selectedValue.value === value
}

// 选择选项
const selectOption = (option: any) => {
  const value = getOptionValue(option)
  emit('update:modelValue', value)
  isOpen.value = false
}

// 切换下拉框显示/隐藏
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    searchQuery.value = ''
  }
}

// 过滤选项（支持搜索）
const filteredOptions = computed(() => {
  if (!props.searchable || !searchQuery.value) {
    return props.options
  }
  
  const query = searchQuery.value.toLowerCase()
  return props.options.filter(option => {
    const label = getOptionLabel(option).toLowerCase()
    return label.includes(query)
  })
})

// 显示文本（已选中的选项）
const displayText = computed(() => {
  if (!selectedValue.value) return ''
  const option = props.options.find(opt => getOptionValue(opt) === selectedValue.value)
  return option ? getOptionLabel(option) : String(selectedValue.value)
})

// 点击外部关闭下拉框
const handleClickOutside = (event: MouseEvent) => {
  if (wrapperRef.value && !wrapperRef.value.contains(event.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.select-wrapper {
  min-width: 200px;
}
</style>

