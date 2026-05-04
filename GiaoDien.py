from flask import Flask, render_template_string, request, redirect
from decimal import Decimal
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# ================= DB =================
def get_conn():
    return pyodbc.connect(
        f"DRIVER={{SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_UID')};"
        f"PWD={os.getenv('DB_PWD')};"
    )

# ================= BASE LAYOUT =================
BASE_STYLE = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:        #f0f4f8;
  --surface:   #ffffff;
  --surface2:  #f8fafc;
  --border:    #e2e8f0;
  --accent:    #3b82f6;
  --accent2:   #6366f1;
  --green:     #16a34a;
  --yellow:    #d97706;
  --red:       #dc2626;
  --text:      #1e293b;
  --muted:     #64748b;
  --radius:    14px;
  --font:      'Sora', sans-serif;
  --mono:      'JetBrains Mono', monospace;
}

body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  display: flex;
}

/* ===== SIDEBAR ===== */
.sidebar {
  width: 240px;
  min-height: 100vh;
  background: #1e3a5f;
  border-right: none;
  display: flex;
  flex-direction: column;
  padding: 24px 16px;
  position: fixed;
  top: 0; left: 0;
  z-index: 100;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  margin-bottom: 28px;
}

.logo-icon {
  width: 36px; height: 36px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
}

.logo-text {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: white;
}

.nav-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: rgba(255,255,255,.4);
  text-transform: uppercase;
  padding: 0 12px;
  margin-bottom: 8px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  color: rgba(255,255,255,.6);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: all .18s ease;
  margin-bottom: 2px;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(255,255,255,.12);
  color: white;
}

.nav-link.active {
  color: white;
}

.nav-icon {
  width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 8px;
  font-size: 15px;
}

.nav-link.active .nav-icon { background: rgba(255,255,255,.15); }

/* ===== MAIN ===== */
.main {
  margin-left: 240px;
  flex: 1;
  padding: 28px 32px;
  min-height: 100vh;
}

/* ===== PAGE HEADER ===== */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;
}

.page-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text);
}

.page-sub {
  font-size: 13px;
  color: var(--muted);
  margin-top: 2px;
}

/* ===== STAT CARDS ===== */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 22px;
  position: relative;
  overflow: hidden;
  transition: border-color .2s;
}

.stat-card:hover { border-color: #2d3748; }

.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
}

.stat-card.c1::before { background: linear-gradient(90deg, #3b82f6, #6366f1); }
.stat-card.c2::before { background: linear-gradient(90deg, #22c55e, #10b981); }
.stat-card.c3::before { background: linear-gradient(90deg, #f59e0b, #f97316); }
.stat-card.c4::before { background: linear-gradient(90deg, #ef4444, #ec4899); }

.stat-icon {
  font-size: 22px;
  margin-bottom: 12px;
}

.stat-label {
  font-size: 12px;
  color: var(--muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: .06em;
  margin-bottom: 6px;
}

.stat-val {
  font-size: 26px;
  font-weight: 700;
  color: white;
}

/* ===== CARD / TABLE ===== */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.card-head {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}

thead th {
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .08em;
  text-transform: uppercase;
  color: var(--muted);
  background: #f1f5f9;
  border-bottom: 1px solid var(--border);
}

tbody tr {
  border-bottom: 1px solid var(--border);
  transition: background .15s;
}

tbody tr:last-child { border-bottom: none; }
tbody tr:hover { background: var(--surface2); }

tbody td {
  padding: 13px 16px;
  color: var(--text);
}

.id-cell {
  font-family: var(--mono);
  font-size: 12px;
  color: var(--muted);
}

.money-cell {
  font-family: var(--mono);
  font-size: 13px;
  color: var(--green);
  font-weight: 600;
}

/* ===== BADGES ===== */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .04em;
}

.badge-draft  { background: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1; }
.badge-active { background: #dcfce7; color: #16a34a; border: 1px solid #bbf7d0; }
.badge-done   { background: #dbeafe; color: #1d4ed8; border: 1px solid #bfdbfe; }
.badge-month  { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.badge-year   { background: #ede9fe; color: #6d28d9; border: 1px solid #ddd6fe; }
.badge-once   { background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; }

/* ===== BUTTONS ===== */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 9px;
  font-size: 13px;
  font-weight: 500;
  font-family: var(--font);
  cursor: pointer;
  border: none;
  text-decoration: none;
  transition: all .15s;
}

.btn-primary {
  background: var(--accent);
  color: white;
}
.btn-primary:hover { background: #2563eb; color: white; }

.btn-warning {
  background: rgba(245,158,11,.15);
  color: var(--yellow);
  border: 1px solid rgba(245,158,11,.2);
}
.btn-warning:hover { background: rgba(245,158,11,.25); }

.btn-danger {
  background: rgba(239,68,68,.12);
  color: var(--red);
  border: 1px solid rgba(239,68,68,.2);
}
.btn-danger:hover { background: rgba(239,68,68,.22); }

.btn-ghost {
  background: white;
  color: var(--muted);
  border: 1px solid var(--border);
}
.btn-ghost:hover { color: var(--text); background: #f1f5f9; }

.btn-sm {
  padding: 5px 11px;
  font-size: 12px;
  border-radius: 7px;
}

/* ===== MODAL ===== */
.modal-bg {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.7);
  backdrop-filter: blur(4px);
  z-index: 999;
  align-items: flex-start;
  justify-content: center;
  padding: 40px 16px;
  overflow-y: auto;
}

.modal-bg.open { display: flex; }

.modal-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  width: 100%;
  max-width: 860px;
  padding: 28px;
  animation: slideUp .25s ease;
}

@keyframes slideUp {
  from { opacity:0; transform:translateY(20px); }
  to   { opacity:1; transform:translateY(0); }
}

.modal-title {
  font-size: 17px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.group-box {
  background: #f8fafc;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  margin-bottom: 14px;
}

.group-title {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: .1em;
  text-transform: uppercase;
  color: var(--muted);
  margin-bottom: 14px;
}

.form-row {
  display: grid;
  gap: 12px;
}

.form-row.cols-2 { grid-template-columns: 1fr 1fr; }
.form-row.cols-3 { grid-template-columns: 1fr 1fr 1fr; }
.form-row.cols-4 { grid-template-columns: 2fr 3fr 2fr; }

.form-group { display: flex; flex-direction: column; gap: 5px; }

label {
  font-size: 12px;
  font-weight: 600;
  color: var(--muted);
  letter-spacing: .02em;
}

input, select, textarea {
  background: white;
  border: 1px solid var(--border);
  border-radius: 9px;
  color: var(--text);
  font-family: var(--font);
  font-size: 13.5px;
  padding: 9px 13px;
  width: 100%;
  outline: none;
  transition: border-color .15s;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(59,130,246,.1);
}

select option { background: white; }

.modal-footer {
  display: flex;
  gap: 10px;
  margin-top: 18px;
}

/* ===== ACTION CELL ===== */
.action-cell {
  display: flex;
  gap: 6px;
  align-items: center;
}

/* ===== FORM PAGE ===== */
.form-page {
  max-width: 640px;
}

.form-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 30px;
}

.form-card h2 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 20px;
}

/* ===== DIVIDER ===== */
hr { border: none; border-top: 1px solid var(--border); margin: 16px 0; }

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
"""

# ================= SIDEBAR NAV =================
def sidebar(active=""):
    links = [
        ("/",           "dashboard", "📊", "Dashboard"),
        ("/customers",  "customers", "👤", "Khách hàng"),
        ("/contracts",  "contracts", "📄", "Hợp đồng"),
    ]
    items = ""
    for href, key, icon, label in links:
        cls = "nav-link active" if active == key else "nav-link"
        items += f'<a href="{href}" class="{cls}"><span class="nav-icon">{icon}</span>{label}</a>\n'

    return f"""
    <aside class="sidebar">
      <div class="sidebar-logo">
        <div class="logo-icon">⚙</div>
        <span class="logo-text">ERP SYSTEM</span>
      </div>
      <div class="nav-label">Menu</div>
      {items}
    </aside>
    """

def page(title, content, active="", extra_head=""):
    nav = sidebar(active)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — ERP</title>
<style>{BASE_STYLE}</style>
{extra_head}
</head>
<body>
{nav}
<div class="main">
{content}
</div>
</body>
</html>"""

# ================= DASHBOARD =================
@app.route("/")
def home():
    conn = get_conn()
    try:
        cur = conn.cursor()

        # Tổng khách hàng
        cur.execute("SELECT COUNT(*) FROM KhachHang")
        total_kh = cur.fetchone()[0]

        # Tổng hợp đồng
        cur.execute("SELECT COUNT(*) FROM HopDong")
        total_hd = cur.fetchone()[0]

        # Tổng doanh thu (tổng TongTien các hợp đồng ACTIVE + DONE)
        cur.execute("SELECT ISNULL(SUM(TongTien),0) FROM HopDong WHERE TrangThai IN ('ACTIVE','DONE')")
        total_dt = cur.fetchone()[0]
        total_dt = float(total_dt) if total_dt else 0

        # Hợp đồng ACTIVE
        cur.execute("SELECT COUNT(*) FROM HopDong WHERE TrangThai='ACTIVE'")
        total_active = cur.fetchone()[0]

        # Cảnh báo: hợp đồng sắp đến hạn trong 30 ngày tới hoặc đã quá hạn mà chưa DONE
        cur.execute("""
            SELECT h.HopDongID, h.SoHopDong, k.TenKhachHang,
                   h.NgayKetThuc, h.TongTien, h.TrangThai,
                   DATEDIFF(day, GETDATE(), h.NgayKetThuc) as SoNgay
            FROM HopDong h
            LEFT JOIN KhachHang k ON h.KhachHangID = k.KhachHangID
            WHERE h.NgayKetThuc IS NOT NULL
              AND h.TrangThai != 'DONE'
              AND DATEDIFF(day, GETDATE(), h.NgayKetThuc) <= 30
            ORDER BY h.NgayKetThuc ASC
        """)
        canh_bao = cur.fetchall()

    finally:
        conn.close()

    def fmt_money(v):
        if not v: return "0"
        return format(int(float(v)), ",").replace(",", ".")

    # Render cảnh báo
    canh_bao_rows = ""
    for r in canh_bao:
        so_ngay = r[6]
        if so_ngay < 0:
            badge = f'<span class="badge badge-once">Quá hạn {abs(so_ngay)} ngày</span>'
        elif so_ngay == 0:
            badge = '<span class="badge badge-once">Hết hạn hôm nay</span>'
        elif so_ngay <= 7:
            badge = f'<span class="badge badge-once">Còn {so_ngay} ngày</span>'
        else:
            badge = f'<span class="badge badge-month">Còn {so_ngay} ngày</span>'

        canh_bao_rows += f"""
        <tr>
          <td style="font-family:var(--mono);font-size:12px;color:#2563eb">{r[1]}</td>
          <td style="font-weight:500">{r[2] or '—'}</td>
          <td class="id-cell">{str(r[3])[:10] if r[3] else '—'}</td>
          <td class="money-cell">{fmt_money(r[4])}</td>
          <td>{badge}</td>
          <td>
            <a href="/contracts/edit/{r[0]}" class="btn btn-warning btn-sm">✏ Xử lý</a>
          </td>
        </tr>"""

    canh_bao_section = ""
    if canh_bao_rows:
        canh_bao_section = f"""
        <div class="card" style="margin-top:0; border: 1px solid #fca5a5;">
          <div class="card-head" style="background:#fff7f7">
            <span class="card-title" style="color:#dc2626">⚠️ Cảnh báo hợp đồng sắp đến hạn</span>
            <span style="font-size:12px;color:#dc2626;font-weight:600">{len(canh_bao)} hợp đồng cần xử lý</span>
          </div>
          <table>
            <thead>
              <tr>
                <th>Số HĐ</th><th>Khách hàng</th><th>Ngày kết thúc</th>
                <th>Tổng tiền</th><th>Trạng thái</th><th>Thao tác</th>
              </tr>
            </thead>
            <tbody>{canh_bao_rows}</tbody>
          </table>
        </div>"""
    else:
        canh_bao_section = """
        <div class="card" style="margin-top:0; border:1px solid #bbf7d0">
          <div class="card-head" style="background:#f0fdf4">
            <span class="card-title" style="color:#16a34a">✅ Không có hợp đồng nào sắp đến hạn</span>
          </div>
        </div>"""

    content = f"""
    <div class="page-header">
      <div>
        <div class="page-title">Dashboard</div>
        <div class="page-sub">Tổng quan hệ thống ERP — cập nhật theo thời gian thực</div>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-card c1">
        <div class="stat-icon">👤</div>
        <div class="stat-label">Khách hàng</div>
        <div class="stat-val">{total_kh}</div>
      </div>
      <div class="stat-card c2">
        <div class="stat-icon">📄</div>
        <div class="stat-label">Hợp đồng</div>
        <div class="stat-val">{total_hd}</div>
      </div>
      <div class="stat-card c3">
        <div class="stat-icon">💰</div>
        <div class="stat-label">Doanh thu (VNĐ)</div>
        <div class="stat-val" style="font-size:18px">{fmt_money(total_dt)}</div>
      </div>
      <div class="stat-card c4">
        <div class="stat-icon">✅</div>
        <div class="stat-label">Đang hoạt động</div>
        <div class="stat-val">{total_active}</div>
      </div>
    </div>

    <div style="margin-bottom:12px">
      <div class="page-title" style="font-size:15px;margin-bottom:12px">⚠️ Cảnh báo thanh toán</div>
      {canh_bao_section}
    </div>
    """
    return page("Dashboard", content, active="dashboard")


# ================= CUSTOMERS =================
@app.route("/customers", methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
            INSERT INTO KhachHang (MaKhachHang, TenKhachHang, MaSoThue, DienThoai, Email)
            VALUES (?, ?, ?, ?, ?)
            """,
            request.form.get("ma_kh"),
            request.form.get("ten_kh"),
            request.form.get("mst"),
            request.form.get("dt"),
            request.form.get("email"))
            conn.commit()
        finally:
            conn.close()
        return redirect("/customers")

    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("""
        SELECT KhachHangID, MaKhachHang, TenKhachHang, MaSoThue, DienThoai, Email
        FROM KhachHang ORDER BY KhachHangID DESC
        """)
        rows = cur.fetchall()
    finally:
        conn.close()

    rows_html = ""
    for r in rows:
        rows_html += f"""
        <tr>
          <td class="id-cell">#{r[0]}</td>
          <td><span style="font-family:var(--mono);font-size:12px;color:#2563eb">{r[1]}</span></td>
          <td style="font-weight:500;color:var(--text)">{r[2]}</td>
          <td class="id-cell">{r[3] or '—'}</td>
          <td>{r[4] or '—'}</td>
          <td>{r[5] or '—'}</td>
          <td>
            <div class="action-cell">
              <a href="/customers/edit/{r[0]}" class="btn btn-warning btn-sm">✏ Sửa</a>
              <a href="/customers/delete/{r[0]}" class="btn btn-danger btn-sm"
                 onclick="return confirm('Xóa khách hàng này?')">🗑</a>
            </div>
          </td>
        </tr>"""

    content = f"""
    <div class="page-header">
      <div>
        <div class="page-title">Khách hàng</div>
        <div class="page-sub">Danh sách khách hàng trong hệ thống</div>
      </div>
      <button class="btn btn-primary" onclick="openModal('modal-add')">➕ Thêm mới</button>
    </div>

    <div class="card">
      <div class="card-head">
        <span class="card-title">Danh sách</span>
        <span style="font-size:12px;color:var(--muted)">{len(rows)} khách hàng</span>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>Mã KH</th><th>Tên khách hàng</th>
            <th>Mã số thuế</th><th>Điện thoại</th><th>Email</th><th>Thao tác</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>

    <!-- MODAL THÊM -->
    <div id="modal-add" class="modal-bg">
      <div class="modal-box">
        <div class="modal-title">➕ Thêm khách hàng mới</div>
        <form method="POST">
          <div class="group-box">
            <div class="group-title">Thông tin cơ bản</div>
            <div class="form-row cols-2" style="margin-bottom:12px">
              <div class="form-group">
                <label>Mã khách hàng *</label>
                <input name="ma_kh" placeholder="VD: KH001" required>
              </div>
              <div class="form-group">
                <label>Tên khách hàng *</label>
                <input name="ten_kh" placeholder="Tên công ty / cá nhân" required>
              </div>
            </div>
            <div class="form-row cols-3">
              <div class="form-group">
                <label>Mã số thuế</label>
                <input name="mst" placeholder="0123456789">
              </div>
              <div class="form-group">
                <label>Điện thoại</label>
                <input name="dt" placeholder="0901 234 567">
              </div>
              <div class="form-group">
                <label>Email</label>
                <input name="email" type="email" placeholder="email@example.com">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="submit" class="btn btn-primary">💾 Lưu khách hàng</button>
            <button type="button" class="btn btn-ghost" onclick="closeModal('modal-add')">Đóng</button>
          </div>
        </form>
      </div>
    </div>
    """

    extra = """<script>
    function openModal(id){ document.getElementById(id).classList.add('open'); }
    function closeModal(id){ document.getElementById(id).classList.remove('open'); }
    document.querySelectorAll('.modal-bg').forEach(m=>{
      m.addEventListener('click',e=>{ if(e.target===m) m.classList.remove('open'); });
    });
    </script>"""

    return page("Khách hàng", content, active="customers", extra_head=extra)


# ================= DELETE CUSTOMER =================
@app.route("/customers/delete/<int:id>")
def delete_customer(id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM KhachHang WHERE KhachHangID=?", id)
        conn.commit()
    finally:
        conn.close()
    return redirect("/customers")


# ================= EDIT CUSTOMER =================
@app.route("/customers/edit/<int:id>", methods=["GET", "POST"])
def edit_customer(id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        if request.method == "POST":
            cur.execute("""
            UPDATE KhachHang
            SET MaKhachHang=?, TenKhachHang=?, MaSoThue=?, DienThoai=?, Email=?
            WHERE KhachHangID=?
            """,
            request.form.get("ma_kh"),
            request.form.get("ten_kh"),
            request.form.get("mst"),
            request.form.get("dt"),
            request.form.get("email"),
            id)
            conn.commit()
            return redirect("/customers")

        cur.execute("""
        SELECT KhachHangID, MaKhachHang, TenKhachHang, MaSoThue, DienThoai, Email
        FROM KhachHang WHERE KhachHangID=?
        """, id)
        row = cur.fetchone()
    finally:
        conn.close()

    content = f"""
    <div class="page-header">
      <div>
        <div class="page-title">Sửa khách hàng</div>
        <div class="page-sub">Cập nhật thông tin khách hàng #{id}</div>
      </div>
    </div>
    <div class="form-page">
      <div class="form-card">
        <form method="POST">
          <div class="group-box">
            <div class="group-title">Thông tin cơ bản</div>
            <div class="form-row cols-2" style="margin-bottom:12px">
              <div class="form-group">
                <label>Mã khách hàng</label>
                <input name="ma_kh" value="{row[1]}">
              </div>
              <div class="form-group">
                <label>Tên khách hàng</label>
                <input name="ten_kh" value="{row[2]}">
              </div>
            </div>
            <div class="form-row cols-3">
              <div class="form-group">
                <label>Mã số thuế</label>
                <input name="mst" value="{row[3] or ''}">
              </div>
              <div class="form-group">
                <label>Điện thoại</label>
                <input name="dt" value="{row[4] or ''}">
              </div>
              <div class="form-group">
                <label>Email</label>
                <input name="email" value="{row[5] or ''}">
              </div>
            </div>
          </div>
          <div style="display:flex;gap:10px;margin-top:16px">
            <button type="submit" class="btn btn-primary">💾 Cập nhật</button>
            <a href="/customers" class="btn btn-ghost">↩ Quay lại</a>
          </div>
        </form>
      </div>
    </div>
    """
    return page("Sửa khách hàng", content, active="customers")


# ================= CONTRACTS =================
def badge_status(val):
    m = {"DRAFT":"badge-draft","ACTIVE":"badge-active","DONE":"badge-done"}
    cls = m.get(val, "badge-draft")
    return f'<span class="badge {cls}">{val or "DRAFT"}</span>'

def badge_tt(val):
    m = {"MONTH":"badge-month","YEAR":"badge-year","ONCE":"badge-once"}
    cls = m.get(val, "badge-draft")
    labels = {"MONTH":"Theo tháng","YEAR":"Theo năm","ONCE":"Một lần"}
    return f'<span class="badge {cls}">{labels.get(val, val or "—")}</span>'

@app.route("/contracts", methods=["GET", "POST"])
def contracts():
    conn = get_conn()
    try:
        cur = conn.cursor()

        if request.method == "POST":
            cur.execute("""
            INSERT INTO HopDong
            (SoHopDong, KhachHangID, NgayKy, NgayBatDau, NgayKetThuc,
             TongTien, TienTamUng, NgayTamUng, LoaiThanhToan, TrangThai)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            request.form.get("so_hd"),
            request.form.get("kh_id"),
            request.form.get("ngay_ky") or None,
            request.form.get("ngay_bd") or None,
            request.form.get("ngay_kt") or None,
            request.form.get("tong_tien") or None,
            request.form.get("tam_ung") or None,
            request.form.get("ngay_tu") or None,
            request.form.get("loai_tt"),
            "DRAFT")
            conn.commit()
            return redirect("/contracts")

        cur.execute("SELECT KhachHangID, TenKhachHang FROM KhachHang ORDER BY TenKhachHang")
        customers = cur.fetchall()

        # cols: [0]ID [1]SoHD [2]KhachHangID [3]NgayKy [4]NgayBatDau [5]NgayKetThuc
        #       [6]TongTien [7]TienTamUng [8]NgayTamUng [9]LoaiThanhToan [10]TrangThai
        cur.execute("""
        SELECT h.HopDongID, h.SoHopDong, k.TenKhachHang,
               h.NgayKy, h.NgayBatDau, h.NgayKetThuc,
               h.TongTien, h.TienTamUng,
               h.LoaiThanhToan, h.TrangThai,
               h.HopDongID as ActionID
        FROM HopDong h
        LEFT JOIN KhachHang k ON h.KhachHangID = k.KhachHangID
        ORDER BY h.HopDongID DESC
        """)
        data = cur.fetchall()
    finally:
        conn.close()

    rows_html = ""
    for r in data:
        r = list(r)
        # Format money
        def fmt(v):
            if v is None: return "—"
            v = float(v) if isinstance(v, Decimal) else v
            return format(int(v), ",").replace(",", ".")

        tong = fmt(r[6])
        tam  = fmt(r[7])

        rows_html += f"""
        <tr>
          <td class="id-cell">#{r[0]}</td>
          <td style="font-family:var(--mono);font-size:12px;color:#2563eb">{r[1]}</td>
          <td style="font-weight:500;color:var(--text)">{r[2] or '—'}</td>
          <td class="id-cell">{r[3] or '—'}</td>
          <td class="id-cell">{r[4] or '—'}</td>
          <td class="id-cell">{r[5] or '—'}</td>
          <td class="money-cell">{tong}</td>
          <td class="money-cell">{tam}</td>
          <td>{badge_tt(r[8])}</td>
          <td>{badge_status(r[9])}</td>
          <td>
            <div class="action-cell">
              <a href="/contracts/edit/{r[10]}" class="btn btn-warning btn-sm">✏ Sửa</a>
              <a href="/contracts/delete/{r[10]}" class="btn btn-danger btn-sm"
                 onclick="return confirm('Xóa hợp đồng này?')">🗑</a>
            </div>
          </td>
        </tr>"""

    cust_opts = "".join(f'<option value="{c[0]}">{c[1]}</option>' for c in customers)

    content = f"""
    <div class="page-header">
      <div>
        <div class="page-title">Hợp đồng</div>
        <div class="page-sub">Quản lý hợp đồng khách hàng</div>
      </div>
      <button class="btn btn-primary" onclick="openModal('modal-add')">➕ Thêm hợp đồng</button>
    </div>

    <div class="card">
      <div class="card-head">
        <span class="card-title">Danh sách hợp đồng</span>
        <span style="font-size:12px;color:var(--muted)">{len(data)} hợp đồng</span>
      </div>
      <div style="overflow-x:auto">
        <table>
          <thead>
            <tr>
              <th>ID</th><th>Số HĐ</th><th>Khách hàng</th>
              <th>Ngày ký</th><th>Bắt đầu</th><th>Kết thúc</th>
              <th>Tổng tiền</th><th>Tạm ứng</th>
              <th>Thanh toán</th><th>Trạng thái</th><th>Thao tác</th>
            </tr>
          </thead>
          <tbody>{rows_html}</tbody>
        </table>
      </div>
    </div>

    <!-- MODAL THÊM HỢP ĐỒNG -->
    <div id="modal-add" class="modal-bg">
      <div class="modal-box">
        <div class="modal-title">📄 Thêm hợp đồng mới</div>
        <form method="POST">
          <div class="group-box">
            <div class="group-title">Thông tin chung</div>
            <div class="form-row cols-4">
              <div class="form-group">
                <label>Số hợp đồng</label>
                <input name="so_hd" placeholder="HD2025-001">
              </div>
              <div class="form-group">
                <label>Tên hợp đồng</label>
                <input name="ten_hd" placeholder="Tên hợp đồng">
              </div>
              <div class="form-group">
                <label>Khách hàng</label>
                <select name="kh_id">
                  <option value="">-- Chọn --</option>
                  {cust_opts}
                </select>
              </div>
            </div>
          </div>

          <div class="group-box">
            <div class="group-title">Thời gian</div>
            <div class="form-row cols-3">
              <div class="form-group">
                <label>Ngày ký</label>
                <input type="date" name="ngay_ky">
              </div>
              <div class="form-group">
                <label>Ngày bắt đầu</label>
                <input type="date" name="ngay_bd">
              </div>
              <div class="form-group">
                <label>Ngày kết thúc</label>
                <input type="date" name="ngay_kt">
              </div>
            </div>
          </div>

          <div class="group-box">
            <div class="group-title">Tài chính</div>
            <div class="form-row cols-3">
              <div class="form-group">
                <label>Tổng tiền</label>
                <input name="tong_tien" placeholder="0">
              </div>
              <div class="form-group">
                <label>Tạm ứng</label>
                <input name="tam_ung" placeholder="0">
              </div>
              <div class="form-group">
                <label>Ngày tạm ứng</label>
                <input type="date" name="ngay_tu">
              </div>
            </div>
            <div class="form-row cols-2" style="margin-top:12px">
              <div class="form-group">
                <label>Loại thanh toán</label>
                <select name="loai_tt">
                  <option value="MONTH">Theo tháng</option>
                  <option value="YEAR">Theo năm</option>
                  <option value="ONCE">Một lần</option>
                </select>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button type="submit" class="btn btn-primary">💾 Lưu hợp đồng</button>
            <button type="button" class="btn btn-ghost" onclick="closeModal('modal-add')">Đóng</button>
          </div>
        </form>
      </div>
    </div>
    """

    extra = """<script>
    function openModal(id){ document.getElementById(id).classList.add('open'); }
    function closeModal(id){ document.getElementById(id).classList.remove('open'); }
    document.querySelectorAll('.modal-bg').forEach(m=>{
      m.addEventListener('click',e=>{ if(e.target===m) m.classList.remove('open'); });
    });
    </script>"""

    return page("Hợp đồng", content, active="contracts", extra_head=extra)


# ================= DELETE CONTRACT =================
@app.route("/contracts/delete/<int:id>")
def delete_contract(id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM HopDong WHERE HopDongID=?", id)
        conn.commit()
    finally:
        conn.close()
    return redirect("/contracts")


# ================= EDIT CONTRACT =================
@app.route("/contracts/edit/<int:id>", methods=["GET", "POST"])
def edit_contract(id):
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute("SELECT KhachHangID, TenKhachHang FROM KhachHang ORDER BY TenKhachHang")
        customers = cur.fetchall()

        if request.method == "POST":
            tong_tien = request.form.get("tong_tien", "").replace(".", "") or None
            tam_ung   = request.form.get("tam_ung", "").replace(".", "") or None
            try:
                tong_tien = float(tong_tien) if tong_tien else None
                tam_ung   = float(tam_ung)   if tam_ung   else None
            except ValueError:
                tong_tien = tam_ung = None

            cur.execute("""
            UPDATE HopDong
            SET SoHopDong=?, KhachHangID=?, NgayKy=?, NgayBatDau=?, NgayKetThuc=?,
                TongTien=?, TienTamUng=?, NgayTamUng=?, LoaiThanhToan=?, TrangThai=?
            WHERE HopDongID=?
            """,
            request.form.get("so_hd"),
            request.form.get("kh_id"),
            request.form.get("ngay_ky") or None,
            request.form.get("ngay_bd") or None,
            request.form.get("ngay_kt") or None,
            tong_tien, tam_ung,
            request.form.get("ngay_tu") or None,
            request.form.get("loai_tt"),
            request.form.get("trang_thai"),
            id)
            conn.commit()
            return redirect("/contracts")  # FIX: redirect sau POST

        cur.execute("""
        SELECT HopDongID, SoHopDong, KhachHangID, NgayKy, NgayBatDau, NgayKetThuc,
               TongTien, TienTamUng, NgayTamUng, LoaiThanhToan, TrangThai
        FROM HopDong WHERE HopDongID=?
        """, id)
        raw = cur.fetchone()
    finally:
        conn.close()

    r = list(raw)
    def fmt(v):
        if v is None: return ""
        v = float(v) if isinstance(v, Decimal) else v
        return format(int(v), ",").replace(",", ".")

    r[6] = fmt(r[6])
    r[7] = fmt(r[7])

    def date_val(v):
        if not v: return ""
        return str(v)[:10]

    cust_opts = "".join(
        f'<option value="{c[0]}" {"selected" if c[0]==r[2] else ""}>{c[1]}</option>'
        for c in customers
    )

    tt_opts = ""
    for val, label in [("MONTH","Theo tháng"),("YEAR","Theo năm"),("ONCE","Một lần")]:
        sel = "selected" if r[9] == val else ""
        tt_opts += f'<option value="{val}" {sel}>{label}</option>'

    status_opts = ""
    for val, label in [("DRAFT","Draft"),("ACTIVE","Active"),("DONE","Done")]:
        sel = "selected" if r[10] == val else ""
        status_opts += f'<option value="{val}" {sel}>{label}</option>'

    content = f"""
    <div class="page-header">
      <div>
        <div class="page-title">Sửa hợp đồng</div>
        <div class="page-sub">Cập nhật thông tin hợp đồng #{id}</div>
      </div>
    </div>

    <form method="POST" style="max-width:860px">
      <div class="group-box">
        <div class="group-title">Thông tin chung</div>
        <div class="form-row cols-2" style="margin-bottom:12px">
          <div class="form-group">
            <label>Số hợp đồng</label>
            <input name="so_hd" value="{r[1]}">
          </div>
          <div class="form-group">
            <label>Khách hàng</label>
            <select name="kh_id">{cust_opts}</select>
          </div>
        </div>
      </div>

      <div class="group-box">
        <div class="group-title">Thời gian</div>
        <div class="form-row cols-3">
          <div class="form-group">
            <label>Ngày ký</label>
            <input type="date" name="ngay_ky" value="{date_val(r[3])}">
          </div>
          <div class="form-group">
            <label>Ngày bắt đầu</label>
            <input type="date" name="ngay_bd" value="{date_val(r[4])}">
          </div>
          <div class="form-group">
            <label>Ngày kết thúc</label>
            <input type="date" name="ngay_kt" value="{date_val(r[5])}">
          </div>
        </div>
      </div>

      <div class="group-box">
        <div class="group-title">Tài chính & Trạng thái</div>
        <div class="form-row cols-3" style="margin-bottom:12px">
          <div class="form-group">
            <label>Tổng tiền</label>
            <input name="tong_tien" value="{r[6]}">
          </div>
          <div class="form-group">
            <label>Tạm ứng</label>
            <input name="tam_ung" value="{r[7]}">
          </div>
          <div class="form-group">
            <label>Ngày tạm ứng</label>
            <input type="date" name="ngay_tu" value="{date_val(r[8])}">
          </div>
        </div>
        <div class="form-row cols-2">
          <div class="form-group">
            <label>Loại thanh toán</label>
            <select name="loai_tt">{tt_opts}</select>
          </div>
          <div class="form-group">
            <label>Trạng thái</label>
            <select name="trang_thai">{status_opts}</select>
          </div>
        </div>
      </div>

      <div style="display:flex;gap:10px;margin-top:4px">
        <button type="submit" class="btn btn-primary">💾 Cập nhật</button>
        <a href="/contracts" class="btn btn-ghost">↩ Quay lại</a>
      </div>
    </form>
    """
    return page("Sửa hợp đồng", content, active="contracts")


if __name__ == "__main__":
    app.run(debug=True)