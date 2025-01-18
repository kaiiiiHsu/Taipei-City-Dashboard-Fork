const { Pool } = require("pg");
require("dotenv").config(); // 加載 .env 文件

const db = new Pool({
  host: process.env.DB_DASHBOARD_HOST, // 資料庫主機
  user: process.env.DB_DASHBOARD_USER, // 資料庫使用者
  password: process.env.DB_DASHBOARD_PASSWORD, // 資料庫密碼
  database: process.env.DB_DASHBOARD_DBNAME, // 資料庫名稱
  port: process.env.DB_DASHBOARD_PORT, // 資料庫埠號
});

// 測試資料庫連線
db.connect((err) => {
  if (err) {
    console.error("資料庫連線失敗：", err.stack);
  } else {
    console.log("資料庫連線成功");
  }
});

module.exports = db;
