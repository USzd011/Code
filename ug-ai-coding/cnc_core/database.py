"""SQLite 数据库层"""
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

DB_DIR = Path(__file__).parent.parent / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "cnc_program.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """初始化数据库表"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        hardness REAL,
        thermal_conductivity REAL,
        max_cutting_speed REAL
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS tools (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        diameter REAL,
        flute_length REAL,
        material TEXT,
        coating TEXT,
        max_rpm INTEGER,
        max_feed REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS process_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        part_name TEXT,
        material TEXT,
        tool_list TEXT,
        parameters TEXT,
        gcode TEXT,
        status TEXT DEFAULT 'draft',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS machining_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id INTEGER,
        actual_time REAL,
        actual_cost REAL,
        quality_score REAL,
        issues TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (plan_id) REFERENCES process_plans(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS operation_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # 插入默认材料
    default_materials = [
        ("Q235碳钢", 120, 52, 200), ("45号钢", 180, 45, 180),
        ("40Cr合金钢", 250, 42, 150), ("40CrNiMo", 280, 40, 140),
        ("Cr12MoV冷作模具钢", 580, 25, 100), ("H13热作模具钢", 520, 28, 110),
        ("40CrMo", 260, 41, 145), ("20CrMo", 200, 44, 170),
        ("TC4钛合金", 330, 6.7, 60), ("Inconel718高温合金", 350, 11, 45),
        ("AL6061铝合金", 90, 167, 500), ("AL7075铝合金", 120, 130, 450),
        ("紫铜C110", 80, 385, 400), ("POM聚甲醛", 70, 0.3, 600),
    ]
    
    c.executemany('''INSERT OR IGNORE INTO materials (name, hardness, thermal_conductivity, max_cutting_speed)
                     VALUES (?, ?, ?, ?)''', default_materials)
    
    conn.commit()
    conn.close()
    return DB_PATH

def save_process_plan(part_name: str, material: str, tool_list: list,
                      parameters: dict, gcode: str) -> int:
    """保存工艺方案"""
    conn = get_connection()
    c = conn.cursor()
    import json
    c.execute('''INSERT INTO process_plans (part_name, material, tool_list, parameters, gcode)
                 VALUES (?, ?, ?, ?, ?)''',
              (part_name, material, json.dumps(tool_list), json.dumps(parameters), gcode))
    plan_id = c.lastrowid
    conn.commit()
    conn.close()
    return plan_id

def get_process_plan(plan_id: int) -> Optional[Dict]:
    """获取工艺方案"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM process_plans WHERE id=?", (plan_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

def get_all_plans() -> List[Dict]:
    """获取所有工艺方案"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM process_plans ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def log_operation(user_id: int, action: str, details: str):
    """记录操作日志"""
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO operation_logs (user_id, action, details) VALUES (?, ?, ?)",
              (user_id, action, details))
    conn.commit()
    conn.close()
