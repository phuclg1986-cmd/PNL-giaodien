from flask import Flask, render_template_string, request, redirect
from decimal import Decimal
import pyodbc

app = Flask(__name__)

import os
import sqlite3
import pyodbc

def get_conn():
    # chạy trên Render
    if os.getenv("RENDER"):
        conn = sqlite3.connect("erp.db")
        conn.row_factory = sqlite3.Row
        return conn

    # chạy local SQL Server
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=PHUCLG\\PHUCLG;"
        "DATABASE=PNL;"
        "UID=phuclg;"
        "PWD=Phucngoc123@;"
    )
def init_sqlite():
    conn = sqlite3.connect("erp.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS KhachHang(
        KhachHangID INTEGER PRIMARY KEY AUTOINCREMENT,
        MaKhachHang TEXT,
        TenKhachHang TEXT,
        MaSoThue TEXT,
        DienThoai TEXT,
        Email TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS HopDong(
        HopDongID INTEGER PRIMARY KEY AUTOINCREMENT,
        SoHopDong TEXT,
        KhachHangID INTEGER,
        NgayKy TEXT,
        NgayBatDau TEXT,
        NgayKetThuc TEXT,
        TongTien REAL,
        TienTamUng REAL,
        NgayTamUng TEXT,
        LoaiThanhToan TEXT,
        TrangThai TEXT
    )
    """)

    conn.commit()
    conn.close()
    # 👇 PHẢI CÓ ĐOẠN NÀY
if os.getenv("RENDER"):
    init_sqlite()

# ================= DASHBOARD =================
DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>ERP DASHBOARD</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body{background:#eef2f7;}
.sidebar{
    height:100vh;
    background:linear-gradient(180deg,#0f172a,#111827);
    color:white;
    padding:20px;
}
.sidebar a{
    display:block;
    color:#cbd5e1;
    padding:10px;
    text-decoration:none;
    border-radius:8px;
    margin-bottom:5px;
}
.sidebar a:hover{background:#1f2937;}
.topbar{
    background:white;
    padding:15px;
    border-radius:12px;
    margin-bottom:20px;
}
.card-box{
    background:white;
    padding:20px;
    border-radius:16px;
    box-shadow:0 2px 10px rgba(0,0,0,0.06);
}
.c1{background:linear-gradient(135deg,#3b82f6,#60a5fa);color:white;}
.c2{background:linear-gradient(135deg,#22c55e,#86efac);color:white;}
.c3{background:linear-gradient(135deg,#f59e0b,#fcd34d);color:white;}
.c4{background:linear-gradient(135deg,#ef4444,#f87171);color:white;}
.stat-title{font-size:14px;}
.stat-value{font-size:28px;font-weight:bold;}
</style>
</head>

<body>
<div class="container-fluid">
<div class="row">

<div class="col-2 sidebar">
<h4>⚙ ERP SYSTEM</h4>
<hr>
<a href="/">📊 Dashboard</a>
<a href="/customers">👤 Khách hàng</a>
<a href="/contracts">📄 Hợp đồng</a>
</div>

<div class="col-10 p-4">

<div class="topbar">
<h3>📊 Dashboard</h3>
<small>Hệ thống ERP mini</small>
</div>

<div class="row g-3">

<div class="col-md-3">
<div class="card-box c1">
<div class="stat-title">Khách hàng</div>
<div class="stat-value">ERP</div>
</div>
</div>

<div class="col-md-3">
<div class="card-box c2">
<div class="stat-title">Hợp đồng</div>
<div class="stat-value">READY</div>
</div>
</div>

<div class="col-md-3">
<div class="card-box c3">
<div class="stat-title">Thu tiền</div>
<div class="stat-value">OK</div>
</div>
</div>

<div class="col-md-3">
<div class="card-box c4">
<div class="stat-title">Quản trị</div>
<div class="stat-value">LIVE</div>
</div>
</div>

</div>

</div>
</div>
</div>
</body>
</html>
"""

# ================= CUSTOMERS =================
CUSTOMERS_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Khách hàng</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body{background:#f1f5f9;}
.sidebar{
    height:100vh;
    background:#0f172a;
    color:white;
    padding:20px;
}
.sidebar a{
    display:block;
    color:#cbd5e1;
    padding:10px;
    text-decoration:none;
}
.sidebar a:hover{background:#1e293b;}
.content{padding:20px;}
.card-box{
    background:white;
    padding:20px;
    border-radius:14px;
}
thead{
    background:#0f172a;
    color:white;
}
</style>
</head>

<body>
<div class="container-fluid">
<div class="row">

<div class="col-2 sidebar">
<h4>⚙ ERP</h4>
<hr>
<a href="/">📊 Dashboard</a>
<a href="/customers">👤 Khách hàng</a>
<a href="/contracts">📄 Hợp đồng</a>
</div>

<div class="col-10 content">

<h2>👤 Danh sách khách hàng</h2>

<button class="btn btn-primary mb-3"
onclick="document.getElementById('popup').style.display='block'">
➕ Thêm mới
</button>

<div class="card-box">
<table class="table table-bordered table-hover">

<thead>
<tr>
<th>ID</th>
<th>Mã KH</th>
<th>Tên</th>
<th>MST</th>
<th>Điện thoại</th>
<th>Email</th>
<th>Xóa</th>
<th>EIDT</th>
</tr>
</thead>

<tbody>
{% for r in customers %}
<tr>
<td>{{r[0]}}</td>
<td>{{r[1]}}</td>
<td>{{r[2]}}</td>
<td>{{r[3]}}</td>
<td>{{r[4]}}</td>
<td>{{r[5]}}</td>
<td>
<a href="/customers/delete/{{r[0]}}" class="btn btn-danger btn-sm"
onclick="return confirm('Xóa khách hàng này?')">🗑 Xóa</a>
</td>
<td>
<a href="/customers/edit/{{r[0]}}"
class="btn btn-warning btn-sm">
✏ Sửa
</a>
</td>
</tr>
{% endfor %}
</tbody>

</table>
</div>
</div>
</div>
</div>

<div id="popup" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.5);">
<div style="width:450px;background:white;margin:80px auto;padding:20px;border-radius:12px;">

<h4>➕ Thêm khách hàng</h4>

<form method="POST">
<input name="ma_kh" class="form-control mb-2" placeholder="Mã khách hàng" required>
<input name="ten_kh" class="form-control mb-2" placeholder="Tên khách hàng" required>
<input name="mst" class="form-control mb-2" placeholder="Mã số thuế">
<input name="dt" class="form-control mb-2" placeholder="Điện thoại">
<input name="email" class="form-control mb-2" placeholder="Email">

<button class="btn btn-success">💾 Lưu</button>
<button type="button" class="btn btn-danger"
onclick="document.getElementById('popup').style.display='none'">❌ Đóng</button>
</form>

</div>
</div>

</body>
</html>
"""
# ================= Eidt CUSTOMERS =================

EDIT_CUSTOMER_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Sửa</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body style="background:#eef2f7">

<div class="container mt-5">
<div class="card shadow p-4">

<h2>✏Sửa</h2>
<hr>

<form method="POST">

<label>Mã khách hàng</label>
<input name="ma_kh" value="{{row[1]}}" class="form-control mb-3">

<label>Tên khách hàng</label>
<input name="ten_kh" value="{{row[2]}}" class="form-control mb-3">

<label>Mã số thuế</label>
<input name="mst" value="{{row[3]}}" class="form-control mb-3">

<label>Điện thoại</label>
<input name="dt" value="{{row[4]}}" class="form-control mb-3">

<label>Email</label>
<input name="email" value="{{row[5]}}" class="form-control mb-3">

<button class="btn btn-success">💾 Cập nhật</button>
<a href="/customers" class="btn btn-secondary">↩ Quay lại</a>

</form>

</div>
</div>

</body>
</html>
"""

# ================= CONTRACT =================
CONTRACT_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Hợp đồng ERP</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body{background:#eef2f7;font-family:Arial;}
.sidebar{
    min-height:100vh;
    background:linear-gradient(180deg,#0f172a,#111827);
    color:white;
    padding:20px;
}
.sidebar a{
    display:block;
    color:#cbd5e1;
    padding:11px 12px;
    text-decoration:none;
    border-radius:10px;
    margin-bottom:6px;
}
.sidebar a:hover{background:#1f2937;color:white;}

.content{padding:22px;}

.header-box{
    background:white;
    padding:18px 22px;
    border-radius:14px;
    margin-bottom:18px;
    display:flex;
    justify-content:space-between;
    align-items:center;
    box-shadow:0 4px 14px rgba(0,0,0,.05);
}

.box{
    background:white;
    padding:20px;
    border-radius:14px;
    box-shadow:0 4px 14px rgba(0,0,0,.05);
}

.table thead th{
    text-align:center;
    vertical-align:middle;
}

.table tbody td{
    vertical-align:middle;
}

.money{
    font-weight:bold;
    color:#16a34a;
}

.badge-run{background:#2563eb;}

.btn-sm{
    border-radius:8px;
    padding:4px 10px;
}

.modal-bg{
    display:none;
    position:fixed;
    top:0;left:0;
    width:100%;
    height:100%;
    background:rgba(0,0,0,.55);
    z-index:999;
}

.modal-box{
    width:1150px;
    max-width:95%;
    background:white;
    margin:35px auto;
    padding:24px;
    border-radius:18px;
}

.group-box{
    border:1px solid #e5e7eb;
    border-radius:14px;
    padding:18px;
    margin-bottom:16px;
}

.group-box h6{
    font-weight:bold;
    margin-bottom:14px;
}

label{
    font-size:13px;
    font-weight:600;
    margin-bottom:4px;
}

.form-control,.form-select{
    border-radius:10px;
    height:42px;
}

textarea.form-control{
    height:auto;
}
</style>
</head>

<body>

<div class="container-fluid">
<div class="row">

<div class="col-md-2 sidebar">
<h4>⚙ ERP</h4>
<hr>
<a href="/">📊 Dashboard</a>
<a href="/customers">👤 Khách hàng</a>
<a href="/contracts">📄 Hợp đồng</a>
</div>

<div class="col-md-10 content">

<div class="header-box">
<div>
<h4 class="mb-1">📄 Danh sách hợp đồng</h4>
<small class="text-muted">Quản lý hợp đồng khách hàng</small>
</div>

<button class="btn btn-primary px-4"
onclick="document.getElementById('modal').style.display='block'">
➕ Thêm hợp đồng
</button>
</div>

<div class="box">

<div class="table-responsive">

<table class="table table-bordered table-hover">
<thead class="table-dark">
<tr>
<th>ID</th>
<th>Số HĐ</th>
<th>Khách hàng</th>
<th>Ngày ký</th>
<th>Bắt đầu</th>
<th>Kết thúc</th>
<th>Tổng tiền</th>
<th>Tạm ứng</th>
<th>Trạng thái</th>
<th width="170">Trạng thái</th>
<th width="170">Thao tác</th>

</tr>
</thead>

<tbody>

{% for r in rows %}
<tr>
<td class="text-center">{{r[0]}}</td>
<td>{{r[1]}}</td>
<td>{{r[2]}}</td>
<td>{{r[3]}}</td>
<td>{{r[4]}}</td>
<td>{{r[5]}}</td>
<td>{{r[6]}}</td>
<td class="money text-end">{{r[7]}}</td>
<td class="text-end">{{r[8]}}</td>

<td class="text-center">
<span class="badge badge-run">{{r[9]}}</span>
</td>

<td class="text-center">

<a href="/contracts/edit/{{r[10]}}"
class="btn btn-warning btn-sm">
✏ Edit
</a>

<a href="/contracts/delete/{{r[10]}}"
class="btn btn-danger btn-sm"
onclick="return confirm('Xóa hợp đồng này?')">
🗑 Delete
</a>

</td>

</tr>
{% endfor %}

</tbody>
</table>

</div>
</div>

</div>
</div>
</div>

<!-- MODAL THÊM -->
<div id="modal" class="modal-bg">
<div class="modal-box">

<h4 class="mb-3">📄 Thêm hợp đồng mới</h4>

<form method="POST">

<div class="group-box">
<h6>Thông tin chung</h6>

<div class="row">

<div class="col-md-3">
<label>Số hợp đồng</label>
<input name="so_hd" class="form-control mb-3">
</div>

<div class="col-md-5">
<label>Tên hợp đồng</label>
<input name="ten_hd" class="form-control mb-3">
</div>

<div class="col-md-4">
<label>Khách hàng</label>
<select name="kh_id" class="form-select mb-3">
<option value="">-- Chọn khách hàng --</option>
{% for c in customers %}
<option value="{{c[0]}}">{{c[1]}}</option>
{% endfor %}
</select>
</div>

</div>
</div>

<div class="group-box">
<h6>Thời gian</h6>

<div class="row">

<div class="col-md-4">
<label>Ngày ký</label>
<input type="date" name="ngay_ky" class="form-control mb-3">
</div>

<div class="col-md-4">
<label>Ngày bắt đầu</label>
<input type="date" name="ngay_bd" class="form-control mb-3">
</div>

<div class="col-md-4">
<label>Ngày kết thúc</label>
<input type="date" name="ngay_kt" class="form-control mb-3">
</div>

</div>
</div>

<div class="group-box">
<h6>Tài chính</h6>

<div class="row">

<div class="col-md-4">
<label>Tổng tiền</label>
<input name="tong_tien" class="form-control mb-3">
</div>

<div class="col-md-4">
<label>Tạm ứng</label>
<input name="tam_ung" class="form-control mb-3">
</div>

<div class="col-md-4">
<label>Loại thanh toán</label>
<select name="loai_tt" class="form-select mb-3">
<option value="MONTH">Theo tháng</option>
<option value="YEAR">Theo năm</option>
<option value="ONCE">Một lần</option>
</select>
</div>

</div>
</div>

<button class="btn btn-success px-4">💾 Lưu hợp đồng</button>

<button type="button"
class="btn btn-danger px-4"
onclick="document.getElementById('modal').style.display='none'">
❌ Đóng
</button>

</form>

</div>
</div>

</body>
</html>
"""


EDIT_CONTRACT_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Sửa hợp đồng</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>

<body style="background:#eef2f7">

<div class="container mt-5">
<div class="card shadow p-4">

<h3>✏ Sửa hợp đồng</h3>
<hr>

<form method="POST">
    <label for="so_hd">Số hợp đồng</label>
    <input name="so_hd" value="{{ row[1] }}" class="form-control mb-3">

    <label for="kh_id">Khách hàng</label>
    <select name="kh_id" class="form-control mb-3">
        {% for c in customers %}
            <option value="{{ c[0] }}" {% if c[0] == row[2] %} selected {% endif %}>
                {{ c[1] }}
            </option>
        {% endfor %}
    </select>

    <label for="ngay_ky">Ngày ký</label>
    <input type="date" name="ngay_ky" value="{{ row[3] }}" class="form-control mb-3">

    <label for="ngay_bd">Ngày bắt đầu</label>
    <input type="date" name="ngay_bd" value="{{ row[4] }}" class="form-control mb-3">

    <label for="ngay_kt">Ngày kết thúc</label>
    <input type="date" name="ngay_kt" value="{{ row[5] }}" class="form-control mb-3">

    <label for="tong_tien">Tổng tiền</label>
    <input name="tong_tien" value="{{ row[6] }}" class="form-control mb-3"> <!-- row[6] cho Tổng tiền -->

    <label for="tam_ung">Tạm ứng</label>
    <input name="tam_ung" value="{{ row[7] }}" class="form-control mb-3"> <!-- row[7] cho Tạm ứng -->

    <button class="btn btn-success">💾 Cập nhật</button>
    <a href="/contracts" class="btn btn-secondary">↩ Quay lại</a>
</form>

</div>
</div>

</body>
</html>
"""

# ================= ROUTES =================

@app.route("/")
def home():
    return DASHBOARD


@app.route("/customers", methods=["GET", "POST"])
def customers():

    if request.method == "POST":
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO KhachHang
        (MaKhachHang, TenKhachHang, MaSoThue, DienThoai, Email)
        VALUES (?, ?, ?, ?, ?)
        """,
        request.form.get("ma_kh"),
        request.form.get("ten_kh"),
        request.form.get("mst"),
        request.form.get("dt"),
        request.form.get("email"))

        conn.commit()
        conn.close()

        return redirect("/customers")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT KhachHangID, MaKhachHang, TenKhachHang, MaSoThue, DienThoai, Email
    FROM KhachHang
    ORDER BY KhachHangID DESC
    """)

    rows = cur.fetchall()
    conn.close()

    return render_template_string(CUSTOMERS_HTML, customers=rows)


@app.route("/customers/delete/<int:id>")
def delete_customer(id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM KhachHang WHERE KhachHangID=?", id)

    conn.commit()
    conn.close()

    return redirect("/customers")

@app.route("/customers/edit/<int:id>", methods=["GET","POST"])
def edit_customer(id):

    conn = get_conn()
    cur = conn.cursor()

    if request.method == "POST":

        cur.execute("""
        UPDATE KhachHang
        SET MaKhachHang=?,
            TenKhachHang=?,
            MaSoThue=?,
            DienThoai=?,
            Email=?
        WHERE KhachHangID=?
        """,
        request.form.get("ma_kh"),
        request.form.get("ten_kh"),
        request.form.get("mst"),
        request.form.get("dt"),
        request.form.get("email"),
        id)

        conn.commit()
        conn.close()

        return redirect("/customers")

    cur.execute("""
    SELECT KhachHangID,
           MaKhachHang,
           TenKhachHang,
           MaSoThue,
           DienThoai,
           Email
    FROM KhachHang
    WHERE KhachHangID=?
    """, id)

    row = cur.fetchone()

    conn.close()

    return render_template_string(EDIT_CUSTOMER_HTML, row=row)


@app.route("/contracts", methods=["GET", "POST"])
def contracts():
    conn = get_conn()
    cur = conn.cursor()

    # ================= THÊM MỚI =================
    if request.method == "POST":
        cur.execute("""
        INSERT INTO HopDong
        (
            SoHopDong,
            KhachHangID,
            NgayKy,
            NgayBatDau,
            NgayKetThuc,
            TongTien,
            TienTamUng,
            NgayTamUng,
            LoaiThanhToan,
            TrangThai
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        request.form.get("so_hd"),
        request.form.get("kh_id"),
        request.form.get("ngay_ky"),
        request.form.get("ngay_bd"),
        request.form.get("ngay_kt"),
        request.form.get("tong_tien"),
        request.form.get("tam_ung"),
        request.form.get("ngay_tu"),
        request.form.get("loai_tt"),
        "DRAFT")

        conn.commit()
        conn.close()

        return redirect("/contracts")

    # ================= LOAD DATA =================
    cur.execute("SELECT KhachHangID, TenKhachHang FROM KhachHang")
    customers = cur.fetchall()

    cur.execute("""
    SELECT HopDongID,
               SoHopDong,
               KhachHangID,
               NgayKy,
               NgayBatDau,
               NgayKetThuc,
               TongTien,
               TienTamUng,
               NgayTamUng,
               LoaiThanhToan,
               TrangThai
    FROM HopDong
    ORDER BY HopDongID DESC
    """)

    data = cur.fetchall()
    rows = []

    # Duyệt qua mỗi bản ghi trong data và format các cột
    for r in data:
        print(r)  # In ra để kiểm tra dữ liệu
        r = list(r)  # Chuyển tuple thành list để có thể sửa đổi

        # Format Tổng tiền (cột 6)
        if r[6] is not None:
            total_money = float(r[6]) if isinstance(r[6], Decimal) else r[6]
            r[6] = format(int(total_money or 0), ",").replace(",", ".")

        # Format Tạm ứng (cột 7)
        if r[7] is not None:
            advance_money = float(r[7]) if isinstance(r[7], Decimal) else r[7]
            r[7] = format(int(advance_money or 0), ",").replace(",", ".")

        rows.append(r)

    conn.close()  # Đảm bảo conn.close() không bị thụt lề sai

    # Trả về template đã render với dữ liệu
    return render_template_string(
        CONTRACT_HTML,
        customers=customers,
        rows=rows
    )
@app.route("/contracts/delete/<int:id>")
def delete_contract(id):

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM HopDong WHERE HopDongID=?", id)

    conn.commit()
    conn.close()

    return redirect("/contracts")
@app.route("/contracts/edit/<int:id>", methods=["GET", "POST"])
def edit_contract(id):
    conn = get_conn()
    cur = conn.cursor()

    # ================= LẤY DỮ LIỆU KHÁCH HÀNG =================
    cur.execute("SELECT KhachHangID, TenKhachHang FROM KhachHang")
    customers = cur.fetchall()  # Lấy tất cả khách hàng từ cơ sở dữ liệu

    # ================= UPDATE =================
    if request.method == "POST":
        so_hd = request.form.get("so_hd")
        kh_id = request.form.get("kh_id")
        ngay_ky = request.form.get("ngay_ky")
        ngay_bd = request.form.get("ngay_bd")
        ngay_kt = request.form.get("ngay_kt")
        tong_tien = request.form.get("tong_tien")
        tam_ung = request.form.get("tam_ung")
        loai_tt = request.form.get("loai_tt")
        trang_thai = request.form.get("trang_thai")
        ngay_tu = request.form.get("ngay_tu")

        # Loại bỏ dấu phân cách ngàn (nếu có) trước khi chuyển thành số
        if tong_tien:
            tong_tien = tong_tien.replace(".", "")  # Loại bỏ dấu phân cách ngàn
        if tam_ung:
            tam_ung = tam_ung.replace(".", "")  # Loại bỏ dấu phân cách ngàn

        # Kiểm tra và xử lý giá trị Tổng tiền và Tạm ứng
        try:
            tong_tien = float(tong_tien) if tong_tien else None  # Chuyển đổi Tổng tiền thành float nếu có giá trị
            tam_ung = float(tam_ung) if tam_ung else None  # Chuyển đổi Tạm ứng thành float nếu có giá trị
        except ValueError:
            # Nếu không thể chuyển đổi giá trị, gán về None
            tong_tien = None
            tam_ung = None

        # Cập nhật hợp đồng trong cơ sở dữ liệu
        cur.execute("""
        UPDATE HopDong
        SET SoHopDong      = ?,
            KhachHangID    = ?,
            NgayKy         = ?,
            NgayBatDau     = ?,
            NgayKetThuc    = ?,
            TongTien       = ?,
            TienTamUng     = ?,
            NgayTamUng     = ?,
            LoaiThanhToan  = ?,
            TrangThai      = ?
        WHERE HopDongID = ?
        """,
        so_hd, kh_id, ngay_ky, ngay_bd, ngay_kt, tong_tien, tam_ung, ngay_tu, loai_tt, trang_thai, id)

        conn.commit()

    # ================= LOAD DATA =================
    cur.execute("""
    SELECT HopDongID,
               SoHopDong,
               KhachHangID,
               NgayKy,
               NgayBatDau,
               NgayKetThuc,
               TongTien,
               TienTamUng,
               NgayTamUng,
               LoaiThanhToan,
               TrangThai
    FROM HopDong
    WHERE HopDongID = ?
    """, id)

    data = cur.fetchall()  # Lấy dữ liệu từ cơ sở dữ liệu
    rows = []

    # Duyệt qua mỗi bản ghi trong data và format các cột
    for r in data:
        r = list(r)  # Chuyển tuple thành list để có thể sửa đổi

        # Format Tổng tiền (cột 6)
        if r[6] is not None:
            total_money = float(r[6]) if isinstance(r[6], Decimal) else r[6]
            r[6] = format(int(total_money or 0), ",").replace(",", ".")

        # Format Tạm ứng (cột 7)
        if r[7] is not None:
            advance_money = float(r[7]) if isinstance(r[7], Decimal) else r[7]
            r[7] = format(int(advance_money or 0), ",").replace(",", ".")

        rows.append(r)

    conn.close()  # Đảm bảo đóng kết nối sau khi xử lý

    # Trả về template đã render với dữ liệu
    return render_template_string(
        EDIT_CONTRACT_HTML,
        row=rows[0],  # Trả về bản ghi đầu tiên
        customers=customers  # Truyền danh sách khách hàng vào form
    )
if __name__ == "__main__":
    if os.getenv("RENDER"):
        init_sqlite()

    app.run(debug=True)