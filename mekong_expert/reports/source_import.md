# Báo cáo nhập nguồn

Nguồn giữ nguyên; chỉ chuyển đổi sang JSON. Chỉ số đoạn DOCX bắt đầu từ 0.

- tap luat-sk 30 dia diem(1).docx: SHA-256 `92889c8350c45b0604e07b82a4d6ab44791c4ecccd01d21ec79de59cc7b58b71`
- minh hoa 30 dia diem(2).docx: SHA-256 `5c48bc74cd4efe8b488480dda6aaffa6acce97c1bb9f3cd8dadd48a5cb1fac3f`

Đã nhập 81 sự kiện (gồm T1–T30), 30 địa điểm, 435 luật.
Không nhập địa chỉ cụ thể vì tài liệu không có trường địa chỉ cụ thể.

## Quan hệ ảnh trong DOCX

| Mã | Đoạn tiêu đề | Đoạn ảnh | Quan hệ | Tệp nhúng | Chú thích |
| --- | --- | --- | --- | --- | --- |
| T1 | 0 | 3 | rId8 | /word/media/image1.jpeg | Hình 1. Làng du lịch Mỹ Khánh |
| T2 | 6 | 7 | rId9 | /word/media/image2.jpg | Hình 2. Chợ nổi Cái Răng |
| T3 | 10 | 11 | rId10 | /word/media/image3.jpeg | Hình 3. Khu du lịch Cồn Phụng |
| T4 | 14 | 15 | rId11 | /word/media/image4.jpeg | Hình 4. Cù lao Thới Sơn |
| T5 | 19 | 20 | rId12 | /word/media/image5.jpg | Hình 5. Trải nghiệm tại vườn xoài ở Làng du lịch Mỹ Xương |
| T6 | 23 | 24 | rId13 | /word/media/image6.jpeg | Hình 6. Làng hoa Sa Đéc |
| T7 | 28 | 29 | rId14 | /word/media/image7.jpeg | Hình 7. Khu di tích Xẻo Quýt |
| T8 | 32 | 33 | rId15 | /word/media/image8.jpeg | Hình 8. Khu du lịch sinh thái Gáo Giồng |
| T9 | 37 | 38 | rId16 | /word/media/image9.jpeg | Hình 9. Vườn quốc gia Tràm Chim |
| T10 | 41 | 42 | rId17 | /word/media/image10.jpeg | Hình 10. Rừng tràm Trà Sư |
| T11 | 46 | 47 | rId18 | /word/media/image11.jpg | Hình 11. Miếu Bà Chúa Xứ Núi Sam |
| T12 | 50 | 51 | rId19 | /word/media/image12.jpeg | Hình 12. Khu bảo tồn thiên nhiên Lung Ngọc Hoàng |
| T13 | 55 | 56 | rId20 | /word/media/image13.jpeg | Hình 13. Vườn quốc gia U Minh Thượng |
| T14 | 59 | 60 | rId21 | /word/media/image14.jpg | Hình 14. Chùa Dơi |
| T15 | 63 | 64 | rId22 | /word/media/image15.jpg | Hình 15. Chùa Xiêm Cán |
| T16 | 67 | 68 | rId23 | /word/media/image16.jpg | Hình 16. Nhà Công tử Bạc Liêu |
| T17 | 72 | 73 | rId24 | /word/media/image17.jpg | Hình 17. VinWonders Phú Quốc |
| T18 | 76 | 77 | rId25 | /word/media/image18.jpeg | Hình 18. Sun World Hòn Thơm |
| T19 | 81 | 82 | rId26 | /word/media/image19.jpeg | Hình 19. Khu du lịch Suối Tranh |
| T20 | 85 | 86 | rId27 | /word/media/image20.png | Hình 20. Bãi Cây Mến – đảo Nam Du |
| T21 | 90 | 91 | rId28 | /word/media/image21.jpg | Hình 21. Điểm du lịch cộng đồng Cồn Sơn |
| T22 | 94 | 95 | rId29 | /word/media/image22.jpg | Hình 22. Nhà cổ Bình Thủy |
| T23 | 99 | 100 | rId30 | /word/media/image23.jpg | Hình 23. Nhà cổ Huỳnh Thủy Lê |
| T24 | 103 | 104 | rId31 | /word/media/image24.jpg | Hình 24. Phơi bánh tráng tại làng nghề Thuận Hưng |
| T25 | 108 | 109 | rId32 | /word/media/image25.jpg | Hình 25. Chùa Âng |
| T26 | 112 | 113 | rId33 | /word/media/image26.jpg | Hình 26. Di tích Gò Cây Thị B thuộc Khu di tích khảo cổ Óc Eo – Ba Thê |
| T27 | 117 | 118 | rId34 | /word/media/image27.jpg | Hình 27. Khu du lịch Làng nổi Tân Lập |
| T28 | 121 | 122 | rId35 | /word/media/image28.jpg | Hình 28. Khu bảo tồn đất ngập nước Láng Sen |
| T29 | 126 | 127 | rId36 | /word/media/image29.jpg | Hình 29. Khu du lịch Mũi Cà Mau |
| T30 | 130 | 131 | rId37 | /word/media/image30.jpg | Hình 30. Đảo Hòn Sơn |

Mỗi khối có đúng một ảnh và một chú thích cùng số T; ghép theo quan hệ DOCX, không theo tên imageN.
Chưa xác minh ảnh/chú thích và dữ liệu du lịch với nguồn thực địa.

## Cảnh báo lúc nhập

- Nguồn không khớp khoảng cách: luật 380: lời văn K1, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 382: lời văn K1, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 384: lời văn K3, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 386: lời văn K1, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 387: lời văn K3, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 388: lời văn K4, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 390: lời văn K1, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 391: lời văn K3, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 393: lời văn K4, biểu thức K2.
- Nguồn không khớp khoảng cách: luật 394: lời văn K1, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 395: lời văn K2, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 397: lời văn K2, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 398: lời văn K1, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 400: lời văn K4, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 401: lời văn K2, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 402: lời văn K1, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 404: lời văn K2, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 405: lời văn K4, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 406: lời văn K1, biểu thức K3.
- Nguồn không khớp khoảng cách: luật 407: lời văn K2, biểu thức K3.
- Luật trùng hoàn toàn: [37, 40] → T3.
- Luật trùng hoàn toàn: [85, 89] → T6.
- Luật trùng hoàn toàn: [91, 94] → T6.
- Luật trùng hoàn toàn: [122, 126] → T8.
- Luật trùng hoàn toàn: [146, 153] → T10.
- Luật trùng hoàn toàn: [316, 319] → T22.
- Luật trùng hoàn toàn: [323, 326] → T22.
- Luật trùng hoàn toàn: [332, 335] → T23.
- Luật trùng hoàn toàn: [336, 339] → T23.
- Luật trùng hoàn toàn: [344, 350] → T24.
- Luật trùng hoàn toàn: [360, 363] → T25.
- Luật trùng hoàn toàn: [410, 413] → T29.
- Luật trùng hoàn toàn: [424, 435] → T30.
- Cùng điều kiện, nhiều kết luận (hợp lệ): [(75, 'T5'), (87, 'T6')].
- Cùng điều kiện, nhiều kết luận (hợp lệ): [(114, 'T8'), (136, 'T9')].
