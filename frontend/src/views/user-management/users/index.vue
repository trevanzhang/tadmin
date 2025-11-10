<template>
  <div class="main-content">
    <!-- 页面标题和操作按钮 -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">用户管理</h1>
      <el-button
        type="primary"
        :icon="Plus"
        @click="handleCreate"
      >
        新增用户
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="mb-6" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="用户名、邮箱或姓名"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
            style="width: 240px"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select
            v-model="searchForm.is_active"
            placeholder="全部状态"
            clearable
            @change="handleSearch"
            style="width: 120px"
          >
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
          </el-select>
        </el-form-item>
        <el-form-item label="角色">
          <el-select
            v-model="searchForm.role_name"
            placeholder="全部角色"
            clearable
            @change="handleSearch"
            style="width: 150px"
          >
            <el-option
              v-for="role in roleOptions"
              :key="role.name"
              :label="role.description || role.name"
              :value="role.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 用户列表 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="userList"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="120" />
        <el-table-column prop="email" label="邮箱" min-width="180" />
        <el-table-column prop="full_name" label="姓名" min-width="120">
          <template #default="{ row }">
            {{ row.full_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="role_names" label="角色" min-width="150">
          <template #default="{ row }">
            <el-tag
              v-for="roleName in row.role_names"
              :key="roleName"
              size="small"
              class="mr-1"
            >
              {{ getRoleDisplayName(roleName) }}
            </el-tag>
            <span v-if="!row.role_names.length" class="text-gray-400">无角色</span>
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
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              link
              type="warning"
              size="small"
              @click="handleToggleStatus(row)"
              v-if="!row.is_superuser"
            >
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-button
              link
              type="danger"
              size="small"
              @click="handleDelete(row)"
              v-if="!row.is_superuser"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="flex justify-end mt-4">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- 用户表单对话框 -->
    <UserFormDialog
      v-model:visible="dialogVisible"
      :user="currentUser"
      :role-options="roleOptions"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getUserList, deleteUser, updateUser, getRoleList, type User, type Role } from '@/api/user'
import UserFormDialog from './components/UserFormDialog.vue'
import { formatDateTime } from '@/utils/formatTime'
import { useUserStore } from '@/store/modules/user'

// 响应式数据
const loading = ref(false)
const userList = ref<User[]>([])
const roleOptions = ref<Role[]>([])
const dialogVisible = ref(false)
const currentUser = ref<User | null>(null)

// 搜索表单
const searchForm = reactive({
  search: '',
  is_active: undefined as boolean | undefined,
  role_name: ''
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 用户存储
const userStore = useUserStore()

// 获取用户列表
const fetchUserList = async () => {
  try {
    loading.value = true
    const params = {
      skip: (pagination.page - 1) * pagination.size,
      limit: pagination.size,
      ...searchForm
    }

    // 过滤掉undefined值
    Object.keys(params).forEach(key => {
      if (params[key] === undefined || params[key] === '') {
        delete params[key]
      }
    })

    const response = await getUserList(params)
    userList.value = response.data || []
    // 注意：实际项目中后端应该返回总数，这里先用列表长度模拟
    pagination.total = userList.value.length
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 获取角色列表
const fetchRoleList = async () => {
  try {
    const response = await getRoleList()
    roleOptions.value = response.data || []
  } catch (error) {
    console.error('获取角色列表失败:', error)
  }
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  fetchUserList()
}

// 重置搜索
const handleReset = () => {
  searchForm.search = ''
  searchForm.is_active = undefined
  searchForm.role_name = ''
  handleSearch()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.size = size
  fetchUserList()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchUserList()
}

// 创建用户
const handleCreate = () => {
  currentUser.value = null
  dialogVisible.value = true
}

// 编辑用户
const handleEdit = (user: User) => {
  currentUser.value = { ...user }
  dialogVisible.value = true
}

// 删除用户
const handleDelete = async (user: User) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${user.username}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteUser(user.id)
    ElMessage.success('删除成功')
    fetchUserList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error('删除用户失败')
    }
  }
}

// 切换用户状态
const handleToggleStatus = async (user: User) => {
  try {
    const action = user.is_active ? '禁用' : '启用'
    await ElMessageBox.confirm(
      `确定要${action}用户 "${user.username}" 吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await updateUser(user.id, { is_active: !user.is_active })
    ElMessage.success(`${action}成功`)
    fetchUserList()
  } catch (error) {
    if ((error as any) !== 'cancel') {
      const action = user.is_active ? '禁用' : '启用'
      console.error(`${action}用户失败:`, error)
      ElMessage.error(`${action}用户失败`)
    }
  }
}

// 表单成功回调
const handleFormSuccess = () => {
  dialogVisible.value = false
  fetchUserList()
}

// 获取角色显示名称
const getRoleDisplayName = (roleName: string) => {
  const role = roleOptions.value.find(r => r.name === roleName)
  return role?.description || roleName
}

// 生命周期
onMounted(() => {
  fetchUserList()
  fetchRoleList()
})
</script>

<style scoped>
.main-content {
  padding: 20px;
}

.el-tag {
  margin-right: 4px;
}

.el-tag:last-child {
  margin-right: 0;
}
</style>