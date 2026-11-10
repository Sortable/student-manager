# Bài A1 — Quản lý kết quả học tập sinh viên

Ứng dụng quản lý kết quả học tập của một nhóm sinh viên, xây dựng bằng Python và FastAPI, có giao diện website và lưu dữ liệu vào file JSON.

## 1. Chức năng

- Nhập thông tin sinh viên và điểm của nhiều môn học.
- Kiểm tra điểm trong khoảng 0–10 và các thông tin bắt buộc.
- Tính điểm tổng kết môn học theo tỷ lệ 40%–60%.
- Tính GPA theo thang 10.
- Lưu và đọc dữ liệu từ file JSON.
- Tìm kiếm theo MSSV hoặc họ tên, không phân biệt hoa/thường và dấu tiếng Việt.
- Sắp xếp sinh viên theo GPA tăng dần hoặc giảm dần.
- Thống kê số sinh viên, GPA cao nhất, thấp nhất và trung bình nhóm.
- Hiển thị đầy đủ sinh viên đồng hạng cao nhất hoặc thấp nhất.
- Xem chi tiết môn học và điểm của từng sinh viên.
- Xử lý lỗi bằng `try...except` ở backend và `try...catch` ở frontend.

## 2. Công nghệ sử dụng

- **Python 3.14:** môi trường phát triển của dự án.
- **FastAPI:** xây dựng API và phục vụ giao diện.
- **Pydantic:** kiểm tra cấu trúc dữ liệu đầu vào.
- **Uvicorn:** chạy ứng dụng.
- **Decimal:** tính toán và làm tròn điểm.
- **HTML, CSS, JavaScript:** xây dựng giao diện và gọi API.
- **JSON:** lưu trữ dữ liệu sinh viên.

Các phiên bản thư viện được ghi trong `backend/requirements.txt`.

## 3. Cấu trúc dự án

```text
student-manager/
├── README.md
├── backend/
│   ├── requirements.txt
│   ├── data/
│   │   └── sinh_vien.json
│   └── main/
│       ├── main.py
│       ├── schemas.py
│       ├── services.py
│       └── storage.py
└── frontend/
    ├── index.html
    ├── styles.css
    ├── app.js
    ├── student-form.js
    └── student-detail.js
```

Vai trò các tệp chính:

| Tệp | Vai trò |
|---|---|
| `main.py` | Khai báo API và cấu hình phục vụ giao diện |
| `schemas.py` | Khai báo các lớp dữ liệu và quy tắc kiểm tra |
| `services.py` | Tính điểm, tìm kiếm, sắp xếp và thống kê |
| `storage.py` | Đọc, ghi JSON và kiểm tra MSSV trùng |
| `app.js` | Hiển thị danh sách, tìm kiếm, sắp xếp và thống kê |
| `student-form.js` | Xử lý biểu mẫu thêm sinh viên và môn học |
| `student-detail.js` | Hiển thị chi tiết kết quả học tập |

Tên tệp dùng tiếng Anh; tên lớp, hàm và các trường dữ liệu chủ yếu dùng tiếng Việt không dấu.

## 4. Cài đặt và chạy

### Thiết lập lần đầu

Mở PowerShell tại **thư mục gốc dự án**, nơi chứa `README.md`.

Kiểm tra Python:

```powershell
python --version
```

Tạo môi trường riêng và cài thư viện:

```powershell
python -m venv backend\.venv
.\backend\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
```

### Chạy chương trình

Từ thư mục gốc dự án:

```powershell
cd .\backend\main
..\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Sau khi xuất hiện `Application startup complete.`, truy cập:

- [Giao diện quản lý sinh viên](http://127.0.0.1:8000/web/)
- [Trang tài liệu và thử API](http://127.0.0.1:8000/docs)
- [Thông tin ứng dụng dạng JSON](http://127.0.0.1:8000/)

Nhấn **Ctrl+C** trong Terminal để dừng chương trình.

Sau khi sửa HTML, CSS hoặc JavaScript, lưu tệp và tải lại trình duyệt. Có thể dùng **Ctrl+F5** để tải lại toàn bộ tài nguyên giao diện.

## 5. Quy tắc xử lý dữ liệu

### Thông tin sinh viên

Mỗi sinh viên có:

- MSSV.
- Họ tên.
- Danh sách môn học.
- GPA.

Mỗi môn có tên môn, điểm 40%, điểm 60% và điểm tổng kết.

### Kiểm tra hợp lệ

- MSSV, họ tên và tên môn phải có nội dung.
- Mỗi sinh viên phải có ít nhất một môn.
- Điểm phải là số trong khoảng **0 đến 10**, gồm cả hai đầu.
- Không chấp nhận điểm dạng chuỗi như `"8"` hoặc boolean như `true`.
- MSSV được kiểm tra trùng không phân biệt hoa/thường.
- Khoảng trắng ở đầu và cuối các chuỗi được loại bỏ.

### Điểm tổng kết môn

```text
Điểm tổng kết = Điểm 40% × 0.4 + Điểm 60% × 0.6
```

Điểm tổng kết làm tròn đến **1 chữ số thập phân**, sử dụng `ROUND_HALF_UP`.

Ví dụ:

```text
7 × 0.4 + 7.25 × 0.6 = 7.15 → 7.2
```

### GPA

GPA dùng **thang 10**, tính bằng trung bình cộng các điểm tổng kết môn đã làm tròn:

```text
GPA = Tổng điểm tổng kết các môn / Số môn
```

GPA làm tròn đến **2 chữ số thập phân**. Các môn có trọng số bằng nhau vì bài tập chưa quy định số tín chỉ.

Ví dụ:

```text
(7.2 + 8.6) / 2 = 7.90
```

### Thống kê nhóm

GPA trung bình nhóm là trung bình cộng GPA của các sinh viên, làm tròn hai chữ số.

Khi nhóm rỗng:

- Số lượng sinh viên là `0`.
- Các giá trị GPA thống kê là `null`.
- Danh sách sinh viên cao nhất và thấp nhất là `[]`.

Thống kê trên website luôn tính toàn nhóm, kể cả khi danh sách đang được lọc theo từ khóa.

## 6. Các API

| Phương thức | Đường dẫn | Chức năng |
|---|---|---|
| GET | `/` | Thông tin ứng dụng |
| POST | `/students/validate` | Kiểm tra dữ liệu sinh viên |
| POST | `/students/calculate` | Tính điểm môn và GPA |
| POST | `/students` | Thêm sinh viên và lưu JSON |
| GET | `/students` | Lấy danh sách, tìm kiếm và sắp xếp |
| GET | `/students/statistics` | Thống kê toàn nhóm |

### Tham số lấy danh sách

| Tham số | Ý nghĩa |
|---|---|
| `tu_khoa` | Tìm chuỗi con trong MSSV hoặc họ tên; có thể bỏ trống |
| `thu_tu=tang` | Sắp xếp GPA tăng dần |
| `thu_tu=giam` | Sắp xếp GPA giảm dần, là lựa chọn mặc định |

Ví dụ:

```text
/students?tu_khoa=nguyen&thu_tu=tang
```

### Dữ liệu mẫu khi thêm sinh viên

Gửi đến `POST /students`:

```json
{
  "mssv": "DEMO001",
  "ho_ten": "Đặng Minh Khoa",
  "danh_sach_mon": [
    {
      "ten_mon": "Python",
      "diem_40": 7,
      "diem_60": 7.25
    },
    {
      "ten_mon": "Cơ sở dữ liệu",
      "diem_40": 8,
      "diem_60": 9
    }
  ]
}
```

API tự tính điểm tổng kết lần lượt là **7.2**, **8.6** và GPA **7.90**.

Người gọi chỉ gửi thông tin đầu vào; các trường `diem_tong_ket` và `gpa` do API tính.

### Mã phản hồi

| Mã | Ý nghĩa |
|---|---|
| 200 | Yêu cầu thành công |
| 201 | Thêm sinh viên thành công |
| 409 | MSSV đã tồn tại |
| 422 | Dữ liệu hoặc tham số không hợp lệ |
| 500 | Lỗi xử lý, đọc hoặc ghi dữ liệu |

## 7. Lưu trữ JSON

Dữ liệu được lưu trong `backend/data/sinh_vien.json`, dưới dạng một danh sách sinh viên, bao gồm cả điểm tổng kết và GPA.

- Nếu file chưa tồn tại, chương trình xem danh sách ban đầu là rỗng và tạo file khi lưu.
- Nếu tự tạo file lúc chưa có dữ liệu, nội dung khởi tạo là:

```json
[]
```

- File rỗng hoàn toàn không phải JSON hợp lệ.
- Dữ liệu được ghi bằng UTF-8 để giữ chữ tiếng Việt.
- Chương trình ghi vào file tạm rồi thay thế file chính khi ghi thành công.
- Nếu JSON hỏng hoặc sai cấu trúc, chương trình báo lỗi.

JSON có thể biểu diễn GPA là `7.9`. Trên giao diện, giá trị được định dạng thành `7.90`. Điểm tổng kết môn luôn hiển thị một chữ số thập phân.

## 8. Kiểm thử thủ công

1. Thêm sinh viên mới với một hoặc nhiều môn học.
2. Đối chiếu điểm tổng kết và GPA với phép tính tay.
3. Thử bỏ trống thông tin, nhập điểm âm hoặc lớn hơn 10.
4. Thử thêm MSSV đã tồn tại.
5. Tìm kiếm bằng MSSV, tên có dấu và tên không dấu.
6. Kiểm tra sắp xếp GPA tăng và giảm.
7. Đối chiếu thống kê với toàn bộ danh sách.
8. Mở chi tiết nhiều sinh viên để kiểm tra đúng dữ liệu.
9. Dừng và chạy lại API, xác nhận dữ liệu vẫn còn.

## 9. Một số lỗi thường gặp

| Hiện tượng | Cách kiểm tra |
|---|---|
| Không nạp được module `main` | Chạy Uvicorn từ thư mục `backend/main` |
| Báo thiếu thư mục `frontend` | Đặt `frontend` ngang cấp với `backend` |
| Website không có CSS | Kiểm tra HTML đang liên kết đúng tệp `styles.css` |
| JavaScript chưa cập nhật | Lưu tệp rồi nhấn Ctrl+F5 |
| API báo lỗi đọc JSON | Kiểm tra cú pháp và cấu trúc file dữ liệu |
| Thêm sinh viên bị lỗi 409 | Sử dụng MSSV chưa tồn tại |