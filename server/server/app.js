const express = require("express");
const cors = require("cors");
const db = require("./db"); // 引入資料庫模組

const app = express();
app.use(cors());
app.use(express.json());

// 取得所有 serial_data 資料
app.get("/api/serial-data", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM public.serial_data ORDER BY id ASC");
    res.json(result.rows); // 返回查詢結果
  } catch (error) {
    console.error("Error fetching serial_data:", error);
    res.status(500).json({ error: "Server Error" });
  }
});

// 新增 serial_data 資料
// 新增 serial_data 資料
app.post("/api/serial-data", async (req, res) => {
  const {
    image,
    location,
    latitude,
    longitude,
    device_id,
    speed_limit,
    actual_speed,
    license_plate,
    error_code,
    resolved_timestamp,
    timestamp,
    status, // 新增 status 參數
  } = req.body;

  try {
    const result = await db.query(
      `INSERT INTO public.serial_data
       (image, location, latitude, longitude, device_id, speed_limit, actual_speed, license_plate, error_code, resolved_timestamp, timestamp, status)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12) RETURNING *`,
      [image, location, latitude, longitude, device_id, speed_limit, actual_speed, license_plate, error_code, resolved_timestamp, timestamp, status]
    );
    res.status(201).json(result.rows[0]); // 返回新增的資料
  } catch (error) {
    console.error("Error adding serial_data:", error);
    res.status(500).json({ error: "Server Error" });
  }
});


// 更新 serial_data 資料
app.put("/api/serial-data/:id", async (req, res) => {
  const { id } = req.params;
  const {
    image,
    location,
    latitude,
    longitude,
    device_id,
    speed_limit,
    actual_speed,
    license_plate,
    error_code,
    resolved_timestamp,
    timestamp,
    district,
    status, // 新增 status 欄位
  } = req.body;

  try {
    const result = await db.query(
      `UPDATE public.serial_data 
       SET image = $1, location = $2, latitude = $3, longitude = $4, device_id = $5, speed_limit = $6, actual_speed = $7,
           license_plate = $8, error_code = $9, resolved_timestamp = $10, timestamp = $11, district = $12, status = $13
       WHERE id = $14 RETURNING *`,
      [image, location, latitude, longitude, device_id, speed_limit, actual_speed, license_plate, error_code, resolved_timestamp, timestamp, district, status, id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Record not found" });
    }

    res.json(result.rows[0]); // 返回更新的資料
  } catch (error) {
    console.error("Error updating serial_data:", error);
    res.status(500).json({ error: "Server Error" });
  }
});

// 刪除 serial_data 資料
app.delete("/api/serial-data/:id", async (req, res) => {
  const { id } = req.params;

  try {
    const result = await db.query("DELETE FROM public.serial_data WHERE id = $1 RETURNING *", [id]);

    if (result.rows.length === 0) {
      return res.status(404).json({ error: "Record not found" });
    }

    res.json({ message: `Record with ID ${id} deleted successfully` });
  } catch (error) {
    console.error("Error deleting serial_data:", error);
    res.status(500).json({ error: "Server Error" });
  }
});

// 取得分類的 serial_data 資料（依據 status）
app.get("/api/serial-data/classified", async (req, res) => {
  try {
    const pendingResult = await db.query(
      "SELECT * FROM public.serial_data WHERE status = $1 ORDER BY id ASC",
      ["待處理"]
    );

    const processedResult = await db.query(
      "SELECT * FROM public.serial_data WHERE status = $1 ORDER BY id ASC",
      ["已處理"]
    );

    res.json({
      pending: pendingResult.rows, // 待處理資料
      processed: processedResult.rows, // 已處理資料
    });
  } catch (error) {
    console.error("Error fetching classified serial_data:", error);
    res.status(500).json({ error: "Server Error" });
  }
});


// 啟動伺服器
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
