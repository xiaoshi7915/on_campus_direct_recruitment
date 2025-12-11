<template>
  <MainLayout>
    <div class="home">
      <h1 class="text-3xl font-bold">校园直聘平台</h1>
      <p class="mt-4">欢迎使用校园直聘平台</p>
      <div class="mt-8">
        <router-link to="/login" class="btn-primary mr-4">登录</router-link>
        <router-link to="/register" class="btn-secondary">注册</router-link>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import MainLayout from '@/components/layouts/MainLayout.vue'
// 首页组件
</script>

<style scoped>
.home {
  padding: 2rem;
}

.btn-primary {
  @apply px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600;
}

.btn-secondary {
  @apply px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600;
}
</style>

