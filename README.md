# Quản lý kết quả học tập sinh viên

Đây là bài thực hành A1 của học phần Lập trình Python. Nhóm xây dựng một trang web để nhập điểm theo môn, tính GPA và tra cứu kết quả của sinh viên. FastAPI xử lý dữ liệu và phục vụ giao diện HTML, CSS, JavaScript. Kết quả được lưu trong một tệp JSON để có thể mở lại sau khi dừng chương trình.

## Chạy dự án

Dự án được phát triển với Python 3.14. Mở PowerShell ở thư mục chứa README này, tạo môi trường ảo và cài thư viện:

```powershell
python --version
python -m venv .\backend\.venv
.\backend\.venv\Scripts\python.exe -m pip install -r .\backend\requirements.txt
```

Sau khi cài xong, chạy ứng dụng từ thư mục chứa mô-đun `main.py`:

```powershell
Set-Location .\backend\main
..\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Khi terminal báo `Application startup complete.`, mở [trang quản lý sinh viên](http://127.0.0.1:8000/web/). Bạn có thể thử từng yêu cầu trên [trang tài liệu API](http://127.0.0.1:8000/docs). Nhấn **Ctrl+C** trong terminal để dừng máy chủ.

## Thử với một sinh viên mẫu

1. Mở **Thêm sinh viên**, nhập MSSV `DEMO001` và họ tên **Đặng Minh Khoa**. Nhập điểm 40% và 60% lần lượt là **7** và **7.25** cho môn Python, **8** và **9** cho môn Cơ sở dữ liệu.
2. Lưu rồi bấm **Xem chi tiết**. Điểm tổng kết hai môn lần lượt là **7.2** và **8.6**, GPA là **7.90**.
3. Chọn **Chỉnh sửa** để thay đổi điểm rồi lưu lại. Mở phần chi tiết hoặc tải lại trang để kiểm tra GPA mới và dữ liệu đã lưu.

Bạn có thể tìm bằng MSSV hoặc một phần họ tên. Chẳng hạn, gõ `dang` để tìm **Đặng Minh Khoa**. Ô sắp xếp cho phép đổi thứ tự GPA. Phần thống kê tính trên toàn bộ nhóm, kể cả khi bảng đang lọc, và hiển thị tất cả sinh viên đồng hạng ở mức GPA cao nhất hoặc thấp nhất.

## Cách tính và lưu điểm

Mỗi sinh viên cần có MSSV, họ tên và ít nhất một môn có tên. Điểm thành phần phải là số từ **0 đến 10**, gồm cả hai đầu mút. Khi gửi JSON, hãy dùng số `8` vì API từ chối chuỗi `"8"` và giá trị `true`. Ứng dụng bỏ khoảng trắng ở đầu và cuối chuỗi, đồng thời kiểm tra trùng MSSV không phân biệt hoa thường.

- **Điểm môn** bằng điểm 40% × 0.4 + điểm 60% × 0.6, làm tròn đến một chữ số thập phân.
- **GPA** là trung bình cộng của các điểm môn đã làm tròn, lấy hai chữ số thập phân trên thang 10. Các môn có trọng số bằng nhau vì bài tập chưa dùng số tín chỉ.

Phần tính toán dùng `Decimal` và quy tắc `ROUND_HALF_UP`. Chẳng hạn, `7 × 0.4 + 7.25 × 0.6 = 7.15` được làm tròn thành `7.2`. JSON có thể lưu GPA dưới dạng số `7.9`. Giao diện định dạng giá trị đó thành `7.90`.

Khi chưa có tệp JSON, danh sách ban đầu rỗng. Lần lưu đầu tiên tạo `backend/data/sinh_vien.json` và ghi dữ liệu bằng UTF-8. Chương trình ghi xong vào tệp tạm rồi thay thế tệp chính. Tệp dữ liệu được bỏ qua trong Git. Nếu tự tạo tệp khi chưa có dữ liệu, hãy ghi `[]` làm nội dung ban đầu.

## Thử API

| Yêu cầu | Công dụng |
| --- | --- |
| `GET /` | Xem thông tin ứng dụng |
| `POST /students/validate` | Kiểm tra dữ liệu đầu vào |
| `POST /students/calculate` | Tính thử điểm môn và GPA |
| `POST /students` | Thêm sinh viên và lưu JSON |
| `GET /students` | Lấy danh sách, tìm kiếm và sắp xếp |
| `PUT /students?mssv_cu=DEMO001` | Cập nhật sinh viên theo MSSV đã lưu |
| `GET /students/statistics` | Xem số sinh viên và GPA cao nhất, thấp nhất, trung bình |

Ví dụ, `GET /students?tu_khoa=dang&thu_tu=tang` lọc các bản ghi khớp với `dang` và xếp GPA từ thấp đến cao. Giá trị mặc định của `thu_tu` là `giam`. Khi chưa có sinh viên, kết quả thống kê trả số lượng `0`, các giá trị GPA là `null` và danh sách đồng hạng là `[]`.

Bạn có thể gửi dữ liệu sau đến `POST /students`. API tự tính `diem_tong_ket` và `gpa`.

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

Tạo thành công trả `201`, cập nhật thành công trả `200`. Nếu đã tạo `DEMO001` ở bước thử giao diện, hãy dùng MSSV khác khi gửi `POST` để tránh mã `409` do trùng. Các mã lỗi khác gồm `404` khi cập nhật một MSSV không tồn tại, `422` cho đầu vào sai và `500` khi có lỗi xử lý hoặc đọc ghi dữ liệu.

## Chạy kiểm thử

Cài thêm `pytest` và `httpx` vào môi trường ảo. Nếu Uvicorn đang chạy, mở một terminal khác ở thư mục gốc dự án:

```powershell
Set-Location .\backend\main
..\.venv\Scripts\python.exe -m pip install pytest httpx
..\.venv\Scripts\python.exe -m pytest -v ..\tests
```

Bộ kiểm thử có **11 ca**, gồm kiểm tra điểm và GPA, kiểm tra API và giả lập lỗi khi lưu. Các ca liên quan đến lưu trữ dùng tệp JSON tạm riêng.

## Tìm mã nguồn

```text
backend/
  main/
    main.py          API và cấu hình phục vụ giao diện
    schemas.py       Cấu trúc dữ liệu và quy tắc kiểm tra
    services.py      Tính điểm, tìm kiếm, sắp xếp, thống kê
    storage.py       Đọc, ghi và cập nhật JSON
  tests/             Kiểm thử điểm, API và lỗi lưu
  requirements.txt  Thư viện cần để chạy ứng dụng
frontend/
  index.html         Giao diện chính
  css/               styles.css và a1-ledger.css
  js/                app.js, student-form.js và student-detail.js
```

Các tệp mang tên tiếng Anh, còn tên hàm và trường dữ liệu chủ yếu dùng tiếng Việt không dấu. Phần Python dùng `try...except` để xử lý ngoại lệ khi đọc, ghi dữ liệu. Giao diện dùng `try...catch` để báo lỗi khi gọi API.

### Khi gặp lỗi

- Nếu Uvicorn báo không tìm thấy mô-đun `main`, kiểm tra terminal đang ở `backend/main`.
- Nếu trang thiếu CSS hoặc nút bấm không hoạt động, kiểm tra đường dẫn trong `index.html` rồi nhấn **Ctrl+F5**.
- Nếu API báo lỗi đọc JSON, kiểm tra cú pháp của tệp và bảo đảm phần ngoài cùng là một danh sách.

