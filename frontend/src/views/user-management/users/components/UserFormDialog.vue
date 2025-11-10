<template>
  <el-dialog
    v-model="dialogVisible"
    :title="isEdit ? '编辑用户' : '新增用户'"
    width="600px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="80px"
      @submit.prevent
    >
      <el-form-item label="用户名" prop="username">
        <el-input
          v-model="form.username"
          placeholder="请输入用户名"
          :disabled="isEdit"
        />
      </el-form-item>

      <el-form-item label="邮箱" prop="email">
        <el-input
          v-model="form.email"
          placeholder="请输入邮箱"
          type="email"
        />
      </el-form-item>

      <el-form-item v-if="!isEdit" label="密码" prop="password">
        <el-input
          v-model="form.password"
          placeholder="请输入密码"
          type="password"
          show-password
        />
      </el-form-item>

      <el-form-item label="姓名" prop="full_name">
        <el-input
          v-model="form.full_name"
          placeholder="请输入姓名"
        />
      </el-form-item>

      <el-form-item label="角色" prop="role_ids">
        <el-select
          v-model="form.role_ids"
          placeholder="请选择角色"
          multiple
          style="width: 100%"
        >
          <el-option
            v-for="role in roleOptions"
            :key="role.id"
            :label="role.description || role.name"
            :value="role.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item v-if="isEdit" label="状态">
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
import { createUser, updateUser, type User, type UserCreate, type UserUpdate, type Role } from '@/api/user'

// Props
interface Props {
  visible: boolean
  user?: User | null
  roleOptions: Role[]
}

const props = withDefaults(defineProps<Props>(), {
  user: null,
  roleOptions: () => []
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
const form = reactive<UserCreate & UserUpdate>({
  username: '',
  email: '',
  password: '',
  full_name: '',
  is_active: true,
  role_ids: []
})

// 计算属性
const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const isEdit = computed(() => !!props.user)

// 表单验证规则
const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    {
      required: !isEdit.value,
      validator: (rule, value, callback) => {
        if (!isEdit.value && !value) {
          callback(new Error('请输入密码'))
        } else if (value && value.length < 6) {
          callback(new Error('密码长度不能少于6位'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  full_name: [
    { max: 50, message: '姓名长度不能超过50个字符', trigger: 'blur' }
  ],
  role_ids: [
    { required: true, message: '请选择至少一个角色', trigger: 'change' }
  ]
}

// 重置表单
const resetForm = () => {
  Object.assign(form, {
    username: '',
    email: '',
    password: '',
    full_name: '',
    is_active: true,
    role_ids: []
  })
  formRef.value?.clearValidate()
}

// 初始化表单数据
const initForm = () => {
  if (props.user) {
    // 编辑模式
    Object.assign(form, {
      username: props.user.username,
      email: props.user.email,
      full_name: props.user.full_name || '',
      is_active: props.user.is_active,
      role_ids: [] // 这里需要根据用户角色ID来设置，暂时为空
    })
    // TODO: 需要根据用户的role_names获取对应的role_ids
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

// 监听user变化，更新表单
watch(() => props.user, () => {
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

    if (isEdit.value && props.user) {
      // 更新用户
      const updateData: UserUpdate = {
        email: form.email,
        full_name: form.full_name,
        is_active: form.is_active,
        role_ids: form.role_ids
      }

      // 如果填写了新密码，则包含密码字段
      if (form.password) {
        updateData.password = form.password
      }

      await updateUser(props.user.id, updateData)
      ElMessage.success('更新用户成功')
    } else {
      // 创建用户
      const createData: UserCreate = {
        username: form.username,
        email: form.email,
        password: form.password!,
        full_name: form.full_name || undefined
      }

      await createUser(createData)

      // 创建成功后分配角色
      if (form.role_ids.length > 0) {
        // 这里需要等待用户创建成功获取ID后再分配角色
        // 简化处理，实际项目中可能需要更复杂的逻辑
        const newUserResponse = await createUser(createData)
        if (newUserResponse.data?.id) {
          await updateUser(newUserResponse.data.id, { role_ids: form.role_ids })
        }
      }

      ElMessage.success('创建用户成功')
    }

    emit('success')
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error(isEdit.value ? '更新用户失败' : '创建用户失败')
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