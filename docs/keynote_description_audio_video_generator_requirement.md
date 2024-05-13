### Requirement Definition Document (RDD) cho "Video Thuyết Minh từ Key Note"

#### Mục Đích
Phát triển một hệ thống tự động hóa để chuyển đổi các tệp trình bày như PowerPoint (PPTX) và PDF thành video thuyết minh, sử dụng các mô hình AI để tạo ra văn bản thuyết minh và âm thanh tương ứng.

#### Các Module Chính và Chức Năng

1. **Image Conversion Module**
   - **Mục đích:** Chuyển đổi file trình bày thành các hình ảnh.
   - **Chức năng:**
     - Nhận input là file PPTX hoặc PDF.
     - Chuyển đổi mỗi slide trình bày thành ảnh độc lập.
   - **Công nghệ sử dụng:** Python, `pdf2image`, `python-pptx`.

2. **Text Generation Module**
   - **Mục đích:** Sinh ra văn bản thuyết minh từ ảnh slide.
   - **Chức năng:**
     - Gửi ảnh cho mô hình AI (GPT model) để sinh ra văn bản thuyết minh.
     - Sử dụng prompts để định hình cấu trúc và phong cách của văn bản.
   - **Công nghệ sử dụng:** OpenAI API, Python.

3. **Audio Generation Module**
   - **Mục đích:** Chuyển văn bản thuyết minh thành audio.
   - **Chức năng:**
     - Gửi văn bản thuyết minh cho mô hình AI (text-to-speech) để tạo file âm thanh.
   - **Công nghệ sử dụng:** OpenAI Text-to-Speech API, Python.

4. **Video Creation Module**
   - **Mục đích:** Tạo video từ các ảnh và file âm thanh tương ứng.
   - **Chức năng:**
     - Kết hợp ảnh và âm thanh để tạo thành video.
     - Xuất video định dạng phù hợp (ví dụ: MP4).
   - **Công nghệ sử dụng:** Python, `moviepy`.

#### Yêu Cầu Không Kỹ Thuật
- **Khả năng tương thích:** Hệ thống phải hỗ trợ các định dạng file phổ biến như PPTX và PDF.
- **Tính dễ sử dụng:** Giao diện người dùng đơn giản cho phép người dùng dễ dàng tải lên và xử lý các file.
- **Hiệu suất:** Hệ thống phải xử lý các tác vụ nhanh chóng, đặc biệt là chuyển đổi file và sinh âm thanh.
- **Chất lượng đầu ra:** Video cuối cùng phải có chất lượng hình ảnh và âm thanh tốt, đồng bộ hình ảnh và âm thanh phải chính xác.

#### Milestones và Lộ trình
- **Nghiên cứu và chọn lựa công nghệ:** ??
- **Phát triển và tích hợp các module:** ??
- **Kiểm thử và tối ưu hóa:** ??
- **Triển khai và đào tạo người dùng:** ??

### Sequence Diagram
![image](https://github.com/tech-learners-ai/nphuc_openai_api_study/assets/17255682/9f0ed53c-f0f0-464d-8386-c81fa16ae757)
