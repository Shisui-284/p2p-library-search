# 🌐 P2P Library Search: Distributed Inverted Index

> **Đồ án môn học: Cơ sở dữ liệu phân tán**
> **Đề tài #64 (Category 7):** Quản lý Dữ liệu Ngang hàng (P2P Data Management)

---

##  1. Giới thiệu dự án (Introduction)
Dự án này xây dựng một hệ thống tìm kiếm tài liệu ngang hàng (Peer-to-Peer - P2P) hoàn toàn phi tập trung, loại bỏ sự phụ thuộc vào máy chủ trung tâm (Single Point of Failure). Hệ thống sử dụng thuật toán **Bảng băm phân tán (DHT - Distributed Hash Table)** để phân mảnh và quản lý bộ chỉ mục đảo ngược (Inverted Index) của 100 tài liệu văn bản (Short Stories).

###  Các tính năng nổi bật:
* ** Truy vấn đa từ khóa (Boolean AND):** Cho phép tìm kiếm các tài liệu chứa đồng thời nhiều từ khóa cùng lúc thông qua phép toán giao tập hợp (Intersection).
* ** Định tuyến thông minh:** Hệ thống tự động băm từ khóa và định tuyến (Forward) request đến đúng máy trạm (Peer) đang quản lý dữ liệu thông qua REST API.
* ** Khả năng chịu lỗi (Fault Tolerance):** Mạng lưới không sụp đổ khi một hoặc nhiều máy trạm bị tắt đột ngột. Hệ thống sẽ báo lỗi an toàn và tiếp tục phục vụ dữ liệu từ các máy trạm còn sống.
* ** Phân tích hiệu năng (Analytical Metrics):** Tích hợp công cụ đo lường độ trễ (Latency) của mỗi truy vấn tính bằng mili-giây (ms).

---

##  2. Kiến trúc hệ thống (Architecture)
Hệ thống được thiết kế với 3 Node độc lập, giao tiếp qua HTTP Protocol:
* **Node 0 (Port 5000):** Peer quản lý dữ liệu nhóm 0.
* **Node 1 (Port 5001):** Peer quản lý dữ liệu nhóm 1.
* **Node 2 (Port 5002):** Peer quản lý dữ liệu nhóm 2.
* **Client:** Giao diện người dùng độc lập để gửi truy vấn vào mạng P2P.

Dữ liệu cục bộ của mỗi Node được lưu trữ dưới định dạng JSON siêu nhẹ trong thư mục `peer_data/`.

---

##  3. Cấu trúc thư mục (Folder Structure)
```text
Du_an_P2P/
├── dataset/               # Chứa 100 file văn bản (.txt) giả lập tài liệu
├── peer_data/             # Chứa 3 file JSON lưu trữ phân mảnh của 3 Node
├── generate_data.py       # Module: Sinh tự động 100 file văn bản mẫu
├── node.py                # Module: Trích xuất chỉ mục đảo ngược (Inverted Index)
├── distribute_data.py     # Module: Thuật toán Hash DHT và phân tán dữ liệu
├── server.py              # Web Server (Flask) chạy dịch vụ cho mỗi Node P2P
└── client.py              # Ứng dụng Client gửi truy vấn & log hệ thống