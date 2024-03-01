import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Đọc dữ liệu và trích xuất embeddings
df = pd.read_csv('data/fine_food_reviews_with_embeddings.csv')
# Chuyển đổi sang mảng Numpy
matrix = np.array(df.embedding.apply(eval).tolist())

# Tạo mô hình t-SNE và biến đổi dữ liệu
tsne = TSNE(n_components=2, perplexity=15, random_state=42, init='random', learning_rate=200)
vis_dims = tsne.fit_transform(matrix)

# Màu sắc cho mỗi đánh giá sao
colors = ["red", "darkorange", "gold", "turquoise", "darkgreen"]
x = [x for x, y in vis_dims]
y = [y for x, y in vis_dims]
color_indices = df.Score.values - 1  # Chỉ số màu dựa trên đánh giá sao

# Tạo biểu đồ
colormap = matplotlib.colors.ListedColormap(colors)
plt.scatter(x, y, c=color_indices, cmap=colormap, alpha=0.3)

# Bổ sung xử lý tính trung bình vị trí cho mỗi loại đánh giá sao và vẽ chúng lên biểu đồ
for score in [0, 1, 2, 3, 4]:
    avg_x = np.array(x)[df.Score - 1 == score].mean()
    avg_y = np.array(y)[df.Score - 1 == score].mean()
    std_x = np.array(x)[df.Score - 1 == score].std()
    std_y = np.array(y)[df.Score - 1 == score].std()
    color = colors[score]
    plt.scatter(avg_x, avg_y, marker='x', color=color, s=100)  # Đánh dấu trung bình của mỗi loại đánh giá
    # In thông số
    print(f"Score {score+1}: Mean (x, y) = ({avg_x:.2f}, {avg_y:.2f}), Std (x, y) = ({std_x:.2f}, {std_y:.2f})")

plt.title("Amazon ratings visualized in language using t-SNE")
plt.show()
