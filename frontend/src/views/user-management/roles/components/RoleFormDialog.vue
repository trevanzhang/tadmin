<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑角色' : '新增角色'"
    width="500px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="80px"
      @submit.prevent
    >
      <el-form-item label="角色名称" prop="name">
        <el-input
          v-model="form.name"
          placeholder="请输入角色名称"
          :disabled="isEdit && isSystemRole(form.name)"
        />
        <div v-if="isEdit && isSystemRole(form.name)" class="text-gray-500 text-sm mt-1">
          系统角色名称不可修改
        </div>
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="form.description"
          placeholder="请输入角色描述"
          type="textarea"
          :rows="3"
        />
      </el-form-item>

      <el-form-item label="状态" prop="is_active">
        <el-switch
          v-model="form.is_active"
          active-text="启用"
          inactive-text="禁用"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button
        type="primary"
        :loading="submitting"
        @click="handleSubmit"
      >
        {{ isEdit ? '更新' : '创建' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { createRole, updateRole, type Role, type RoleCreate, type RoleUpdate } from '@/api/user'

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
  'success': []
}>()

// 响应式数据
const formRef = ref<FormInstance>()
const submitting = ref(false)

// 表单数据
const form = reactive<RoleCreate & RoleUpdate>({
  name: '',
  description: '',
  is_active: true
})

// 计算属性
const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const isEdit = computed(() => !!props.role)

// 系统角色名称（不可修改）
const systemRoles = ['super_admin', 'admin', 'user']

// 判断是否为系统角色
const isSystemRole = (roleName: string) => {
  return systemRoles.includes(roleName)
}

// 表单验证规则
const rules: FormRules = {
  name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '角色名称长度在 2 到 50 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '角色名称只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  description: [
    { max: 200, message: '描述长度不能超过200个字符', trigger: 'blur' }
  ]
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    name: '',
    description: '',
    is_active: true
  })
  formRef.value?.clearValidate()
}

// 初始化表单数据
const initForm = () => {
  if (props.role) {
    // 编辑模式
    Object.assign(form, {
      name: props.role.name,
      description: props.role.description || '',
      is_active: props.role.is_active
    })
  } else {
    // 新增模式
    resetForm()
  }
}

// 监听visible变化，初始化表单
watch(() => props.visible, (visible) => {
  if (visible) {
    initForm()
  }
})

// 监听role变化，更新表单
watch(() => props.role, () => {
  if (props.visible) {
    initForm()
  }
})

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false
  resetForm()
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    const valid = await formRef.value.validate()
    if (!valid) return

    submitting.value = true

    if (isEdit.value && props.role) {
      // 更新角色
      const updateData: RoleUpdate = {
        description: form.description,
        is_active: form.is_active
      }

      // 系统角色不能修改名称
      if (!isSystemRole(props.role.name)) {
        updateData.name = form.name
      }

      await updateRole(props.role.id, updateData)
      ElMessage.success('更新角色成功')
    } else {
      // 创建角色
      const createData: RoleCreate = {
        name: form.name,
        description: form.description || undefined,
        is_active: form.is_active
      }

      await createRole(createData)
      ElMessage.success('创建角色成功')
    }

    emit('success')
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error(isEdit.value ? '更新角色失败' : '创建角色失败')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.el-form {
  padding: 20px 0;
}
</style>