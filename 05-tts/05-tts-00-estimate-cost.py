def estimate_tts_cost(file_path, model="TTS"):
    # Đơn giá cho mỗi mô hình
    price_per_million_chars = {
        "TTS": 15.00,  # $15.00 / 1M characters for standard TTS
        "TTS HD": 30.00  # $30.00 / 1M characters for HD TTS
    }

    try:
        # Đọc file và tính số ký tự
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            num_chars = len(content)
            
            # Ước lượng chi phí
            cost_per_char = price_per_million_chars[model] / 1_000_000
            estimated_cost = cost_per_char * num_chars
            
            print(f"Estimated cost for {model} with {num_chars} characters: ${estimated_cost:.2f}")
            
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except KeyError:
        print(f"Model not recognized. Please choose between 'TTS' or 'TTS HD'.")

# Sử dụng hàm này để ước lượng chi phí
file_path = "book/hoang-tu-be-bui-giang-full.txt"  # Thay thế đường dẫn tới file văn bản của bạn
estimate_tts_cost(file_path, "TTS")
estimate_tts_cost(file_path, "TTS HD")
