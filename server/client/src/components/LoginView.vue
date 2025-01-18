<template>
  <div class="login-container" :class="{ 'dark-mode': isDarkMode }">
    <div class="login-card">
      <h2>登入人工辨識系統</h2>

      <div class="form-group">
        <label for="username">帳號:</label>
        <input
          id="username"
          v-model="username"
          type="text"
          placeholder="請輸入帳號"
          @keyup.enter="handleLogin"
          class="full-width-input"
        />
        <span v-if="errors.username" class="error-message">{{ errors.username }}</span>
      </div>

      <div class="form-group">
        <label for="password">密碼:</label>
        <input
          id="password"
          v-model="password"
          type="password"
          placeholder="請輸入密碼"
          @keyup.enter="handleLogin"
          class="full-width-input"
        />
        <span v-if="errors.password" class="error-message">{{ errors.password }}</span>
      </div>

      <button @click="handleLogin" :disabled="isLoading" class="login-btn">
        {{ isLoading ? '登入中...' : '登入' }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginView",
  props: {
    isDarkMode: { type: Boolean, default: false },
  },
  data() {
    return {
      username: "",
      password: "",
      isLoading: false,
      errors: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    validateForm() {
      let isValid = true;
      this.errors = { username: "", password: "" };
      if (!this.username.trim()) {
        this.errors.username = "請輸入帳號";
        isValid = false;
      }
      if (!this.password.trim()) {
        this.errors.password = "請輸入密碼";
        isValid = false;
      }
      return isValid;
    },
    async handleLogin() {
      if (!this.validateForm()) return;

      this.isLoading = true;
      try {
        // 模擬 API 請求
        await new Promise((resolve) => setTimeout(resolve, 800));

        // 驗證帳密
        if (this.username === "admin" && this.password === "password") {
          localStorage.setItem("isLoggedIn", "true");
          this.$router.push("/plates");
        } else {
          throw new Error("帳號或密碼錯誤");
        }
      } catch (error) {
        alert(error.message);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #ffffff;
  color: #333333;
  font-family: 'Arial', sans-serif;
}

.dark-mode {
  background: #333333;
  color: #ffffff;
}

.login-card {
  background: #ffffff;
  padding: 40px;
  width: 400px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  text-align: center;
  color: #333333;
}

.dark-mode .login-card {
  background: #444444;
  color: #ffffff;
}

.login-card h2 {
  margin-bottom: 24px;
  font-size: 28px;
  font-weight: bold;
  color: inherit;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  font-size: 14px;
  margin-bottom: 6px;
  display: block;
  color: inherit;
}

.full-width-input {
  width: 100%;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  color: #333333;
  background: #ffffff;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.dark-mode .full-width-input {
  background: #555555;
  color: #ffffff;
  border: 1px solid #666666;
}

.full-width-input:focus {
  outline: none;
  border-color: #2828FF;
  box-shadow: 0 0 8px rgba(40, 40, 255, 0.2);
}

.login-btn {
  width: 100%;
  padding: 14px;
  background: #2828FF;
  border: none;
  border-radius: 8px;
  color: #ffffff;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover {
  background: #1f1fbf;
}

.login-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 4px;
}
</style>
