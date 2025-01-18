<template>
  <div class="manual-recognition" :class="{ 'dark-mode': isDarkMode }">
    <!-- 左側面板：顯示無法辨識的照片 -->
    <div class="left-panel">
      <div class="panel-content">
        <h2>無法辨識的車牌</h2>
        <div class="image-container">
          <!-- 這裡顯示照片。若沒有就用預設圖 -->
          <img :src="photo" alt="無法辨識的照片" class="photo" />
        </div>
      </div>
    </div>

    <!-- 右側面板：人工輸入表單 -->
    <div class="right-panel">
      <div class="panel-content">
        <h2>人工辨識輸入</h2>

        <!-- 違規資訊 -->
        <div class="info-group">
          <p><strong>拍攝時間:</strong> {{ timestamp }}</p>
          <p><strong>違規流水號:</strong> {{ violationId }}</p>
          <p><strong>拍攝地點:</strong> {{ address }}</p>
        </div>

        <!-- 違規項目選擇 -->
        <div class="form-group">
          <label for="violation-item">違規項目:</label>
          <select
            id="violation-item"
            v-model="violationItem"
            class="form-control"
          >
            <option disabled value="">請選擇違規項目</option>
            <option>超速</option>
            <option>闖紅燈</option>
            <option>違規停車</option>
            <option>未繫安全帶</option>
          </select>
        </div>

        <!-- 車牌輸入框 -->
        <div class="form-group">
          <label for="license-plate">人工輸入車牌:</label>
          <input
            type="text"
            id="license-plate"
            v-model="manualInput"
            placeholder="請輸入車牌號碼"
            class="form-control"
          />
        </div>

        <!-- Checkbox 群組 -->
        <div class="checkbox-group">
          <label>
            <input type="checkbox" v-model="unableToRecognize" />
            人工無法辨識
          </label>
          <label>
            <input type="checkbox" v-model="multiplePlates" />
            多車牌選項
          </label>
        </div>

        <!-- 提交按鈕 -->
        <button
          :disabled="!canSubmit"
          @click="submitRecognition"
          class="submit-btn"
        >
          提交
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ManualRecognitionView",
  props: {
    isDarkMode: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      photo: this.$route.query.image || "/images/default-plate.jpg",
      timestamp: this.$route.query.timestamp || "未知時間",
      violationId: this.$route.query.violationId || "未知編號",
      address: this.$route.query.location || "未知地點",

      violationItem: "",
      manualInput: "",
      unableToRecognize: false,
      multiplePlates: false,
    };
  },
  computed: {
    canSubmit() {
      const hasPlateInput =
        this.unableToRecognize ||
        this.multiplePlates ||
        this.manualInput.trim() !== "";
      return this.violationItem && hasPlateInput;
    },
  },
  methods: {
    submitRecognition() {
      const result = {
        id: this.$route.params.id,
        licensePlate: this.getDisplayedPlate(),
        violationItem: this.violationItem,
        timestamp: this.timestamp,
        violationId: this.violationId,
        address: this.address,
        photo: this.photo,
      };
      this.$router.push({ name: "ReportSystemView", query: result });
    },
    getDisplayedPlate() {
      if (this.unableToRecognize) return "人工無法辨識";
      if (this.multiplePlates) return "多車牌";
      return this.manualInput || "未知車牌";
    },
  },
};
</script>

<style src="../assets/styles/ManualRecognitionView.css"></style>
