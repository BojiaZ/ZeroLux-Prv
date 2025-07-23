import os
import shutil
import re

DIR = "resources/icons/menu_icon"
TARGET_COLOR = "#009CA6"

print("当前目录文件列表：")
print(os.listdir(DIR))
print("-" * 50)

for fname in os.listdir(DIR):
    try:
        print(f"检测: {fname}")
        if fname.lower().endswith(".svg") and not fname.endswith("_gray.svg") and not fname.endswith("_blue.svg"):
            print(f" 处理：{fname}")
            basename, ext = os.path.splitext(fname)
            gray_name = f"{basename}_gray{ext}"
            blue_name = f"{basename}_blue{ext}"
            # 原文件重命名为 _gray
            os.rename(os.path.join(DIR, fname), os.path.join(DIR, gray_name))
            print(f"  重命名: {fname} -> {gray_name}")
            # 复制一份做 _blue
            shutil.copy(os.path.join(DIR, gray_name), os.path.join(DIR, blue_name))
            print(f"  复制一份: {gray_name} -> {blue_name}")
            # 替换颜色
            with open(os.path.join(DIR, blue_name), "r", encoding="utf-8") as f:
                svg_text = f.read()
            svg_text = re.sub(r'stroke="#?[A-Fa-f0-9]{3,6}"', f'stroke="{TARGET_COLOR}"', svg_text)
            svg_text = re.sub(r'stroke=\'#?[A-Fa-f0-9]{3,6}\'', f'stroke="{TARGET_COLOR}"', svg_text)
            svg_text = re.sub(r'fill="#?[A-Fa-f0-9]{3,6}"', f'fill="{TARGET_COLOR}"', svg_text)
            svg_text = re.sub(r'fill=\'#?[A-Fa-f0-9]{3,6}\'', f'fill="{TARGET_COLOR}"', svg_text)
            svg_text = re.sub(r'stroke="currentColor"', f'stroke="{TARGET_COLOR}"', svg_text)
            svg_text = re.sub(r'fill="currentColor"', f'fill="{TARGET_COLOR}"', svg_text)
            with open(os.path.join(DIR, blue_name), "w", encoding="utf-8") as f:
                f.write(svg_text)
            print(f"  {fname} → {gray_name} & {blue_name}（换色完成）")
        else:
            print(f" 跳过：{fname}")
    except Exception as e:
        print(f"处理 {fname} 时发生错误: {e}")

print("全部svg重命名和蓝色文件生成完毕！")
