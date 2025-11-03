from PIL import Image, ImageOps
from fpdf import FPDF
import os
import pandas as pd

# 设置文件夹路径
root_folder = "/Users/tangerine/Desktop/test_ebird"

# 读取 ebird_taxa.xlsx
xls_path = "/Users/tangerine/Documents/ebird_taxa.xlsx"
df = pd.read_excel(xls_path)

# 提取物种名称列和分布情况列
common_names = df['common_name'].tolist()
#location_columns = df.columns[4:8]
#locations = df[location_columns]

# 初始化PDF，横向模式
pdf = FPDF(orientation='L', unit='mm', format='A4')  # 横向排版
pdf.set_auto_page_break(auto=True, margin=1)  # 减小页面边距

# 设置字体
pdf.set_font("helvetica", size=12)

# 遍历每个子文件夹
for common_name in common_names:
    folder_path = os.path.join(root_folder, common_name)
    if os.path.isdir(folder_path):  # 确保是子文件夹
        pdf.add_page()

        # 添加鸟类 common name
        species_row = df[df['common_name'] == common_name]
        #distributed_locations = ',   '.join(species_row.iloc[0, 3:8].dropna().index)
        title_height = 5  # 标题高度
        pdf.cell(0, title_height, text=f"{common_name}", ln=True, align='C')  # 输出 common_name

        # 图片排版参数
        page_width, page_height = 297, 210  # A4横向大小（mm）
        margin = 1  # 页面边距
        img_width = (page_width - margin * 3) / 2  # 每行两张图片，计算图片宽度
        img_height = (page_height - title_height - margin * 3) / 2  # 每列两张图片，计算图片高度
        x, y = margin, title_height + 10  # 图片起始位置，标题下方约5mm

        # 遍历子文件夹中的图片
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))][:4]  # 每页最多4张图片
        temp_files = []  # 用于存储临时文件路径
        for img_file in image_files:
            img_path = os.path.join(folder_path, img_file)
            try:
                img = Image.open(img_path)

                # 如果是RGBA模式（含透明度），转换为RGB模式
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                # 创建一个适配图片区域的背景
                bg = Image.new("RGB", (int(img_width * 3.78), int(img_height * 3.78)), (255, 255, 255))

                # 根据比例调整图片大小
                img.thumbnail((bg.width, bg.height), Image.Resampling.LANCZOS)

                # 将调整后的图片粘贴到背景中央
                paste_x = (bg.width - img.width) // 2
                paste_y = (bg.height - img.height) // 2
                bg.paste(img, (paste_x, paste_y))

                # 保存为临时文件
                temp_img_path = os.path.join(folder_path, f"temp_{img_file}")
                bg.save(temp_img_path, quality=95, subsampling=0)
                temp_files.append(temp_img_path)  # 将临时文件路径保存

                # 添加图片到PDF
                pdf.image(temp_img_path, x=x, y=y, w=img_width, h=img_height)

                # 更新下一个图片的位置
                x += img_width + margin
                if x + img_width > page_width:  # 如果到页面宽度，换行
                    x = margin
                    margin.as_integer_ratio()
                    y += img_height + margin / 2  # 减少行之间的间距

            except Exception as e:
                print(f"Error processing {img_path}: {e}")

        # 删除临时文件
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)

# 保存PDF
output_pdf = "/Users/tangerine/Desktop/Birds_Collection_High_Quality.pdf"
pdf.output(output_pdf)
print(f"PDF saved as {output_pdf}")