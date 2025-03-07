import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io


def generate_image(text):
    """生成白字黑底图片"""
    image_size = (1600, 1600)
    # 提高图片分辨率以提升字体清晰度
    high_res_size = (image_size[0] * 2, image_size[1] * 2)
    # 根据字符数量确定字体大小
    char_count = len(text)
    if char_count == 1:
        font_size = 900
    elif char_count == 2:
        font_size = 700
    elif char_count == 3:
        font_size = 500
    elif char_count == 4:
        font_size = 400
    elif char_count == 5:
        font_size = 320
    elif char_count == 6:
        font_size = 280
    elif char_count == 7:
        font_size = 240
    elif char_count == 8:
        font_size = 200
    else:
        return None
    high_res_font_size = font_size * 2
    img = Image.new('RGB', high_res_size, color='black')
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default(size=high_res_font_size)
    # 计算文字位置（兼容 Pillow 10.0+）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[0]
    x = (high_res_size[0] - text_width) // 2
    # 微调垂直位置
    y = (high_res_size[1] - text_height) // 2 - high_res_font_size // 10
    # 模拟字体加粗，多次绘制文字并进行微小偏移
    offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
    for offset_x, offset_y in offsets:
        draw.text((x + offset_x, y + offset_y), text, fill='white', font=font)
    # 将高分辨率图片缩放到所需尺寸
    img = img.resize(image_size, Image.LANCZOS)
    return img


# 网页界面
st.title(f"📷 {st.secrets["name"]} 头像生成器")
st.markdown("输入文字 → 自动生成居中图片 → 支持下载")
# 主界面
user_input = st.text_input("输入要生成图片的文字（最多 8 个字符）：", "8")
if len(user_input) > 8:
    st.error("输入的字符数量不能超过 8 个，请重新输入。")
else:
    if user_input:
        try:
            # 生成图片
            img = generate_image(user_input)
            if img:
                # 显示预览
                st.image(img, caption="预览效果", use_container_width=True)
                # 下载功能
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                st.download_button(
                    label="⬇️ 下载图片",
                    data=img_bytes.getvalue(),
                    file_name='custom_image.png',
                    mime='image/png'
                )
            else:
                st.error("输入的字符数量不符合要求，请重新输入。")
        except Exception as e:
            st.error(f"生成图片时出错: {str(e)}")
# 使用提示
st.markdown("""
### 使用说明：
1. 在输入框输入你的编号
2. 点击下载按钮保存图片
3. 更换至 Lark 头像
""")
