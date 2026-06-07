import os
import random

DATASET_DIR = 'dataset'

# Các từ khóa chuyên ngành buộc phải có để hệ thống P2P có dữ liệu hoạt động
core_keywords = ['distributed', 'database', 'network', 'system', 'peer', 'node', 'architecture', 'p2p', 'index', 'hash']

# Các đoạn văn mẫu mang phong cách "Truyện ngắn" (Short Stories)
story_templates = [
    "The old clock ticked loudly in the empty room. Alice looked out the window, watching the heavy rain fall.",
    "It was a dark and stormy night. The wind howled through the tall trees, making a sound like a dying beast.",
    "Captain Ray checked the monitors of his spaceship. Everything was green, but a strange feeling lingered in his gut.",
    "In a small village hidden in the mountains, there lived a wise baker who knew the secret of true happiness.",
    "The detective lit a cigarette and stared at the evidence board. The pieces didn't fit. Someone was lying.",
    "She found the ancient map hidden inside a dusty book in the library. It promised treasures beyond imagination.",
    "He woke up with no memory of who he was or how he got there. Only a small silver key was in his pocket.",
    "The festival was in full swing. Lights danced in the sky, and the sound of music filled the warm summer air."
]

def generate_mock_documents(num_docs=100):
    # Tạo thư mục nếu chưa có
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)

    print(f"[*] Đang tiến hành tạo {num_docs} file truyện ngắn...")

    for i in range(1, num_docs + 1):
        # Format tên file: doc_001.txt, doc_002.txt...
        filename = f"doc_{i:03d}.txt"
        filepath = os.path.join(DATASET_DIR, filename)

        # 1. Chọn ngẫu nhiên 2-4 câu chuyện nhỏ để ghép lại thành một truyện ngắn
        selected_paragraphs = random.sample(story_templates, random.randint(2, 4))
        story_text = " ".join(selected_paragraphs)
        
        # 2. Chuyển thành danh sách các từ để chuẩn bị chèn từ khóa
        words = story_text.split()
        
        # 3. Chọn ngẫu nhiên 3-5 từ khóa chuyên ngành cho mỗi file
        keywords_to_inject = random.sample(core_keywords, random.randint(3, 5))
        
        # 4. Chèn từ khóa vào các vị trí ngẫu nhiên trong truyện ngắn
        for kw in keywords_to_inject:
            insert_pos = random.randint(0, len(words))
            words.insert(insert_pos, kw)
            
        # Nối lại thành đoạn văn bản hoàn chỉnh
        final_content = " ".join(words)

        # Ghi vào file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(final_content)

    print("[+] Hoàn tất! 100 file truyện ngắn đã được tạo mới hoàn toàn trong thư mục 'dataset'.")

if __name__ == '__main__':
    generate_mock_documents()