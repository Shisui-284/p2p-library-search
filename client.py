import requests
import time

# Chọn Node 0 làm cổng giao tiếp mặc định cho người dùng
ENTRY_NODE_URL = "http://127.0.0.1:5000/search"

def search_single_keyword(keyword):
    print(f"[*] Đang tra cứu từ khóa: '{keyword}'...")
    try:
        # Gửi API đến mạng P2P
        response = requests.get(f"{ENTRY_NODE_URL}?keyword={keyword}")
        data = response.json()
        
        if data.get('status') == 'success':
            docs = data.get('docs', [])
            print(f"  -> Thành công! Dữ liệu được xử lý bởi: {data.get('handled_by')}")
            print(f"  -> Danh sách tài liệu: {docs}\n")
            return set(docs) # Dùng set (tập hợp) để dễ tính phần giao (AND)
        else:
            print(f"  -> [LỖI TỪ MẠNG]: {data.get('error')}\n")
            return set()
    except Exception as e:
        print(f"Lỗi kết nối đến mạng P2P: {e}\n")
        return set()

def search_boolean_and(keyword1, keyword2):
    print(f"=== BẮT ĐẦU TRUY VẤN: '{keyword1}' AND '{keyword2}' ===\n")
    
    start_time = time.time() # BẮT ĐẦU BẤM GIỜ
    
    # 1. Tra cứu tập tài liệu của từ khóa 1
    docs_1 = search_single_keyword(keyword1)
    
    # 2. Tra cứu tập tài liệu của từ khóa 2
    docs_2 = search_single_keyword(keyword2)
    
    # 3. Phép tính logic AND
    result = docs_1.intersection(docs_2)
    
    end_time = time.time() # KẾT THÚC BẤM GIỜ
    latency = (end_time - start_time) * 1000 # Đổi ra mili-giây (ms)
    
    print("=== KẾT QUẢ CUỐI CÙNG ===")
    if result:
        print(f"Các tài liệu chứa CẢ HAI từ khóa là: {list(result)}")
    else:
        print("Không có tài liệu nào chứa đồng thời cả hai từ khóa này.")
        
    # IN RA CHỈ SỐ PHÂN TÍCH (ANALYTICAL METRICS)
    print(f"\n[Analytical Metrics] Độ trễ truy vấn (Latency): {latency:.2f} ms")

if __name__ == '__main__':
    # Đổi từ khóa để ép hệ thống gọi vào Node 1
    search_boolean_and("network", "database")