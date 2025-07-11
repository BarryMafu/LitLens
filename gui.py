import gradio as gr
import pandas as pd
from main import LitLens, LitLensConfig  # 假设你的推荐逻辑在main.py中
from utils import get_basic_info, get_arxiv_id_by_title
import os
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

# 自定义CSS实现淡蓝色主题
CSS_STYLE = """
:root {
    --light-purple: #d9c4f5;    /* 浅紫色 */
    --light-blue: #c4e3f5;      /* 浅蓝色 */
    --gradient-blue-purple: linear-gradient(135deg, #5c6bc0 0%, #7e57c2 100%); /* 按钮渐变 */
    --global-bg: linear-gradient(145deg, #f0e6ff 0%, #e6f2ff 100%); /* 全局渐变背景 */
}

body {
    background: var(--global-bg) !important;
    min-height: 100vh;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

#component-0 {
    max-width: 1200px !important;
    border-radius: 20px !important;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(103, 58, 183, 0.15);
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}

#component-1 {
    background: rgba(255, 255, 255, 0.7) !important;
    padding: 30px !important;
    border-radius: 15px;
    margin: 10px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

#component-2 {
    overflow-y: auto !important;
    max-height: 70vh !important;
    padding-right: 15px !important;
}

#component-2::-webkit-scrollbar {
    width: 8px;
}

#component-2::-webkit-scrollbar-track {
    background: rgba(126, 87, 194, 0.1);
    border-radius: 10px;
}

#component-2::-webkit-scrollbar-thumb {
    background: linear-gradient(#7e57c2, #5c6bc0);
    border-radius: 10px;
}

/* 父容器控制间距（更紧凑版） */
.gr-markdown:has(.header) {
    display: flex;
    flex-direction: column;
    gap: 0.1em !important;  /* 比之前更小的间距值 */
    margin-bottom: 0.8em !important;
}

.gr-markdown h1.header,
.gr-markdown h1.header > span {
    color: white !important;
    -webkit-text-fill-color: white !important;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3) !important;
    background: linear-gradient(135deg, #3f51b5 0%, #9c27b0 100%) !important;
    font-size: 3em !important;
    padding: 0.5em 0 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 15px rgba(63, 81, 181, 0.3) !important;
    display: block !important;
    width: 100% !important;
}

/* 副标题（更紧凑对齐） */
.sub-header {
    text-align: center;
    color: #7e57c2 !important;
    font-size: 1.3em !important;  /* 从1.2em略微增大 */
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;
    font-weight: 500 !important;
}

/* 输入框样式 */
input[type="text"], .slider-container {
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 12px !important;
    padding: 14px !important;
    border: 1px solid rgba(126, 87, 194, 0.3) !important;
    box-shadow: 0 2px 8px rgba(126, 87, 194, 0.1) !important;
    transition: all 0.3s ease;
}

input[type="text"]:focus {
    border-color: #7e57c2 !important;
    box-shadow: 0 2px 12px rgba(126, 87, 194, 0.2) !important;
}

/* 按钮样式 */
button {
    background: var(--gradient-blue-purple) !important;
    color: white !important;
    border: none !important;
    padding: 14px 28px !important;
    border-radius: 12px !important;
    margin-top: 20px !important;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    box-shadow: 0 4px 15px rgba(92, 107, 192, 0.3);
    transition: all 0.3s ease;
    background-size: 200% auto;
}

button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(92, 107, 192, 0.4);
    background-position: right center;
}

/* 标题样式 */
h2 {
    color: #5e35b1 !important;
    margin-bottom: 20px !important;
    font-weight: 600;
    border-bottom: 2px solid rgba(126, 87, 194, 0.2);
    padding-bottom: 10px;
}

/* 结果区域样式 */
.output_html {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.current_paper_html {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    border-left: 4px solid #7e57c2;
}

/* 滑块样式 */
.gr-slider .gr-slider-container {
    background: rgba(126, 87, 194, 0.1) !important;
}

.gr-slider .gr-slider-container .gr-slider-handle {
    background: var(--gradient-blue-purple) !important;
    border: 3px solid white !important;
}

/* 响应式调整 */
@media (max-width: 768px) {
    #component-0 {
        border-radius: 0 !important;
    }
    
    #component-1, #component-2 {
        margin: 5px !important;
        padding: 20px !important;
    }
}

/* Paper Information卡片样式 */
.paper-info-card {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
    border-left: 4px solid #7e57c2 !important;
}

/* 推荐结果卡片样式 */
.recommendation-card {
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
    border-left: 4px solid #1e88e5 !important;
}

/* 标题统一使用Markdown样式 */
.paper-info-title {
    color: #5e35b1 !important;
    margin-bottom: 15px !important;
}

.recommendation-title {
    color: #1e88e5 !important;
    margin-bottom: 10px !important;
}
"""

def recommend_papers(arxiv_id, first_n, second_n, progress=gr.Progress()):
    # 调用你的主逻辑函数（示例）
    config = LitLensConfig(
        limit_reference=-1,
        limit_cited=-1,
        limit_search=10,
        count_first_round=first_n,
        count_second_round=second_n,
        count_third_round=20,
        verbose=True
    )

    litlens = LitLens(config=config)
    recommendations = litlens.get_recommendations(arxiv_id, progress)
    
    # 格式化输出为美观的HTML
    output_md = ""
    for i, title in enumerate(recommendations):
        arxiv_id = get_arxiv_id_by_title(title)
        output_md += f"""
### Recommendation #{i + 1}
<div class="recommendation-card">
<strong>Title</strong> {title}

**ArXiv ID** [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})
</div>
""" if arxiv_id else f"""
### Recommendation #{i + 1}
<div class="recommendation-card">
<strong>Title</strong> {title}

**ArXiv ID** Not found
</div>
"""
    # output_html += "</div>"
    return output_md

def show_info(arxiv_id):
    info = get_basic_info(arxiv_id)
    if info:
        return f"""
## Paper Information
<div class="paper-info-card">
<strong>Title</strong>  {info['title']}

**ArXiv ID** [{info['arxiv_id']}]({info['link']})

**Published on** {info['publish_time']}
</div>
"""

if __name__ == "__main__":
    with gr.Blocks(css=CSS_STYLE, analytics_enabled=False, theme=gr.themes.Soft()) as demo:
        gr.Markdown("# LitLens", elem_classes="header")
        gr.Markdown("## An arXiv paper recommendation system based on Large Language Models", elem_classes="sub-header")
        
        with gr.Row():
            with gr.Column():
                current_paper_html = gr.Markdown(
                    label="Current Paper",
                    value="*No paper selected yet.*"
                )

        with gr.Row():
            # 左侧深蓝参数区
            with gr.Column(elem_id="left-col"):
                gr.Markdown("## Setting", elem_classes="white-text")
                arxiv_id = gr.Textbox(label="ArXiv号", placeholder="Please input the arXiv id. eg: 2301.00001", lines=1)
                first_round_limit = gr.Slider(5, 50, value=30, label="First Round Limit", step=1)
                second_round_limit = gr.Slider(3, 20, value=10, label="Final Recommendation Number", step=1)
                submit_btn = gr.Button("Recommend", variant="primary")
            
            # 右侧白色结果区
            with gr.Column(elem_id="right-col"):
                gr.Markdown("## Result")
                output_html = gr.Markdown()
        
        submit_btn.click(
            fn=show_info,
            inputs=arxiv_id,
            outputs=current_paper_html
        ).then(
            fn=recommend_papers,
            inputs=[arxiv_id, first_round_limit, second_round_limit],
            outputs=output_html
        )


    demo.launch(server_name="0.0.0.0", 
                server_port=7861, 
                favicon_path=None,  # 禁用图标请求
                # enable_queue=True,
                ssl_verify=False,
                _frontend=False     # 关键参数：禁用前端PWA特性
    )