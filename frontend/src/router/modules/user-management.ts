import { $t } from "@/plugins/i18n";
const Layout = () => import("@/layout/index.vue");

export default {
  path: "/user-management",
  name: "UserManagement",
  component: Layout,
  redirect: "/user-management/users",
  meta: {
    icon: "ep:user",
    title: $t("menus.userManagement"),
    rank: 10
  },
  children: [
    {
      path: "/user-management/users",
      name: "UserList",
      component: () => import("@/views/user-management/simple-users.vue"),
      meta: {
        title: $t("menus.userList"),
        roles: ["admin", "super_admin", "user"]
      }
    },
    {
      path: "/user-management/roles",
      name: "RoleList",
      component: () => import("@/views/user-management/roles/index.vue"),
      meta: {
        title: $t("menus.roleList"),
        roles: ["admin", "super_admin", "user"]
      }
    }
  ]
} satisfies RouteConfigsTable;