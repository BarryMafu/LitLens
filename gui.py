import gradio as gr
import pandas as pd
from main import get_recommendations  # 假设你的推荐逻辑在main.py中
import os
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"

# 自定义CSS实现淡蓝色主题
css = """
:root {
    --left-bg: #98cbf8;    /* 左侧深蓝 */
    --right-bg: #ffffff;   /* 右侧纯白 */
    --global-bg: #e3f2fd;  /* 全局淡蓝背景 */
}

body {
    background: var(--global-bg) !important;
    min-height: 100vh;
}

#component-0 {
    max-width: 1200px !important;
    border-radius: 12px !important;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    background: var(--global-bg)
}

#component-1 { /* 左侧栏 */
    background: var(--global-bg) !important;
    padding: 30px !important;
    color: white !important;
}

#component-2 { /* 右侧栏 */
    background: var(--global-bg) !important;
    padding: 30px !important;
}

/* 输入框样式 */
input[type="text"], .slider-container {
    background: rgba(255,255,255,0.9) !important;
    border-radius: 8px !important;
    padding: 12px !important;
}

/* 按钮样式 */
button {
    background: var(--left-bg) !important;  /* 橙色按钮 */
    color: white !important;
    border: none !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    margin-top: 20px !important;
}

/* 标题样式 */
h2 {
    color: inherit !important;
    margin-bottom: 20px !important;
}
"""

def recommend_papers(paper_name, top_n):
    # 调用你的主逻辑函数（示例）
    recommendations = get_recommendations(paper_name)
    
    # 格式化输出为美观的HTML
    output_html = "<div style='font-family: Arial, sans-serif'>"
    for i, (paper, reason) in enumerate(recommendations.items(), 1):
        output_html += f"""
        <div style='margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;'>
            <h3 style='color: #1e88e5'>推荐论文 #{i}</h3>
            <p><strong>论文ID:</strong> {paper}</p>
            <p><strong>推荐理由:</strong> {reason}</p>
        </div>
        """
    output_html += "</div>"
    return output_html

with gr.Blocks(css=css, analytics_enabled=False) as demo:
    gr.Markdown("# 学术论文推荐系统", elem_classes="header")
    
    with gr.Row():
         # 左侧深蓝参数区
        with gr.Column(elem_id="left-col"):
            gr.Markdown("## 参数设置", elem_classes="white-text")
            paper_name = gr.Textbox(label="论文标题", placeholder="请输入目标论文标题")
            top_n = gr.Slider(1, 20, value=5, label="推荐数量", step=1)
            submit_btn = gr.Button("开始推荐", variant="primary")
        
        # 右侧白色结果区
        with gr.Column(elem_id="right-col"):
            gr.Markdown("## 推荐结果")
            output_html = gr.HTML()
    
    submit_btn.click(
        fn=recommend_papers,
        inputs=[paper_name, top_n],
        outputs=output_html
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", 
                server_port=7861, 
                favicon_path=None,  # 禁用图标请求
                # enable_queue=True,
                ssl_verify=False,
                _frontend=False     # 关键参数：禁用前端PWA特性
    )