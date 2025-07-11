import gradio as gr
from typing import List, Dict
import time
import random
from PIL import Image, ImageDraw, ImageFont
import io
import os
import numpy as np

# 定义论文类
class Paper:
    def __init__(self, arxiv_id: str, title: str, label: str):
        self.arxiv_id = arxiv_id
        self.title = title
        self.label = label  # OR, R2, R1, R0
        
    def to_dict(self) -> Dict:
        return {
            "arxiv_id": self.arxiv_id,
            "title": self.title,
            "label": self.label
        }
    
    def to_html(self) -> str:
        # 为不同标签设置不同颜色
        label_colors = {
            "OR": "#FF5733",  # 橙色
            "R2": "#33FF57",  # 绿色
            "R1": "#3357FF",  # 蓝色
            "R0": "#F033FF"   # 紫色
        }
        color = label_colors.get(self.label, "#CCCCCC")
        
        return f"""
        <div style="
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            background-color: #f9f9f9;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            ">
                <span style="
                    background-color: {color};
                    color: white;
                    padding: 3px 10px;
                    border-radius: 15px;
                    font-size: 0.9em;
                ">{self.label}</span>
                <span style="
                    font-family: monospace;
                    color: #666;
                ">{self.arxiv_id}</span>
            </div>
            <h3 style="margin: 0; color: #333;">{self.title}</h3>
        </div>
        """

# 创建示例背景图片的函数
def create_background_image():
    # 创建一个简单的渐变背景
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # 添加渐变效果
    for i in range(height):
        r = int(200 + 55 * i / height)
        g = int(230 + 25 * i / height)
        b = int(255 - 55 * i / height)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # 添加LitLens文字
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    
    draw.text((width//2 - 100, height//2 - 30), "LitLens", fill=(0, 0, 0), font=font)
    
    # 将PIL Image转换为numpy数组
    return np.array(img)

# 模拟后端处理函数
def process_papers():
    # 这里模拟后端处理过程，实际应用中替换为你的实际处理逻辑
    papers = []
    labels = ["OR", "R2", "R1", "R0"]
    
    # 生成一些示例论文
    for i in range(1, 11):
        arxiv_id = f"arXiv:210{i}.1234{i}"
        title = f"Example Paper Title {i} on Machine Learning and Natural Language Processing"
        label = random.choice(labels)
        papers.append(Paper(arxiv_id, title, label).to_dict())
    
    # 模拟处理延迟
    time.sleep(2)
    
    return papers

# 主处理函数，与Gradio交互
def start_processing(progress=gr.Progress()):
    progress(0, desc="Starting LitLens recommendation engine...")
    time.sleep(1)
    
    # 模拟处理步骤
    steps = [
        "Loading user preferences...",
        "Analyzing research interests...",
        "Querying literature database...",
        "Processing recent publications...",
        "Applying recommendation algorithms...",
        "Generating final recommendations..."
    ]
    
    papers = []
    for i, step in enumerate(steps):
        progress(i / len(steps), desc=step)
        time.sleep(1.5)
        
        # 模拟在处理过程中逐步获取论文
        if i > 2:
            new_paper = process_papers()[0]  # 每次获取一篇新论文
            papers.append(new_paper)
    
    progress(1.0, desc="Recommendations complete!")
    return papers

# 自定义CSS样式
custom_css = """
#title {
    text-align: center;
    font-size: 2.5em;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 20px;
}
#paper-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
#start-btn {
    background: linear-gradient(to right, #3498db, #2ecc71);
    color: white;
    border: none;
    padding: 12px 24px;
    font-size: 1.1em;
    border-radius: 25px;
    cursor: pointer;
    transition: all 0.3s ease;
}
#start-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}
"""

# 创建Gradio界面
with gr.Blocks(css=custom_css, title="LitLens - Literature Recommendation System") as demo:
    # 创建背景图片
    bg_image = create_background_image()
    
    # 标题部分
    gr.Markdown("<div id='title'>LitLens Literature Recommendation</div>")
    
    # 背景图片 - 现在使用numpy数组
    gr.Image(value=bg_image, show_label=False, interactive=False, height=200)
    
    # 主内容区域
    with gr.Row():
        with gr.Column(scale=8):
            # 论文显示容器
            paper_output = gr.HTML(label="Recommended Papers", elem_id="paper-container")
        with gr.Column(scale=2):
            # 开始按钮
            start_btn = gr.Button("Start Recommendation", elem_id="start-btn")
    
    # 按钮点击事件
    start_btn.click(
        fn=start_processing,
        outputs=paper_output,
        # show_progress="full"
    )

# 启动应用
if __name__ == "__main__":
    demo.launch()