import sys
import json
import requests
from flask import Flask, request, jsonify
from distribute_data import get_node_id

app = Flask(__name__)

# Cấu hình mạng: Phân chia Port (cổng) cho từng Node để chạy trên cùng 1 máy tính
NODE_PORTS = {
    0: 5000,
    1: 5001,
    2: 5002
}

# Biến lưu trữ dữ liệu của Node này
local_data = {}
my_node_id = None

def load_data():
    """Hàm tải file JSON cục bộ lên bộ nhớ RAM khi Node khởi động"""
    global local_data
    try:
        with open(f'peer_data/node_{my_node_id}.json', 'r', encoding='utf-8') as f:
            local_data = json.load(f)
        print(f"--> [Node {my_node_id}] Đã tải thành công file dữ liệu cục bộ.")
    except FileNotFoundError:
        print(f"--> [Node {my_node_id}] Lỗi: Không tìm thấy file dữ liệu.")

@app.route('/search', methods=['GET'])
def search():
    """API Tìm kiếm cốt lõi của mạng P2P"""
    keyword = request.args.get('keyword', '').lower()
    if not keyword:
        return jsonify({"error": "Vui lòng nhập từ khóa (keyword)"}), 400

    # 1. Thuật toán DHT: Băm từ khóa để biết ai đang giữ nó
    target_node = get_node_id(keyword)
    print(f"\n[Trace] Tìm '{keyword}' -> Băm DHT chỉ định Node đích là: {target_node}")

    # 2. Xử lý cục bộ: Nếu từ khóa thuộc về CHÍNH MÁY NÀY
    if target_node == my_node_id:
        print(f"[Trace] Node {my_node_id} tự xử lý yêu cầu.")
        docs = local_data.get(keyword, [])
        return jsonify({
            "keyword": keyword,
            "docs": docs,
            "handled_by": f"Node {my_node_id}",
            "status": "success"
        })
    
    # 3. Định tuyến (Routing): Nếu từ khóa thuộc về MÁY KHÁC
    else:
        target_port = NODE_PORTS[target_node]
        # Tạo đường dẫn API gọi sang máy bạn
        target_url = f"http://127.0.0.1:{target_port}/search?keyword={keyword}"
        print(f"[Trace] Chuyển tiếp (Forward) yêu cầu sang Node {target_node} (Cổng {target_port})")
        
        try:
            # Gửi tín hiệu mạng sang Node đích
            response = requests.get(target_url, timeout=5)
            return jsonify(response.json())
        except requests.exceptions.RequestException:
            # Xử lý kịch bản lỗi (The Failure Scenario)
            error_msg = f"Node {target_node} đang bị tắt (Offline) hoặc mất kết nối."
            print(f"[LỖI] {error_msg}")
            return jsonify({
                "keyword": keyword,
                "error": error_msg,
                "status": "failed"
            }), 503

if __name__ == '__main__':
    # Đọc tham số từ dòng lệnh để biết đang khởi động Node số mấy
    if len(sys.argv) < 2:
        print("Cách chạy: py server.py <node_id> (Ví dụ: py server.py 0)")
        sys.exit(1)
        
    my_node_id = int(sys.argv[1])
    if my_node_id not in NODE_PORTS:
        print("Lỗi: ID của máy chỉ được là 0, 1 hoặc 2")
        sys.exit(1)

    # Tải dữ liệu và bật server
    load_data()
    port = NODE_PORTS[my_node_id]
    print(f"=== HỆ THỐNG SẴN SÀNG: NODE {my_node_id} ĐANG CHẠY TRÊN CỔNG {port} ===")
    
    # Tắt thông báo rác của Flask để màn hình log (Trace) sạch sẽ dễ nhìn hơn
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(host='127.0.0.1', port=port)