from PIL import Image

# Đường dẫn đến hình ảnh WebP nguồn
input_webp = 'image/image_edit_original.webp'

# Đường dẫn đến hình ảnh PNG đích
output_png = 'image/image_edit_original.png'

# Mở hình ảnh WebP
image = Image.open(input_webp)

# Chuyển đổi hình ảnh sang định dạng RGBA nếu nó không phải là RGBA
if image.mode != 'RGBA':
    image = image.convert('RGBA')

# Lưu hình ảnh dưới dạng PNG
image.save(output_png, 'PNG')
