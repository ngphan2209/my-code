# Hệ chuyên gia tư vấn địa điểm du lịch Đồng bằng sông Cửu Long

Ứng dụng desktop Python/PyQt6, dùng 30 địa điểm, 435 luật nguồn, 30 ảnh minh họa và hai nền đã cung cấp. Có file Qt Designer thật tại `ui/main.ui`, nạp trực tiếp bằng `PyQt6.uic.loadUi`. Không cần tài khoản, mạng, máy chủ, SQL hay dịch vụ AI khi chạy.

## 1. Chạy trên Windows và VS Code

Đã kiểm thử với Python 3.12.14, PyQt6 6.12.0, Qt 6.12.0 và python-docx 1.2.0 trên Linux. Khuyến nghị Python 3.12 bản 64 bit trên Windows. Bản bàn giao không chứa môi trường ảo của dự án cũ.

1. Giải nén ZIP, mở thư mục `mekong_expert` trong VS Code bằng **File → Open Folder**. Thư mục này phải có `main.py`.
2. Mở Terminal → New Terminal, chạy:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Nhấn `Ctrl+Shift+P` → **Python: Select Interpreter** → chọn `.venv\Scripts\python.exe`. Nếu chưa có lệnh này, cài extension Python của Microsoft cho VS Code.
4. Mở terminal mới, kích hoạt môi trường:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

Nếu PowerShell chặn Activate.ps1, không cần đổi chính sách máy. Chạy trực tiếp:

```powershell
.\.venv\Scripts\python.exe main.py
```

Cài thư viện lần đầu có thể cần Internet; sử dụng ứng dụng sau đó không cần mạng. Không cài PyQt5-tools cho dự án này. `python-docx` dùng cho công cụ nhập lại Word, không tham gia suy luận.

## 2. Cách sử dụng

- **Bắt đầu tư vấn**: chuyển sang trang có bảy tiêu chí. Mỗi nhóm phải chọn một mục.
- **Tư vấn**: lấy mã bằng `currentData()`, duyệt toàn bộ luật và liệt kê mọi địa điểm khớp hoàn toàn theo thứ tự T.
- Chọn một địa điểm trong danh sách để xem ảnh và mô tả. Mở thẻ **Lý do đề xuất / luật** để xem số luật, biểu thức và nhãn tương ứng với từng mã.
- Thẻ **Video** dùng khung ngang 16:9, tự điều chỉnh theo cửa sổ và giữ nguyên tỉ lệ video gốc.
- Kết quả đầu tiên được chọn tự động. Thay đổi tiêu chí sẽ xóa kết quả cũ; bấm Tư vấn để tính lại.
- **Xóa** xóa cả bảy mục, danh sách, ảnh, mô tả và giải thích. **Trang chủ** chỉ chuyển trang, không tạo thêm cửa sổ.
- Kéo vạch chia để đổi độ rộng danh sách, ảnh và khu vực nhập. Khi cửa sổ thấp, cuộn vùng tiêu chí; các nút thao tác luôn ở ngoài vùng cuộn. Nhãn dài có tooltip trong danh sách chọn.

Ví dụ thử nhanh:

| Bộ mã | Kết quả bắt buộc |
| --- | --- |
| R1 K1 N1 V1 L3 DT1 TG2 | T1 – Làng du lịch Mỹ Khánh |
| R3 K2 N2 V5 L7 DT5 TG2 | T5 và T6 |
| R3 K3 N2 V9 L5 DT3 TG2 | T8 và T9 |
| R6 K4 N4 V20 L1 DT6 TG4 | Không có kết quả |

Tra nhãn tương ứng trong `data/events.json`. Không có kết quả sẽ báo đúng: “Chưa có địa điểm phù hợp hoàn toàn với các lựa chọn trong cơ sở tri thức.”

## 3. Cấu trúc và trách nhiệm

| Tệp | Trách nhiệm |
| --- | --- |
| `main.py` | Tạo ứng dụng, cấu hình logging, kiểm tra dữ liệu, mở cửa sổ, báo lỗi khởi động |
| `app/main_window.py` | Nạp UI, nối tín hiệu, nhận mã, gọi suy luận, hiển thị ảnh và kết quả |
| `app/knowledge.py` | Đọc UTF-8 JSON, kiểm tra chung, phân biệt lỗi và cảnh báo |
| `app/inference.py` | Suy luận chính xác, không import PyQt hay thao tác widget |
| `ui/main.ui` | QMainWindow, QStackedWidget hai trang, layout và widget thật |
| `data/events.json` | 81 mã gồm 51 mã đầu vào và T1–T30, nhãn và nhóm |
| `data/destinations.json` | Tên, mô tả, đường dẫn ảnh và chú thích nguồn |
| `data/rules.json` | 435 luật với ID, conditions, result, lời văn và biểu thức nguồn |
| `assets/backgrounds/` | home.png là nền sảnh, consult.png là nền tư vấn |
| `assets/destinations/` | 30 ảnh trích xuất từ DOCX theo quan hệ đoạn và chú thích |
| `tools/import_sources.py` | Nhập lại hai Word, trích ảnh, gọi bộ kiểm tra chung, tạo báo cáo nhập |
| `tools/check_knowledge.py` | Kiểm tra JSON, cảnh báo nguồn và thử kết luận cho từng luật |
| `tests/test_inference.py` | Các ca suy luận dương, âm, nhiều kết quả và luật trùng |
| `tests/test_knowledge.py` | Dữ liệu hợp lệ và các lỗi cấu trúc/tham chiếu/nhóm |
| `tests/test_gui.py` | Kiểm tra widget Qt thật: điều hướng, tư vấn, chọn ảnh, xóa, resize |
| `reports/` | Kiểm kê nguồn, quan hệ ảnh, cảnh báo tri thức và kết quả kiểm thử |

Đường dẫn dữ liệu được tính từ vị trí dự án bằng pathlib, không dựa vào thư mục terminal. Có thể chạy bằng đường dẫn đầy đủ đến `main.py` khi terminal đang ở thư mục khác.

## 4. Mở và sửa giao diện bằng Qt Designer

Dùng **Qt Designer cho Qt 6**, chọn **File → Open** → `ui/main.ui`. Preview bằng **Form → Preview** hoặc `Ctrl+R`. Sau khi sửa, Save và chạy lại ứng dụng. Không cần chạy pyuic6 hay sinh file giao diện Python.

PyQt6 trong requirements không tự kèm chương trình Designer. Nếu máy chưa có Designer, có thể cài công cụ Designer đi kèm PySide6 vào môi trường riêng, chỉ để mở/sửa UI:

```powershell
py -3.12 -m venv .designer-venv
.\.designer-venv\Scripts\python.exe -m pip install PySide6
.\.designer-venv\Scripts\pyside6-designer.exe ui\main.ui
```

Môi trường phụ này không dùng chạy ứng dụng. Ứng dụng vẫn hoàn toàn dùng PyQt6; không thêm PySide6 vào requirements. `.ui` dùng widget chuẩn của Qt 6, tương thích cả hai binding. Xem tài liệu công cụ: https://doc.qt.io/qtforpython-6/tools/pyside-designer.html

Giữ đúng objectName của các widget đang được Python sử dụng, đặc biệt bảy combobox và các nút/khu vực kết quả đã nêu trong yêu cầu. Muốn đổi tên phải sửa cả tham chiếu trong `main_window.py`. Dùng layout để thêm widget. Không thay widget chuẩn bằng widget tùy biến nếu chưa bổ sung cách nạp.

Các mục trong combobox được lấy từ JSON lúc chạy nên không hiện đầy đủ trong Preview của Designer. Hai nền được Python áp dụng theo kích thước trang; trong Designer có thể chỉ thấy nền màu. Toàn bộ widget, trang, layout và style chính vẫn nằm trong `.ui`.

## 5. Sửa cơ sở tri thức

JSON lưu UTF-8, dùng dấu nháy kép, không có comment hay dấu phẩy cuối danh sách. Sao lưu trước khi sửa.

- `events.json`: mỗi dòng dữ liệu là đối tượng có `code`, `label`, `group`. Ví dụ `{"code":"K1","label":"Không quá 30 km","group":"K"}`. Giữ các nhóm R1–R6, K1–K4, N1–N4, V1–V20, L1–L7, DT1–DT6, TG1–TG4 và T1–T30. Nếu thật sự đổi phạm vi mã, phải điều chỉnh GROUPS/bộ kiểm tra và cập nhật nguồn, kiểm thử.
- `destinations.json`: sửa `name`, `description`, `image` khi có nguồn xác nhận. Đường dẫn ảnh tương đối từ thư mục dự án, ví dụ `assets/destinations/T1.jpeg`. Chỉ thêm `address` khi có tài liệu tương ứng; bản này không tự dựng địa chỉ. Không dùng đường dẫn ổ C của máy cá nhân.
- `rules.json`: mỗi luật có ID nguyên dương duy nhất, bảy điều kiện thuộc bảy nhóm khác nhau, result là T hợp lệ. `source_text` và `source_formula` giữ nguyên từ nguồn. Bộ kiểm tra phát hiện conditions/result không khớp source_formula. Muốn thay luật chính thức cần sửa bản nguồn được duyệt rồi nhập lại để tránh mất dấu đối chiếu.
- Không tự ghép thêm tổ hợp thuộc tính, không suy diễn giá cao bao hàm giá thấp. Một luật chỉ khớp khi cả bảy mã đều có trong đầu vào.

Nhập lại từ nguồn khi cần, thay các đường dẫn mẫu bằng đường dẫn thật tới Word trên máy bạn:

```powershell
python tools/import_sources.py --rules "D:\TaiLieu\tap luat-sk 30 dia diem(1).docx" --places "D:\TaiLieu\minh hoa 30 dia diem(2).docx" --backgrounds "D:\TaiLieu"
python tools/check_knowledge.py --report
```

`--backgrounds` không bắt buộc. Thư mục này chỉ nên có một bản mỗi nền tên `nền sảnh*.png` và `nền tư vấn*.png`. Nếu có nhiều bản, công cụ dừng để bạn chọn rõ nguồn. Công cụ nhập sẽ ghi đè ba JSON, ảnh T tương ứng và báo cáo nhập; hãy sao lưu chỉnh sửa tay. Không cần giải nén RAR để chạy hoặc nhập lại: RAR cũ chỉ được đọc tham khảo, không phải nguồn dữ liệu mới. Bản ZIP không đóng lại các tài liệu nguồn; bạn giữ các bản đã cung cấp riêng.

Nếu ảnh trong Word không có đúng một ảnh và một chú thích cùng số trong mỗi khối T, công cụ dừng, yêu cầu đối chiếu thủ công. Không mặc định image1 tương ứng T1.

## 6. Kiểm tra và kiểm thử

Từ thư mục dự án:

```powershell
python tools/check_knowledge.py --report
python -m unittest discover -s tests -v
```

Công cụ check trả exit code 1 khi có lỗi chặn chạy; cảnh báo đơn thuần trả 0. `--report` cập nhật `reports/knowledge_audit.md`. Kiểm thử tạo đối tượng dữ liệu sai trong bộ nhớ hoặc thư mục tạm, không sửa dữ liệu thật.

Nếu chỉ muốn chạy logic và dữ liệu, không mở cửa sổ:

```powershell
python -m unittest discover -s tests -p test_inference.py -v
python -m unittest discover -s tests -p test_knowledge.py -v
```

Chạy Qt không màn hình trong PowerShell:

```powershell
$env:QT_QPA_PLATFORM = "offscreen"
python -m unittest discover -s tests -v
Remove-Item Env:QT_QPA_PLATFORM
```

Đã chạy 27 kiểm thử và xác nhận từng luật trong 435 luật suy ra được địa điểm của nó. Sáu kiểm thử giao diện dùng widget Qt thực, nền tảng offscreen; đã render và xem giao diện ở kích thước thường và nhỏ. Không thay thế việc kiểm tra Windows, HiDPI, font và Qt Designer trên máy bạn. Chi tiết ở `reports/validation.md`.

## 7. Log và cách tìm lỗi

Log ưu tiên ghi `logs/app.log`, tự luân chuyển tối đa 2 MB/tệp, giữ ba bản cũ. Nếu thư mục dự án không ghi được, thử `%LOCALAPPDATA%\MekongExpert\logs\app.log`, sau đó thư mục tạm của hệ điều hành `MekongExpert\logs\app.log`. Đường dẫn log thật được in ra terminal và gắn vào tooltip cửa sổ. Mọi vị trí đều ghi không được thì chương trình báo lỗi terminal và dừng.

- **ModuleNotFoundError / không nạp được Qt**: dùng đúng `.venv\Scripts\python.exe`, chạy lại cài requirements bằng chính interpreter này. Chi tiết ImportError có trong log nếu logging đã khởi tạo.
- **Không thể khởi động**: xem dòng ERROR và traceback cuối trong app.log. JSON hỏng có tên tệp; lỗi tham chiếu có số luật/mã; UI thiếu widget sẽ báo tên widget tại traceback. Sửa nguyên nhân rồi chạy check.
- **Ảnh thiếu/không đọc được**: WARNING chứa mã T và đường dẫn. Ứng dụng vẫn hoạt động và hiện “Chưa có ảnh địa điểm”. Check phát hiện tệp ảnh thiếu; GUI thử đọc ảnh có phát hiện thêm ảnh không giải mã được.
- **Không có kết quả**: có thể là tổ hợp chưa tồn tại trong tập luật, không phải lỗi chương trình. Kiểm tra mã trong rules.json; không tự bỏ tiêu chí để ép ra kết quả.
- **Qt platform plugin không nạp được**: lỗi native Qt có thể xảy ra trước khi Python hiển thị thông báo; xem terminal. Đảm bảo không kích hoạt nhầm môi trường cũ/PyQt5 và không đặt QT_PLUGIN_PATH trỏ sang bản Qt khác. Xóa biến QT_QPA_PLATFORM=offscreen khi muốn thấy cửa sổ sau khi kiểm thử.

## 8. Giới hạn và dữ liệu cần xác minh

Bản nguồn thực tế khớp toàn bộ các mốc đã cung cấp: 30 địa điểm, 435 luật liên tục, 13 cặp luật trùng, cặp 75/87 và 114/136 cùng điều kiện nhưng khác địa điểm, 20 luật lời văn khoảng cách khác mã K tại T27–T28. Không có lỗi chặn chạy; có 35 cảnh báo được lưu trong báo cáo.

Suy luận **theo biểu thức mã hóa**, giữ nguyên lời văn nguồn, không tự sửa luật 380 hay 19 luật còn lại. Giải thích hiển thị dùng danh mục mã nên nhất quán với bộ suy luận. Mô tả địa điểm vẫn là văn bản gốc; có thể khác lời văn luật hoặc biểu thức, cần đối chiếu khi hoàn thiện báo cáo. Đây là quy ước kỹ thuật, chưa phải xác minh du lịch thực tế.

Khoảng cách theo trung tâm hành chính đến địa điểm trong tài liệu, không tính từ vị trí người dùng. Ngân sách là người/ngày, chưa gồm lưu trú và đi từ nơi xuất phát. Tên tỉnh, chi phí, khoảng cách và ảnh được giữ theo nguồn đồ án, chưa xác minh thực địa; R6/T27/T28 là phần mở rộng phạm vi cần trình bày rõ. Không có phần trăm phù hợp, trọng số hay tư vấn gần đúng.

Chạy ứng dụng và các công cụ hoàn toàn cục bộ; không gửi dữ liệu hoặc tài liệu lên dịch vụ bên ngoài. Không có chức năng quản trị trực tiếp trong GUI; sửa JSON hoặc nhập lại Word rồi kiểm tra.
