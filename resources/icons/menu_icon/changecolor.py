import os
import re

# 获取当前脚本（changecolor.py）所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
icon_dir = os.path.join(current_dir)  # 当前文件夹就是 menu_icon
# 如果 SVG 其实在上一级，可以改为 os.path.join(current_dir, 'menu_icon')

for fname in os.listdir(icon_dir):
    if fname.endswith('.svg'):
        path = os.path.join(icon_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            svg = f.read()
        svg = re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="currentColor"', svg)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
print("批量替换完成！")
