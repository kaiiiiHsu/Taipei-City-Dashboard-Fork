<template>
  <!-- 透過 :class 綁定 dark-mode -->
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <!-- 將 isDarkMode 傳給 NavBar，讓 NavBar 也知道狀態 -->
    <NavBar :isDarkMode="isDarkMode" @toggle-theme="toggleDarkMode" />

    <!-- 將 isDarkMode 傳給 router-view 內頁 -->
    <router-view :isDarkMode="isDarkMode" />
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
export default {
  name: "App",
  components: {
    NavBar,
  },
  data() {
    return {
      isDarkMode: false,
    };
  },
  methods: {
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem("darkMode", this.isDarkMode);
    },
  },
  mounted() {
    const darkPref = localStorage.getItem("darkMode");
    if (darkPref === "true") {
      this.isDarkMode = true;
    }
  },
};
</script>

<style src="./assets/styles/App.css"></style>
