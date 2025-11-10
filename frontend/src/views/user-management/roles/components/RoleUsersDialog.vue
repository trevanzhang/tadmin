<template>
  <el-dialog
    v-model="dialogVisible"
    :title="`角色用户 - ${role?.name || ''}`"
    width="800px"
    @close="handleClose"
  >
    <div v-loading="loading">
      <!-- 角色信息 -->
      <el-descriptions :column="2" border class="mb-4">
        <el-descriptions-item label="角色名称">
          {{ role?.name }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="role?.is_active ? 'success' : 'danger'" size="small">
            {{ role?.is_active ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">
          {{ role?.description || '-' }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- 用户列表 -->
      <el-table
        :data="userList"
        stripe
        style="width: 100%"
        empty-text="暂无用户"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="full_name" label="姓名" min-width="120">
          <template #default="{ row }">
            {{ row.full_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_superuser" label="超级用户" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.is_superuser" type="warning" size="small">是</el-tag>
            <span v-else class="text-gray-400">否</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-end mt-4" v-if="userList.length > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <template #footer>
      <el-button @click="handleClose">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { getRoleUsers, type Role } from '@/api/user'
import { formatDateTime } from '@/utils/formatTime'

// Props
interface Props {
  visible: boolean
  role?: Role | null
}

const props = withDefaults(defineProps<Props>(), {
  role: null
})

// Emits
const emit = defineEmits<{
  'update:visible': [visible: boolean]
}>()

// 响应式数据
const loading = ref(false)
const userList = ref<any[]>([])

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 计算属性
const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

// 获取角色用户列表
const fetchRoleUsers = async () => {
  if (!props.role) return

  try {
    loading.value = true
    const params = {
      skip: (pagination.page - 1) * pagination.size,
      limit: pagination.size
    }

    const response = await getRoleUsers(props.role.id, params)
    userList.value = response.data || []
    // 注意：实际项目中后端应该返回总数，这里先用列表长度模拟
    pagination.total = userList.value.length
  } catch (error) {
    console.error('获取角色用户失败:', error)
    ElMessage.error('获取角色用户失败')
  } finally {
    loading.value = false
  }
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.size = size
  fetchRoleUsers()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchRoleUsers()
}

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false
  // 重置数据
  userList.value = []
  pagination.page = 1
  pagination.total = 0
}

// 监听visible变化
watch(() => props.visible, (visible) => {
  if (visible && props.role) {
    fetchRoleUsers()
  }
})

// 监听role变化
watch(() => props.role, (role) => {
  if (props.visible && role) {
    fetchRoleUsers()
  }
})
</script>

<style scoped>
.el-descriptions {
  margin-bottom: 20px;
}
</style>