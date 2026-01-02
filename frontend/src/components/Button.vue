<template>
  <component
    :is="tag"
    :type="type"
    :disabled="disabled"
    :class="buttonClasses"
    @click="handleClick"
  >
    <slot name="icon">
      <component
        v-if="icon"
        :is="iconComponent"
        :class="iconClasses"
      />
    </slot>
    <span v-if="$slots.default" :class="textClasses">
      <slot />
    </span>
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'outline-primary' | 'outline-secondary' | 'outline-success' | 'outline-danger' | 'ghost' | 'ghost-primary' | 'link'
  size?: 'sm' | 'md' | 'lg'
  icon?: string
  iconPosition?: 'left' | 'right'
  disabled?: boolean
  loading?: boolean
  fullWidth?: boolean
  type?: 'button' | 'submit' | 'reset'
  tag?: 'button' | 'a' | 'router-link'
  to?: string
  href?: string
  title?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  iconPosition: 'left',
  disabled: false,
  loading: false,
  fullWidth: false,
  type: 'button',
  tag: 'button'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const buttonClasses = computed(() => {
  const classes = ['btn', `btn-${props.variant}`, `btn-${props.size}`]
  
  if (props.disabled || props.loading) {
    classes.push('btn-disabled')
  }
  if (props.loading) {
    classes.push('btn-loading')
  }
  if (props.fullWidth) {
    classes.push('btn-full')
  }
  
  return classes
})

const handleClick = (event: MouseEvent) => {
  if (props.disabled || props.loading) {
    event.preventDefault()
    return
  }
  emit('click', event)
}
</script>

<style scoped>
/* 按钮基础样式 */
.btn {
  @apply inline-flex items-center justify-center font-medium transition-all duration-200;
  @apply focus:outline-none focus:ring-2 focus:ring-offset-2;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
  border-radius: 0.75rem;
  position: relative;
  overflow: hidden;
}

/* 按钮尺寸 */
.btn-sm {
  @apply px-3 py-1.5 text-sm;
  min-height: 2rem;
}

.btn-md {
  @apply px-4 py-2.5 text-base;
  min-height: 2.75rem;
}

.btn-lg {
  @apply px-6 py-3.5 text-lg;
  min-height: 3.5rem;
}

/* 主要按钮 - 渐变紫色 */
.btn-primary {
  background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
  @apply text-white shadow-md;
  @apply hover:shadow-lg hover:-translate-y-0.5;
  @apply focus:ring-primary-500;
}

.btn-primary::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-primary:hover:not(:disabled)::before {
  left: 100%;
}

/* 次要按钮 - 灰色边框 */
.btn-secondary {
  @apply bg-white text-gray-700 border-2 border-gray-300;
  @apply hover:bg-gray-50 hover:border-gray-400;
  @apply focus:ring-gray-500;
}

/* 成功按钮 - 绿色 */
.btn-success {
  @apply bg-green-600 text-white shadow-md;
  @apply hover:bg-green-700 hover:shadow-lg hover:-translate-y-0.5;
  @apply focus:ring-green-500;
}

/* 警告按钮 - 黄色 */
.btn-warning {
  @apply bg-yellow-500 text-white shadow-md;
  @apply hover:bg-yellow-600 hover:shadow-lg hover:-translate-y-0.5;
  @apply focus:ring-yellow-500;
}

/* 危险按钮 - 红色 */
.btn-danger {
  @apply bg-red-600 text-white shadow-md;
  @apply hover:bg-red-700 hover:shadow-lg hover:-translate-y-0.5;
  @apply focus:ring-red-500;
}

/* 轮廓按钮 - 透明背景，有边框 */
.btn-outline {
  @apply bg-transparent border-2;
  @apply hover:bg-opacity-10;
}

.btn-outline.btn-primary {
  @apply border-primary-600 text-primary-600;
  @apply hover:bg-primary-50;
}

.btn-outline.btn-success {
  @apply border-green-600 text-green-600;
  @apply hover:bg-green-50;
}

.btn-outline.btn-danger {
  @apply border-red-600 text-red-600;
  @apply hover:bg-red-50;
}

/* 幽灵按钮 - 无边框，悬停时显示背景 */
.btn-ghost {
  @apply bg-transparent;
  @apply hover:bg-gray-100;
}

.btn-ghost.btn-primary {
  @apply text-primary-600;
  @apply hover:bg-primary-50;
}

/* 链接按钮 - 无背景，仅文字 */
.btn-link {
  @apply bg-transparent p-0 underline-offset-4;
  @apply hover:underline;
}

.btn-link.btn-primary {
  @apply text-primary-600;
}

/* 图标样式 */
.btn-icon {
  @apply flex-shrink-0;
  width: 1.25rem;
  height: 1.25rem;
}

.btn-icon-left {
  @apply mr-2;
}

.btn-icon-right {
  @apply ml-2;
}

.btn-icon-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 文字样式 */
.btn-text {
  @apply whitespace-nowrap;
}

/* 全宽按钮 */
.btn-full-width {
  @apply w-full;
}

/* 加载状态 */
.btn-loading {
  @apply cursor-wait;
}
</style>

