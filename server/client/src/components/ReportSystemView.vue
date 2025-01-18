<template>
  <div class="report-system" :class="{ 'dark-mode': isDarkMode }">
    <div class="main-content">
      <!-- 報表標題：需要印出，所以不要加 no-print -->
      <h2 class="report-title">交通違規通知單</h2>

      <div class="content">
        <!-- 左側：詳細資料卡片 -->
        <div class="left-card card">
          <div class="info-grid">
            <p><strong>發單機關：</strong><span>台北市政府警察局</span></p>
            <p><strong>受處人：</strong><span>(依行為人)</span></p>
            <p><strong>車牌號碼：</strong><span>{{ $route.query.licensePlate }}</span></p>
            <p><strong>事由：</strong><span>{{ $route.query.violationItem }}</span></p>
            <p><strong>違規時間：</strong><span>{{ $route.query.timestamp }}</span></p>
            <p><strong>違規地點：</strong><span>{{ $route.query.address }}</span></p>
            <p><strong>罰鍰：</strong><span>400元</span></p>
          </div>
          <div class="notice">
            <strong>注意事項：</strong>
            <ol>
              <li>逾期未繳，將依法移送法務部行政執行署處理。</li>
              <li>請於期限內繳交罰鍰。</li>
            </ol>
          </div>
        </div>

        <!-- 右側：照片 + 按鈕 -->
        <div class="right-card card">
          <!-- 違規照片：調整大小避免撐壞版面 -->
          <div class="image-container">
            <img
              :src="$route.query.photo || '/images/test-plate.jpg'"
              alt="違規照片"
              class="violation-image"
            />
          </div>

          <!-- 按鈕區 -->
          <div class="button-group no-print">
            <button class="print-button" @click="handlePrint">列印通知單</button>
            <button class="done-button" @click="handleDone">完成</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ReportSystemView",
  props: {
    isDarkMode: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    // 列印功能
    handlePrint() {
      window.print();
    },
    // 完成後將該車牌移至 processed 並返回 /plates
    // handleDone() {
    //   const plateId = parseInt(this.$route.query.id, 10);
    //   if (!plateId) {
    //     this.$router.push("/plates");
    //     return;
    //   }
    //   const pending = JSON.parse(localStorage.getItem("pendingPlates")) || [];
    //   const processed = JSON.parse(localStorage.getItem("processedPlates")) || [];
    //   const idx = pending.findIndex(item => item.id === plateId);
    //   if (idx !== -1) {
    //     processed.push(pending[idx]);
    //     pending.splice(idx, 1);
    //     localStorage.setItem("pendingPlates", JSON.stringify(pending));
    //     localStorage.setItem("processedPlates", JSON.stringify(processed));
    //   }
    //   this.$router.push("/plates");
    // },
    // async handleDone() {
    //   const plateId = parseInt(this.$route.query.id, 10);
    //   if (!plateId) {
    //     this.$router.push("/plates");
    //     return;
    //   }

    //   try {
    //     // 發送 POST 請求將車牌移動到 "已處理"
    //     const response = await fetch("http://localhost:3000/api/move-to-processed", {
    //       method: "POST",
    //       headers: { "Content-Type": "application/json" },
    //       body: JSON.stringify({ id: plateId }),
    //     });

    //     if (!response.ok) {
    //       throw new Error("無法移動至已處理");
    //     }

    //     // 重新獲取數據，確保列表最新
    //     this.$emit("refreshData");
    //     this.$router.push("/plates");
    //   } catch (error) {
    //     console.error("更改處理狀態失敗：", error.message);
    //     alert("移動處理狀態失敗，請稍後重試。");
    //   }
    // },
    async handleDone() {
    const plateId = parseInt(this.$route.query.id, 10); // 獲取車牌 ID
    if (!plateId) {
      this.$router.push("/plates"); // 如果無效 ID，返回主頁
      return;
    }

    try {
      // 調用 API 更新 status 狀態
      const response = await fetch(`http://localhost:3000/api/serial-data/${plateId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          status: "已完成", // 更新狀態為 "已完成"
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to update status");
      }

      const updatedData = await response.json(); // 獲取後端返回的更新數據
      console.log("更新成功：", updatedData);

      // 更新成功後跳轉回車牌處理頁面
      this.$router.push("/plates");
    } catch (error) {
      console.error("Error updating status:", error);
      alert("更新失敗，請稍後再試。");
    }
    },
  },
};
</script>

<style src="../assets/styles/ReportSystemView.css"></style>

