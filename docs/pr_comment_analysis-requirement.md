### Requirement Definition cho Ứng Dụng Tự Động Hóa Quản Lý Comment trên GitHub PR

#### Tổng quan
Ứng dụng này nhằm mục đích tự động hóa quá trình thu thập, phân loại, thống kê và phân tích các bình luận từ các Pull Request (PR) trên GitHub, và đưa ra các đề xuất hành động dựa trên phân tích đó.

#### Các Module Chính và Chức Năng

1. **PR Collect Module**
   - **Mục đích:** Thu thập các bình luận từ PR trên GitHub.
   - **Chức năng:**
     - Kết nối với GitHub API để truy xuất bình luận.
     - Lưu trữ bình luận vào CSV.
   - **Công nghệ:** Python, GitHub API, pandas.

2. **Classify Module**
   - **Mục đích:** Phân loại các bình luận dựa trên nội dung.
   - **Chức năng:**
     - Đọc bình luận từ CSV.
     - Gửi bình luận đến OpenAI API để phân loại.
     - Nhận kết quả phân loại và cập nhật vào CSV.
   - **Công nghệ:** Python, OpenAI API, pandas.

3. **Plotting Module**
   - **Mục đích:** Tạo biểu đồ thống kê từ dữ liệu bình luận đã phân loại.
   - **Chức năng:**
     - Đọc dữ liệu từ CSV.
     - Vẽ biểu đồ và lưu vào file.
   - **Công nghệ:** Python, matplotlib, pandas.

4. **Analysis Module**
   - **Mục đích:** Phân tích các biểu đồ và dữ liệu thống kê để đưa ra các đề xuất hành động.
   - **Chức năng:**
     - Đọc biểu đồ và dữ liệu từ file.
     - Gửi dữ liệu đến OpenAI API để yêu cầu phân tích.
     - Nhận phân tích và đề xuất hành động từ OpenAI.
     - Lưu kết quả phân tích vào file.
   - **Công nghệ:** Python, OpenAI API.

#### Yêu Cầu Không Kỹ Thuật
- **Bảo mật:** Quản lý an toàn các khóa API và thông tin nhạy cảm.
- **Hiệu suất:** Đảm bảo hệ thống xử lý và phản hồi nhanh chóng, kể cả khi số lượng bình luận lớn.
- **Khả năng mở rộng:** Có thể mở rộng để xử lý nhiều repository và tăng khối lượng dữ liệu mà không làm giảm hiệu suất.

### Sequence Diagram
![alt text](image.png)

Dưới đây là checklist ngắn gọn để bạn theo dõi tiến độ của dự án tự động hóa việc quản lý comment trên GitHub PR, dựa trên các chức năng chính đã nêu trong Requirement Definition Document (RDD) mới:

### Checklist Theo Dõi Tiến Độ Dự Án

#### 1. PR Collect Module
- [ ] Đã thiết lập và cấu hình xác thực GitHub API.
- [ ] Hoàn thành script thu thập bình luận từ PR.
- [ ] Đã kiểm tra và xác nhận việc lưu trữ bình luận vào CSV.
- [ ] Đã thực hiện kiểm thử tích hợp với GitHub API.

#### 2. Classify Module
- [ ] Đã hoàn thành script đọc bình luận từ CSV.
- [ ] Đã tích hợp OpenAI API để phân loại bình luận.
- [ ] Kiểm thử phân loại bình luận và cập nhật vào CSV.
- [ ] Đã kiểm tra độ chính xác của kết quả phân loại.

#### 3. Plotting Module
- [ ] Hoàn thành script đọc dữ liệu từ CSV.
- [ ] Phát triển chức năng vẽ biểu đồ từ dữ liệu phân loại.
- [ ] Kiểm thử việc lưu biểu đồ vào file.
- [ ] Đảm bảo biểu đồ thể hiện đúng thông tin dữ liệu.

#### 4. Analysis Module
- [ ] Hoàn thành script đọc biểu đồ và dữ liệu từ file.
- [ ] Tích hợp OpenAI API để yêu cầu phân tích và đề xuất.
- [ ] Kiểm thử việc nhận và xử lý phân tích từ OpenAI.
- [ ] Lưu trữ kết quả phân tích vào file và kiểm tra tính chính xác.

#### Chức Năng Tổng Hợp và Kiểm Thử
- [ ] Kiểm thử tổng thể toàn bộ dòng chảy dữ liệu và chức năng.
- [ ] Đánh giá và khắc phục lỗi trên toàn hệ thống.
- [ ] Chuẩn bị tài liệu hướng dẫn sử dụng và bảo trì hệ thống.
- [ ] Tổ chức phiên đào tạo sử dụng hệ thống cho người dùng cuối (nếu cần).