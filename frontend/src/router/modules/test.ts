import { $t } from "@/plugins/i18n";
const Layout = () => import("@/layout/index.vue");

export default {
  path: "/test",
  name: "Test",
  component: Layout,
  redirect: "/test/page",
  meta: {
    icon: "ep:document",
    title: "测试页面",
    rank: 20
  },
  children: [
    {
      path: "/test/page",
      name: "TestPage",
      component: () => import("@/views/test-page.vue"),
      meta: {
        title: "测试页面"
      }
    }
  ]
} satisfies RouteConfigsTable;