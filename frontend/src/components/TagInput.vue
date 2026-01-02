<template>
  <div class="tag-input-wrapper">
    <label v-if="label" class="block text-sm font-semibold text-gray-700 mb-2">{{ label }}</label>
    <div class="w-full px-4 py-3 border border-gray-300 rounded-xl focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 transition-all duration-200 bg-white min-h-[3rem] flex flex-wrap items-center gap-2">
      <!-- 已添加的标签 -->
      <span
        v-for="(tag, index) in tags"
        :key="index"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
      >
        {{ tag }}
        <button
          type="button"
          @click="removeTag(index)"
          class="ml-2 text-blue-600 hover:text-blue-800 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </span>
      
      <!-- 输入框 -->
      <input
        ref="inputRef"
        v-model="inputValue"
        type="text"
        :placeholder="placeholder"
        class="flex-1 min-w-[120px] outline-none text-gray-900 bg-transparent"
        @keydown.enter.prevent="addTag"
        @keydown.comma.prevent="addTag"
        @keydown.backspace="handleBackspace"
        @blur="handleBlur"
      />
    </div>
    <p v-if="hint" class="mt-1 text-xs text-gray-500">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'

interface Props {
  modelValue: string[]
  label?: string
  placeholder?: string
  hint?: string
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '输入标签后按回车或逗号添加',
  hint: '输入标签后按回车或逗号添加，点击标签可删除'
})

const emit = defineEmits<{
  'update:modelValue': [value: string[]]
}>()

const tags = ref<string[]>([])
const inputValue = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

// 同步外部值
watch(() => props.modelValue, (newValue) => {
  if (newValue && Array.isArray(newValue)) {
    tags.value = [...newValue]
  } else {
    tags.value = []
  }
}, { immediate: true })

// 添加标签
const addTag = () => {
  const trimmed = inputValue.value.trim()
  if (trimmed && !tags.value.includes(trimmed)) {
    tags.value.push(trimmed)
    emit('update:modelValue', [...tags.value])
    inputValue.value = ''
  }
}

// 删除标签
const removeTag = (index: number) => {
  tags.value.splice(index, 1)
  emit('update:modelValue', [...tags.value])
}

// 处理退格键
const handleBackspace = (e: KeyboardEvent) => {
  if (inputValue.value === '' && tags.value.length > 0) {
    tags.value.pop()
    emit('update:modelValue', [...tags.value])
  }
}

// 处理失焦
const handleBlur = () => {
  if (inputValue.value.trim()) {
    addTag()
  }
}
</script>

<style scoped>
.tag-input-wrapper {
  @apply w-full;
}
</style>

