import { http } from "@/utils/http";

export type UserResult = {
  success: boolean;
  data: {
    /** 头像 */
    avatar: string;
    /** 用户名 */
    username: string;
    /** 昵称 */
    nickname: string;
    /** 当前登录用户的角色 */
    roles: Array<string>;
    /** 按钮级别权限 */
    permissions: Array<string>;
    /** `token` */
    accessToken: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refreshToken: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

export type RefreshTokenResult = {
  success: boolean;
  data: {
    /** `token` */
    accessToken: string;
    /** 用于调用刷新`accessToken`的接口时所需的`token` */
    refreshToken: string;
    /** `accessToken`的过期时间（格式'xxxx/xx/xx xx:xx:xx'） */
    expires: Date;
  };
};

// 用户管理相关类型定义
export interface User {
  id: number;
  username: string;
  email: string;
  full_name: string | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at: string;
  role_names: string[];
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface UserUpdate {
  username?: string;
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  role_ids?: number[];
}

export interface UserListParams {
  skip?: number;
  limit?: number;
  search?: string;
  is_active?: boolean;
  role_name?: string;
}

export interface Role {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface RoleCreate {
  name: string;
  description?: string;
  is_active?: boolean;
}

export interface RoleUpdate {
  name?: string;
  description?: string;
  is_active?: boolean;
}

export interface UserRoleAssign {
  user_id: number;
  role_ids: number[];
}

// API 函数定义
/** 登录 */
export const getLogin = (data?: object) => {
  return http.request<UserResult>("post", "/auth/sessions", { data });
};

/** 刷新`token` */
export const refreshTokenApi = (data?: object) => {
  return http.request<RefreshTokenResult>("post", "/auth/refresh-token", { data });
};

/** 获取用户列表 */
export const getUserList = (params?: UserListParams) => {
  return http.request<{ data: User[] }>("get", "/users/", { params });
};

/** 创建用户 */
export const createUser = (data: UserCreate) => {
  return http.request<{ data: User }>("post", "/users/", { data });
};

/** 获取用户详情 */
export const getUserDetail = (id: number) => {
  return http.request<{ data: User }>("get", `/users/${id}`);
};

/** 更新用户 */
export const updateUser = (id: number, data: UserUpdate) => {
  return http.request<{ data: User }>("put", `/users/${id}`, { data });
};

/** 删除用户 */
export const deleteUser = (id: number) => {
  return http.request("delete", `/users/${id}`);
};

/** 获取角色列表 */
export const getRoleList = (params?: { skip?: number; limit?: number; search?: string; is_active?: boolean }) => {
  return http.request<{ data: Role[] }>("get", "/roles/", { params });
};

/** 创建角色 */
export const createRole = (data: RoleCreate) => {
  return http.request<{ data: Role }>("post", "/roles/", { data });
};

/** 获取角色详情 */
export const getRoleDetail = (id: number) => {
  return http.request<{ data: Role }>("get", `/roles/${id}`);
};

/** 更新角色 */
export const updateRole = (id: number, data: RoleUpdate) => {
  return http.request<{ data: Role }>("put", `/roles/${id}`, { data });
};

/** 删除角色 */
export const deleteRole = (id: number) => {
  return http.request("delete", `/roles/${id}`);
};

/** 分配用户角色 */
export const assignUserRoles = (data: UserRoleAssign) => {
  return http.request("post", "/roles/assign", { data });
};

/** 获取角色下的用户列表 */
export const getRoleUsers = (roleId: number, params?: { skip?: number; limit?: number }) => {
  return http.request<{ data: any[] }>("get", `/roles/${roleId}/users`, { params });
};
