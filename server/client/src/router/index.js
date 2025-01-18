import { createRouter, createWebHistory } from "vue-router";
import LoginView from "@/components/LoginView.vue";
import ManualRecognitionView from "@/components/ManualRecognitionView.vue";
import ReportSystemView from "@/components/ReportSystemView.vue";
import ProcessedPendingPlatesView from "@/components/ProcessedPendingPlatesView.vue";

const routes = [
  {
    path: "/",
    redirect: "/login"
  },
  {
    path: "/login",
    name: "LoginView",
    component: LoginView
  },
  {
    path: "/manual/:id",
    name: "ManualRecognitionView",
    component: ManualRecognitionView,
    props: true
  },
  {
    path: "/report",
    name: "ReportSystemView",
    component: ReportSystemView
  },
  {
    path: "/plates",
    name: "ProcessedPendingPlatesView",
    component: ProcessedPendingPlatesView
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;