import os
import re

# Tên thư mục chứa dữ liệu
DATASET_DIR = 'dataset'

def build_local_inverted_index():
    """
    Hàm đọc các file .txt trong thư mục dataset, 
    tách từ khóa và tạo Chỉ mục đảo ngược (Inverted Index).
    """
    inverted_index = {}

    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.exists(DATASET_DIR):
        print(f"Lỗi: Không tìm thấy thư mục '{DATASET_DIR}'")
        return {}

    # Lấy danh sách tất cả các file có đuôi .txt
    files = [f for f in os.listdir(DATASET_DIR) if f.endswith(".txt")]
    
    if not files:
        print("Cảnh báo: Không có file .txt nào trong thư mục dataset!")
        return {}

    print(f"Đang xử lý {len(files)} tài liệu...")

    # Duyệt qua từng file
    for filename in files:
        # Lấy DocID từ tên file (ví dụ: doc_01.txt -> doc_01)
        doc_id = filename.replace('.txt', '')
        filepath = os.path.join(DATASET_DIR, filename)

        try:
            # Mở và đọc nội dung file
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()

            # Tiền xử lý văn bản: 
            # 1. Chuyển tất cả thành chữ thường
            text = text.lower()
            # 2. Dùng Regex để tách từ (chỉ lấy các cụm chữ cái/số, bỏ qua dấu câu)
            words = re.findall(r'\b\w+\b', text)

            # Đưa từ khóa vào Inverted Index
            for word in words:
                # Nếu từ này chưa từng xuất hiện, tạo một tập hợp (set) mới cho nó
                if word not in inverted_index:
                    inverted_index[word] = set() # Dùng set() để tránh việc 1 file bị ghi tên 2 lần
                
                # Thêm DocID vào danh sách của từ khóa này
                inverted_index[word].add(doc_id)

        except Exception as e:
            print(f"Lỗi khi đọc file {filename}: {e}")

    # Chuyển kiểu dữ liệu 'set' về dạng 'list' (danh sách) 
    # để sau này dễ dàng chuyển thành file JSON khi chia sẻ qua mạng
    for word in inverted_index:
        inverted_index[word] = list(inverted_index[word])

    return inverted_index

# --- PHẦN CHẠY THỬ NGHIỆM ---
if __name__ == '__main__':
    # Chạy hàm tạo chỉ mục
    index = build_local_inverted_index()
    
    if index:
        print(f"\nHoàn thành! Đã tách được {len(index)} từ khóa duy nhất.")
        print("Mẫu 5 từ khóa đầu tiên trong hệ thống:")
        
        # In thử 5 kết quả đầu tiên để xem cấu trúc
        count = 0
        for word, docs in index.items():
            print(f"- Từ khóa '{word}' xuất hiện tại: {docs}")
            count += 1
            if count >= 5:
                break