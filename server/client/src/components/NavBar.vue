<template>
  <nav class="navbar" :class="{ 'dark-mode': isDarkMode }">
    <div class="nav-content">
      <!-- 左側系統名稱 -->
      <router-link to="/" class="nav-brand">人工辨識系統</router-link>

      <!-- 處理車牌按鈕：在 /login 時不顯示 -->
      <router-link
        v-if="$route.path !== '/login'"
        to="/plates"
        class="plates-link"
      >
        處理車牌
      </router-link>

      <!-- 右側按鈕區 -->
      <div class="nav-items">
        <!-- 深色/淺色模式切換按鈕 -->
        <button @click="$emit('toggle-theme')" class="theme-toggle" :class="{ 'dark-mode': isDarkMode }">
          <span v-if="isDarkMode">⭐</span>
          <span v-else>☀️</span>
        </button>

        <!-- 登出按鈕：同樣在 /login 時隱藏 -->
        <button
          v-if="$route.path !== '/login'"
          @click="handleLogout"
          class="logout-btn"
        >
          登出
        </button>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  props: {
    isDarkMode: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    handleLogout() {
      localStorage.removeItem("isLoggedIn");
      this.$router.push("/login");
    },
  },
};
</script>

<!-- 匯入外部 CSS (NavBar.css) -->
<style src="../assets/styles/NavBar.css"></style>
