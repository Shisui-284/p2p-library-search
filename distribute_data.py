import os
import json
# Import hàm tạo chỉ mục từ file node.py của bạn
from node import build_local_inverted_index

PEER_DATA_DIR = 'peer_data'
NUM_NODES = 3

def get_node_id(keyword):
    """
    Hàm băm (Hash function) cốt lõi của DHT.
    Nhiệm vụ: Chuyển một chữ cái/từ khóa thành một con số từ 0 đến 2.
    """
    # Tính tổng mã ASCII của các ký tự trong từ khóa
    # Ví dụ: chữ 'a' = 97, 'b' = 98...
    ascii_sum = sum(ord(char) for char in keyword)
    
    # Chia lấy dư cho số lượng Node (3) để quyết định từ khóa thuộc về máy nào
    return ascii_sum % NUM_NODES

def distribute_index():
    print("1. Đang đọc dữ liệu và tạo Inverted Index tổng...")
    global_index = build_local_inverted_index()

    if not global_index:
        print("Lỗi: Không có dữ liệu để phân phối.")
        return

    # Tạo 3 "kho chứa" cục bộ (tương đương 3 ổ cứng của 3 máy trạm)
    node_data = {
        0: {},
        1: {},
        2: {}
    }

    print("2. Đang tiến hành băm (Hash) và phân mảnh dữ liệu (Fragmentation)...")
    # Duyệt qua từng từ khóa để "chia bài"
    for word, doc_list in global_index.items():
        target_node = get_node_id(word)
        node_data[target_node][word] = doc_list

    # Kiểm tra và tạo thư mục peer_data nếu chưa có
    if not os.path.exists(PEER_DATA_DIR):
        os.makedirs(PEER_DATA_DIR)

    print("3. Đang xuất dữ liệu ra các Node...")
    # Lưu dữ liệu phân mảnh ra 3 file JSON riêng biệt
    for node_id, data in node_data.items():
        filepath = os.path.join(PEER_DATA_DIR, f'node_{node_id}.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            # indent=4 giúp file JSON được format đẹp, dễ đọc bằng mắt thường
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"  -> Đã lưu {len(data)} từ khóa vào Node {node_id} (File: {filepath})")

    print("\nHoàn tất Bước 3! Dữ liệu đã được phân tán thành công.")

if __name__ == '__main__':
    distribute_index()