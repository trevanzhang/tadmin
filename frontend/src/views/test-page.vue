<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-4">测试页面</h1>
    <p>如果你能看到这个页面，说明Vue路由工作正常。</p>
    <p>当前时间：{{ currentTime }}</p>
    <el-button @click="showMessage" type="primary">测试按钮</el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const currentTime = ref('')

const showMessage = () => {
  ElMessage.success('测试成功！')
}

onMounted(() => {
  currentTime.value = new Date().toLocaleString()
})
</script>