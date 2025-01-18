<template>
  <div class="cases-page">
    <!-- 左側邊欄 -->
    <aside class="sidebar">
      <ul class="status-list">
        <li class="status-item" v-for="(count, status, ) in caseStatusCounts" :key="status">
          <div class="status-card">
            <div class="status-icon-container">{{ statusIcons[status] }}</div>
            <div class="status-content">
              <div class="status-title">{{ status }}</div>
              <div class="status-count">{{ count }}</div>
            </div>
          </div>
        </li>
      </ul>
      <div class="quick-access">
        <button @click="filterTodayCases" class="quick-btn">今日案件</button>
        <button class="quick-btn" disabled>異常案件</button>
        <button class="quick-btn" disabled>緊急處理</button>
      </div>
    </aside>

    <!-- 案件主頁面 -->
    <main>
      <div class="header">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="搜尋案件編號或關鍵字..."
          class="search-input"
        />
        <!-- 篩選欄目按鈕 -->
        <!-- <div class="filter-buttons">
          <button
            v-for="(value, key) in caseList[0]"
            :key="key"
            @click="toggleActive($event.target); selectFilter({ field: key, value: null })"
            class="filter-btn"
          >
          {{ key }}
          </button>
        </div>
        <button @click="clearFilter" class="clear-btn">清除篩選</button> -->
      </div>

      <section class="case-list-section">
        <h2 class="section-title">案件列表</h2>
        <table class="case-table">
          <thead>
            <tr>
              <th>案件編號</th>
              <th>拍攝時間</th>
              <th>地點</th>
              <th>限速</th>
              <th>車速</th>
              <th>狀態</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            
            <tr v-for="caseItem in paginatedCases" :key="caseItem.id">
              <td>#{{ caseItem.id }}</td>
              <td>{{ caseItem.timestamp }}</td>
              <td>{{ caseItem.location }}</td>
              <td>{{ caseItem.道路速限 }}km/h</td>  
              <td>{{ caseItem.車輛時速 }}km/h</td>
              <td><span class="status-badge">{{ caseItem.status }}</span></td>
              <td>
                <button class="process-btn" @click="processCase(caseItem)">處理</button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 分頁控制 -->
        <div class="pagination">
          <button @click="goToPage(currentPage - 1)" :disabled="currentPage === 1">
            &lt;
          </button>
          <span>頁面 {{ currentPage }} / {{ totalPages }}</span>
          <button @click="goToPage(currentPage + 1)" :disabled="currentPage === totalPages">
            &gt;
          </button>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
      caseList: [],
      caseStatusCounts: {},
      currentPage: 1,
      itemsPerPage: 6,
      selectedFilter: null, // 新增篩選條件
    };
  },
  computed: {
    // 動態篩選過的資料，基於使用者選擇的篩選條件與搜尋欄內容
    filteredCases() {
    return this.caseList.filter((item) => {
      // 如果選擇了篩選欄目，匹配相應的值；否則顯示全部
      const matchesFilter =
        !this.selectedFilter || 
        (this.selectedFilter.value === null || 
         item[this.selectedFilter.field]?.toString().includes(this.selectedFilter.value));
      // 搜尋條件過濾
      const matchesQuery =
        !this.searchQuery ||
        Object.values(item)
          .join(" ")
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());
      return matchesFilter && matchesQuery;
    });
    },
    availableFilters() {
    // 動態生成可用的篩選項目
    const fields = ["status", "道路速限", "車輛時速"];
    return fields.flatMap((field) =>
      [...new Set(this.caseList.map((item) => item[field]))].map((value) => ({
        field,
        value,
        }))
      );
    },

    paginatedCases() {
    const start = (this.currentPage - 1) * this.itemsPerPage;
    return this.filteredCases.slice(start, start + this.itemsPerPage);
    },
    totalPages() {
      return Math.ceil(this.filteredCases.length / this.itemsPerPage);
    },
    statusIcons() {
      return {
        "待處理": "🕥",
        "處理中": "⚙️",
        "已完成": "✔️",
        "今日拍攝": "📷",
      };
    },
  },
  methods: {
    toggleActive(button) {
    button.classList.toggle("active");
    },
    filterTodayCases() {
      this.searchQuery = "今日拍攝";
    },
    processCase(caseItem) {
      this.$router.push({ name: "ManualRecognitionView", params: { id: caseItem.id } });
    },
    goToPage(page) {
      if (page > 0 && page <= this.totalPages) {
        this.currentPage = page;
      }
    },
    filterCases(status) {
    this.selectedFilter = status; // 設定篩選條件
    this.currentPage = 1; // 篩選後重置頁數
    },
    selectFilter(filter) {
    this.selectedFilter = filter; // 設定目前選擇的欄目
    this.currentPage = 1; // 回到第一頁
    },
    clearFilter() {
      this.selectedFilter = null; // 清除篩選
      this.searchQuery = ""; // 清空搜尋內容
      this.currentPage = 1; // 重置頁面
      // 移除所有 filter-btn 的 active 樣式
      const buttons = document.querySelectorAll(".filter-btn");
      buttons.forEach((button) => button.classList.remove("active"));
    },// 清除篩選條件
    updateCaseStatusCounts() {
      this.caseStatusCounts = this.caseList.reduce((counts, item) => {
        counts[item.status] = (counts[item.status] || 0) + 1;
        return counts;
      }, {});
    },
  },
  async mounted() {
    try {
      const response = await fetch("http://localhost:3000/api/serial-data");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      this.caseList = await response.json();
      this.updateCaseStatusCounts();
    } catch (error) {
      console.error("Error fetching data:", error.message);
    }
  },
};
</script>

<style>
/* 簡潔現代的 CSS */
/* 重設 CSS 確保一致性 */
/* 全局樣式重設 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Roboto', sans-serif;
  background-color: #eef2f7;
  color: #333;
  line-height: 1.6;
  overflow: hidden; /* 防止整體頁面滾動 */
}

.cases-page {
  display: flex;
  height: 90vh;
  overflow: hidden;
}

/* 左側邊欄樣式 */
.sidebar {
  width: 300px;
  background: linear-gradient(135deg, #1e3a8a, #3b82f6);
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
  list-style: none;
}

.status-item {
  display: flex;
  justify-content: center;
}

.status-card {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  color: #1e3a8a;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.status-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.quick-access {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 10px; /* 新增按鈕之間的間距 */
}

.quick-btn {
  width: 100%;
  background-color: #34d399;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
  margin: 0; /* 清除內建的間距，避免影響佈局 */
}

.quick-btn:hover {
  background-color: #10b981;
}

.quick-btn:disabled {
  background-color: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
}

/* 主頁面樣式 */
main {
  flex: 1;
  padding: 30px;
  overflow: hidden; /* 防止主頁面滾動 */
}

.header {
  display: flex;
  flex-direction: column; /* 讓搜尋欄與按鈕堆疊 */
  gap: 15px;
  margin-bottom: 30px;
}

.search-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-btn {
  padding: 12px 20px;
  background: #f59e0b;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.filter-btn:hover {
  background: #d97706;
}

.clear-btn {
  padding: 12px 20px;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.clear-btn:hover {
  background: #dc2626;
}

.case-list-section {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  height: calc(100vh - 150px); /* 動態調整高度以防滾動 */
  overflow-y: auto;
}

.case-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.case-table th,
.case-table td {
  padding: 15px;
  border-bottom: 1px solid #e5e7eb;
  text-align: left;
}

.case-table th {
  background-color: #f3f4f6;
  font-weight: bold;
  color: #1f2937;
}

.status-badge {
  display: inline-block;
  background-color: #3b82f6; /* 預設狀態顏色 */
  color: white;
  padding: 5px 15px;
  border-radius: 50px;
  font-size: 14px;
}

/* 將"已完成"的狀態背景改為綠色 */
.status-badge:contains("已完成") {
  background-color: #10b981; /* 綠色背景 */
}

/* 將"待處理"的狀態背景保持藍色 */
.status-badge:contains("待處理") {
  background-color: #3b82f6; /* 藍色背景 */
}

.view-btn {
  padding: 8px 15px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
  background: #60a5fa; /* 預設藍色背景 */
  color: white;
}

.view-btn:hover {
  background: #3b82f6; /* 藍色變深 */
}

.process-btn {
  padding: 8px 15px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s ease;
  background: #fbbf24; /* 黃色背景 */
  color: white;
  margin-left: 10px;
}

.process-btn:hover {
  background: #f59e0b; /* 深黃色背景 */
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.pagination button {
  background: #e5e7eb;
  border: none;
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  margin: 0 5px;
  transition: background 0.3s ease;
}

.pagination button:hover {
  background: #9ca3af;
  color: white;
}

.pagination button:disabled {
  background: #f3f4f6;
  color: #9ca3af;
  cursor: not-allowed;
}

.case-table td {
    background-color: #4a5568; /* 深色表頭背景 */
    color: #edf2f7; /* 表頭文字顏色 */
  }

/* 深色模式樣式 */
@media (prefers-color-scheme: dark) {
  body {
    background-color: #1a202c; /* 深色背景 */
    color: #e2e8f0; /* 字體顏色 */
  }

  .case-list-section {
    background-color: #2d3748; /* 深色卡片背景 */
    color: #e2e8f0; /* 深色文字 */
  }
  .case-table td {
    background-color: #4a5568; /* 深色表頭背景 */
    color: #edf2f7; /* 表頭文字顏色 */
  }

  .case-table th {
    background-color: #4a5568; /* 深色表頭背景 */
    color: #edf2f7; /* 表頭文字顏色 */
  }

  .case-table th {
    background-color: #4a5568; /* 深色表頭背景 */
    color: #edf2f7; /* 表頭文字顏色 */
  }

  .case-table td {
    border-bottom: 1px solid #4a5568; /* 深色分隔線 */
  }

  .status-badge {
    color: white; /* 狀態字體顏色 */
  }

  /* 狀態按鈕顏色保持不變 */
  .status-badge:contains("已完成") {
    background-color: #10b981; /* 綠色背景 */
  }

  .status-badge:contains("待處理") {
    background-color: #3b82f6; /* 藍色背景 */
  }

  .filter-btn {
    background: #f59e0b; /* 篩選按鈕 */
    color: white;
  }

  .filter-btn:hover {
    background: #d97706; /* 深色按鈕 hover */
  }

  .clear-btn {
    background: #ef4444; /* 清除按鈕 */
  }

  .clear-btn:hover {
    background: #dc2626; /* 清除按鈕 hover */
  }
}
</style>