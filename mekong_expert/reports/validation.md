# Kết quả kiểm thử bàn giao

Môi trường thực hiện: Linux, Python 3.12.14, PyQt6/Qt 6.12.0, python-docx 1.2.0. Các kiểm thử Qt chạy với QT_QPA_PLATFORM=offscreen, tạo và thao tác widget thật, không mô phỏng bộ suy luận.

## Kết quả

- `python tools/check_knowledge.py --report`: 0 lỗi chặn chạy, 35 cảnh báo, cả 435 luật suy ra được kết luận nguồn.
- `QT_QPA_PLATFORM=offscreen python -m unittest discover -s tests -v`: 27/27 kiểm thử đạt trên bản cuối cùng.
- 10 kiểm thử suy luận: Mỹ Khánh, T5/T6, T8/T9, không khớp, sáu điều kiện không đủ, không bao hàm ngân sách thấp, luật trùng, giữ đủ ID, đầu vào sai và kiểm tra tất cả luật nguồn.
- 11 kiểm thử cơ sở tri thức: mã không tồn tại, ID trùng, thiếu/lặp nhóm, JSON hỏng/thiếu tệp, thiếu trường, đường dẫn ảnh sai, mã sự kiện trùng, ảnh thiếu/địa điểm không có luật là cảnh báo, khác biểu thức nguồn và các mốc đối chiếu.
- Sáu kiểm thử Qt: mở cửa sổ/chuyển trang/tư vấn/chọn kết quả đầu và thứ hai/xóa/quay lại; lần tư vấn không có kết quả xóa kết quả cũ; chọn thiếu và hướng dẫn; đọc đủ 30 ảnh và hai nền; resize 850×600, 1200×780, 1500×900 và giữ tỷ lệ ảnh; ảnh thiếu có placeholder và log.
- Đã chạy main.py từ thư mục terminal /tmp khác thư mục dự án: cửa sổ khởi tạo và giữ mở, app.log được tạo; kết thúc tiến trình sau kiểm tra khởi động.
- Đã render và xem ảnh trang chủ/trang tư vấn ở 1200×780 và 850×600. Sau điều chỉnh bố cục, các nút thao tác nằm ngoài vùng cuộn tiêu chí. Sau lần sửa XML có phát hiện lỗi tên encoding utf8; đã đổi sang utf-8 và chạy lại đủ 27 kiểm thử đạt.

## Giới hạn kiểm chứng

Chưa chạy trực tiếp trên Windows, chưa mở bằng chương trình Qt Designer riêng. UI đã được nạp trực tiếp thành widget PyQt6 qua uic.loadUi; không có widget tùy biến. Cần kiểm tra thêm trên Windows về font, tỷ lệ HiDPI, hộp thoại native và thao tác Qt Designer.

Bộ kiểm thử có kiểm tra mọi luật nguồn, nhưng không chỉ dựa vào vòng kiểm tra này: còn có các ca dương/âm, nhiều kết quả và biến đổi dữ liệu có chủ đích. Không xác nhận tính đúng thực địa của tỉnh, khoảng cách, chi phí hoặc ảnh. Danh sách cảnh báo và quy ước dùng biểu thức nằm trong knowledge_audit.md.

## Tự kiểm tra trên Windows

1. Mở main.py bằng đúng môi trường ảo; vào trang tư vấn, chọn bảy mục theo ví dụ Mỹ Khánh trong README.
2. Thử ví dụ hai kết quả, chọn từng địa điểm, mở thẻ lý do; kiểm tra ảnh/mô tả/số luật thay đổi tương ứng.
3. Bấm Xóa; thử chưa chọn đủ; thử bộ mã không có kết quả và kiểm tra vùng kết quả không còn nội dung cũ.
4. Thu nhỏ/phóng to; cuộn tiêu chí khi cần và kéo vạch chia. Xem tooltip để đọc hết nhãn dài.
5. Quay lại sảnh rồi vào tư vấn; mở Hướng dẫn; thử nút Thoát.
6. Mở ui/main.ui trong Qt Designer, Preview, sửa một nhãn, lưu rồi chạy lại; giữ nguyên objectName.

Đã giải nén bản đóng gói vào thư mục tạm độc lập và chạy lại: 27/27 kiểm thử đạt; kiểm tra dữ liệu 0 lỗi, 35 cảnh báo, 435 luật qua kiểm tra. Bản ZIP không phụ thuộc thư mục upload hay môi trường cũ.
