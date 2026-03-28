import sys
import json
import sqlite3
import time
import re
import hashlib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "s2_small_enterprise.db")

class SMallEnterpriseEngine:
    def __init__(self):
        self.init_db()

    def init_db(self):
        """初始化企业版商业数据库：包含 1年期审计日志 和 智能合约库"""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 1v1 互斥锁洽谈室状态
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS negotiation_rooms (
                mm_coordinate TEXT PRIMARY KEY,
                is_locked BOOLEAN,
                visitor_did TEXT,
                agent_did TEXT,
                start_time REAL
            )
        ''')
        
        # 四大数据流的 1 年期全息审计快照 (Visitor, Agent, Product, Six Elements)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compliance_audit_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                mm_coordinate TEXT,
                visitor_did TEXT,
                agent_did TEXT,
                product_id TEXT,
                six_elements_hash TEXT,
                interaction_log TEXT,
                timestamp REAL,
                retention_expiry REAL
            )
        ''')

        # 空间绑定智能合约存证
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spatial_smart_contracts (
                contract_hash TEXT PRIMARY KEY,
                mm_coordinate TEXT,
                visitor_did TEXT,
                agent_did TEXT,
                product_id TEXT,
                six_elements_hash TEXT,
                timestamp REAL
            )
        ''')
        conn.commit()
        conn.close()

    def validate_mm_coordinate(self, coord):
        """
        校验毫米级精度的 S-Mall 展示间坐标
        格式: [L1]-[L2]-[L3]-[L4C]-[RoomID(L5)]-[GridID(L6)]-[X]-[Y]-[Z]
        示例: PHYS-CN-001-QIANJIA9-5-1-1000-1000-1200
        """
        pattern = re.compile(
            r'^([A-Z]{4})-([A-Z]{2})-([0-9]{3})-([A-Z]{5,35}[0-9])-([1-9][0-9]{0,4})-([1-9])-(\d{1,4})-(\d{1,4})-(\d{1,4})$',
            re.IGNORECASE
        )
        match = pattern.match(coord)
        if not match:
            return False, "[Error] Invalid Millimeter Coordinate. Must follow L1-L2-L3-L4C-L5-L6-X-Y-Z."
        
        # 校验 XYZ 边界: SSSU 标准空间尺寸 2000x2000x2400
        x, y, z = int(match.group(7)), int(match.group(8)), int(match.group(9))
        if x > 2000 or y > 2000 or z > 2400:
            return False, "[Error] Coordinate out of SSSU bounds (Max: 2000x2000x2400)."
            
        return True, coord.upper()

    def enter_1v1_negotiation(self, params):
        """进入展示间洽谈：激活 SMP 互斥锁，开始四据流记录"""
        coord = params.get("mm_coordinate", "")
        visitor_did = params.get("visitor_did", "Unknown_Visitor")
        agent_did = params.get("agent_did", "Unknown_Agent")

        is_valid, parsed_coord = self.validate_mm_coordinate(coord)
        if not is_valid:
            return parsed_coord

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 检查是否已被占用
        cursor.execute('SELECT is_locked FROM negotiation_rooms WHERE mm_coordinate = ?', (parsed_coord,))
        row = cursor.fetchone()
        if row and row[0]:
            conn.close()
            return f"[SMP Mutex Locked] 展示间 {parsed_coord} 正在进行 1v1 专属接待，请在橱窗外公海等候。"

        # 上锁
        cursor.execute('''
            INSERT OR REPLACE INTO negotiation_rooms (mm_coordinate, is_locked, visitor_did, agent_did, start_time)
            VALUES (?, ?, ?, ?, ?)
        ''', (parsed_coord, True, visitor_did, agent_did, time.time()))
        conn.commit()
        conn.close()
        
        return f"[1v1 Negotiation Started] 顾客 {visitor_did} 已跨入 {parsed_coord}。互斥锁已激活，全息审计录音/录像流（四大对象）开始同步，留存期自动设为 1 年。"

    def open_x_sssu_portal(self, params):
        """开启 X-SSSU 扩展空间，处理缩放 k 值"""
        coord = params.get("mm_coordinate", "")
        k_factor = float(params.get("k_factor", 1.0))
        product_name = params.get("product_name", "Unknown Product")

        is_valid, parsed_coord = self.validate_mm_coordinate(coord)
        if not is_valid: return parsed_coord

        if k_factor > 1.0:
            return (f"[X-SSSU Expanded] 扩展门已打开 (k={k_factor})。空间等比例放大。"
                    f"请 {params.get('agent_did')} 与访客 步入 扩展空间，体验 {product_name} 的全尺寸真实物理反馈。六要素实施库已覆盖至放大区域。")
        elif k_factor < 1.0:
            return (f"[X-SSSU Shrunk] 微观扩展门已打开 (k={k_factor})。空间等比例缩小。"
                    f"基于占位法则，生命体无法进入。系统已切换至 上帝旁观者视角，以协助观察 {product_name} 的微观运作细节。")
        else:
            return "[Error] Invalid k_factor. Must be > 1.0 or < 1.0."

    def sign_spatial_contract(self, params):
        """生成并签署带有空间烙印的智能合约"""
        coord = params.get("mm_coordinate", "")
        visitor_did = params.get("visitor_did", "")
        agent_did = params.get("agent_did", "")
        product_id = params.get("product_id", "")
        six_elements_hash = params.get("six_elements_hash", "0x0000_DEFAULT") # 应从环境OS获取

        is_valid, parsed_coord = self.validate_mm_coordinate(coord)
        if not is_valid: return parsed_coord

        timestamp = time.time()
        # 核心算法：将时间、地点(毫米级)、双方身份、环境哈希进行不可逆加密
        raw_data = f"{timestamp}|{parsed_coord}|{visitor_did}|{agent_did}|{product_id}|{six_elements_hash}"
        contract_hash = hashlib.sha256(raw_data.encode()).hexdigest()

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # 写入合约表
        cursor.execute('''
            INSERT INTO spatial_smart_contracts (contract_hash, mm_coordinate, visitor_did, agent_did, product_id, six_elements_hash, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (contract_hash, parsed_coord, visitor_did, agent_did, product_id, six_elements_hash, timestamp))
        
        # 同时写入 1年期全息审计日志
        retention_expiry = timestamp + (365 * 24 * 60 * 60) # 1年
        cursor.execute('''
            INSERT INTO compliance_audit_logs (mm_coordinate, visitor_did, agent_did, product_id, six_elements_hash, interaction_log, timestamp, retention_expiry)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (parsed_coord, visitor_did, agent_did, product_id, six_elements_hash, "[Contract Signed] Intent Confirmed.", timestamp, retention_expiry))
        
        # 释放 Mutex 锁
        cursor.execute('UPDATE negotiation_rooms SET is_locked = False WHERE mm_coordinate = ?', (parsed_coord,))
        
        conn.commit()
        conn.close()

        return (f"[Smart Contract Minted] 交易达成！\n"
                f"合约哈希: {contract_hash}\n"
                f"签约坐标: {parsed_coord}\n"
                f"买方: {visitor_did} | 卖方: {agent_did}\n"
                f"审计记录已归档，锁定期 1 年。互斥锁已释放，橱窗恢复公海浏览状态。")

def main():
    try:
        input_data = sys.stdin.read()
        if not input_data: return
        request = json.loads(input_data)
        action = request.get("action")
        params = request.get("params", {})
        
        engine = SMallEnterpriseEngine()
        if action == "enter_1v1_negotiation": result = engine.enter_1v1_negotiation(params)
        elif action == "open_x_sssu_portal": result = engine.open_x_sssu_portal(params)
        elif action == "sign_spatial_contract": result = engine.sign_spatial_contract(params)
        else: result = "Unknown Enterprise Action."
        
        print(json.dumps({"status": "success", "output": result}))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}))

if __name__ == "__main__":
    main()