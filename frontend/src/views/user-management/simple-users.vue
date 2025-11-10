<template>
  <div class="main-content p-6">
    <h1 class="text-2xl font-bold mb-6">简化用户管理</h1>

    <div class="mb-4">
      <el-button type="primary" @click="loadUsers">重新加载用户</el-button>
      <span class="ml-4">状态：{{ loading ? '加载中...' : '已加载' }}</span>
    </div>

    <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded">
      错误：{{ error }}
    </div>

    <div v-if="users.length > 0">
      <table class="w-full border-collapse border border-gray-300">
        <thead>
          <tr class="bg-gray-100">
            <th class="border border-gray-300 p-2">ID</th>
            <th class="border border-gray-300 p-2">用户名</th>
            <th class="border border-gray-300 p-2">邮箱</th>
            <th class="border border-gray-300 p-2">状态</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="border border-gray-300 p-2">{{ user.id }}</td>
            <td class="border border-gray-300 p-2">{{ user.username }}</td>
            <td class="border border-gray-300 p-2">{{ user.email }}</td>
            <td class="border border-gray-300 p-2">
              <span :class="user.is_active ? 'text-green-600' : 'text-red-600'">
                {{ user.is_active ? '启用' : '禁用' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else-if="!loading" class="text-gray-500">
      暂无用户数据
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface User {
  id: number
  username: string
  email: string
  is_active: boolean
}

const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')

const loadUsers = async () => {
  try {
    loading.value = true
    error.value = ''

    // 使用正确的token获取方法
    const { getToken } = await import('@/utils/auth')
    const tokenData = getToken()
    const accessToken = tokenData?.accessToken

    if (!accessToken) {
      throw new Error('未找到访问令牌，请重新登录')
    }

    const response = await fetch('/api/v1/users/', {
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()
    users.value = data.data || []
    console.log('用户数据加载成功:', users.value)
  } catch (err) {
    error.value = err instanceof Error ? err.message : '未知错误'
    console.error('加载用户失败:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadUsers()
})
</script>