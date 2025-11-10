<template>
  <div class="main-content">
    <!-- 页面标题和操作按钮 -->
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">角色管理</h1>
      <el-button
        type="primary"
        :icon="Plus"
        @click="handleCreate"
      >
        新增角色
      </el-button>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="mb-6" shadow="never">
      <el-form :model="searchForm" inline>
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="角色名称或描述"
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
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 角色列表 -->
    <el-card shadow="never">
      <el-table
        v-loading="loading"
        :data="roleList"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" min-width="150" />
        <el-table-column prop="description" label="描述" min-width="200">
          <template #default="{ row }">
            {{ row.description || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="updated_at" label="更新时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              link
              type="primary"
              size="small"
              @click="handleViewUsers(row)"
            >
              查看用户
            </el-button>
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
            >
              {{ row.is_active ? '禁用' : '启用' }}
            </el-button>
            <el-button
              link
              type="danger"
              size="small"
              @click="handleDelete(row)"
              v-if="!isSystemRole(row.name)"
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

    <!-- 角色表单对话框 -->
    <RoleFormDialog
      v-model:visible="dialogVisible"
      :role="currentRole"
      @success="handleFormSuccess"
    />

    <!-- 角色用户对话框 -->
    <RoleUsersDialog
      v-model:visible="usersDialogVisible"
      :role="currentRole"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getRoleList, deleteRole, updateRole, type Role } from '@/api/user'
import RoleFormDialog from './components/RoleFormDialog.vue'
import RoleUsersDialog from './components/RoleUsersDialog.vue'
import { formatDateTime } from '@/utils/formatTime'

// 响应式数据
const loading = ref(false)
const roleList = ref<Role[]>([])
const dialogVisible = ref(false)
const usersDialogVisible = ref(false)
const currentRole = ref<Role | null>(null)

// 搜索表单
const searchForm = reactive({
  search: '',
  is_active: undefined as boolean | undefined
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 系统角色名称（不能删除）
const systemRoles = ['super_admin', 'admin', 'user']

// 判断是否为系统角色
const isSystemRole = (roleName: string) => {
  return systemRoles.includes(roleName)
}

// 获取角色列表
const fetchRoleList = async () => {
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

    const response = await getRoleList(params)
    roleList.value = response.data || []
    // 注意：实际项目中后端应该返回总数，这里先用列表长度模拟
    pagination.total = roleList.value.length
  } catch (error) {
    console.error('获取角色列表失败:', error)
    ElMessage.error('获取角色列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  pagination.page = 1
  fetchRoleList()
}

// 重置搜索
const handleReset = () => {
  searchForm.search = ''
  searchForm.is_active = undefined
  handleSearch()
}

// 分页处理
const handleSizeChange = (size: number) => {
  pagination.size = size
  fetchRoleList()
}

const handleCurrentChange = (page: number) => {
  pagination.page = page
  fetchRoleList()
}

// 创建角色
const handleCreate = () => {
  currentRole.value = null
  dialogVisible.value = true
}

// 编辑角色
const handleEdit = (role: Role) => {
  currentRole.value = { ...role }
  dialogVisible.value = true
}

// 查看角色用户
const handleViewUsers = (role: Role) => {
  currentRole.value = role
  usersDialogVisible.value = true
}

// 删除角色
const handleDelete = async (role: Role) => {
  if (isSystemRole(role.name)) {
    ElMessage.warning('系统角色不能删除')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确定要删除角色 "${role.name}" 吗？此操作不可恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteRole(role.id)
    ElMessage.success('删除成功')
    fetchRoleList()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除角色失败:', error)
      ElMessage.error('删除角色失败')
    }
  }
}

// 切换角色状态
const handleToggleStatus = async (role: Role) => {
  try {
    const action = role.is_active ? '禁用' : '启用'
    await ElMessageBox.confirm(
      `确定要${action}角色 "${role.name}" 吗？`,
      `确认${action}`,
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await updateRole(role.id, { is_active: !role.is_active })
    ElMessage.success(`${action}成功`)
    fetchRoleList()
  } catch (error) {
    if ((error as any) !== 'cancel') {
      const action = role.is_active ? '禁用' : '启用'
      console.error(`${action}角色失败:`, error)
      ElMessage.error(`${action}角色失败`)
    }
  }
}

// 表单成功回调
const handleFormSuccess = () => {
  dialogVisible.value = false
  fetchRoleList()
}

// 生命周期
onMounted(() => {
  fetchRoleList()
})
</script>

<style scoped>
.main-content {
  padding: 20px;
}
</style>