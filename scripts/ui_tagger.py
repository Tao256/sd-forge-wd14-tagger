import os
import json
from pathlib import Path
import gradio as gr
from modules import script_callbacks, shared
from scripts.wd14_tagger import WD14Tagger

def sync_value(value):
    """同步所有标签页的选择器值"""
    return [value, value]

# send to txt2img or img2img
def get_send_js_code(target_tab_type):
    """使用指定的 ID: txt2img 或 img2img"""
    return f"""
        async function() {{
            function getTagText() {{
            let tagsBox = gradioApp().getElementById("wd14_tags_output_single");
            if (!tagsBox) return "";
            let ta = tagsBox.querySelector("textarea, input");
            if (ta && ta.value) return ta.value;
            return tagsBox.textContent.trim();
        }}

        // 图片 as base64
        async function getImageBase64FromImg(src) {{
            return new Promise((resolve) => {{
                let img = new window.Image();
                img.crossOrigin = "Anonymous";
                img.onload = function() {{
                    try {{
                        let canvas = document.createElement('canvas');
                        canvas.width = img.width;
                        canvas.height = img.height;
                        let ctx = canvas.getContext('2d');
                        ctx.drawImage(img, 0, 0);
                        let b64 = canvas.toDataURL('image/png').split(',')[1];
                        resolve(b64);
                    }} catch(e) {{
                        resolve("");
                    }}
                }};
                img.onerror = function() {{ resolve(""); }};
                img.src = src;
            }});
        }}
        // 调用
        let tags = getTagText();
        let image_b64 = "";
        let parent = gradioApp().getElementById("wd14_single_input");
        if (parent) {{
            let img = parent.querySelector("img");
            if (img && img.src) {{
                image_b64 = await getImageBase64FromImg(img.src);
            }}
        }}

        data = {{ tags, image_b64 }};
        console.log(data);

        var targetTabContentId = 'tab_{target_tab_type}'; // 使用您指定的 ID: tab_txt2img 或 tab_img2img
        var tabContent = gradioApp().getElementById(targetTabContentId);
        if (!tabContent) {{
            console.error("WD14 Tagger: 找不到目標分頁 ID: " + targetTabContentId);
            return [];
        }}
        // 尋找該 ID 區塊內的第一個 textarea
        var prompt_textarea = tabContent.querySelector('textarea');
        if (prompt_textarea) {{
            prompt_textarea.value = data.tags;
            prompt_textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
            prompt_textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }} else {{
            console.error("WD14 Tagger: 在 " + targetTabContentId + " 中找不到 textarea");
        }}
        // 跳转页面
        var tabsContainer = gradioApp().getElementById('tabs');
        if (!tabsContainer) tabsContainer = gradioApp().querySelector('.tabs');
        if (tabsContainer) {{
            var allTabDivs = Array.from(tabsContainer.children).filter(
                node => node.tagName === 'DIV' && node.classList.contains('tabitem')
            );
            // 找出目標 ID 在這些分頁中的索引 (Index)
            var targetIndex = -1;
            for (var i = 0; i < allTabDivs.length; i++) {{
                if (allTabDivs[i].id === targetTabContentId) {{
                    targetIndex = i;
                    break;
                }}
            }}
            if (targetIndex !== -1) {{
                var nav = tabsContainer.querySelector('.tab-nav');
                if (nav) {{
                    var buttons = nav.querySelectorAll('button');
                    if (buttons && buttons[targetIndex]) {{
                        buttons[targetIndex].click();
                    }} else {{
                        console.error("WD14 Tagger: 找不到對應索引的按鈕");
                    }}
                }} else {{
                    console.error("WD14 Tagger: 找不到 .tab-nav");
                }}
            }} else {{
                console.error("WD14 Tagger: 無法計算分頁索引，找不到 ID " + targetTabContentId + " 在 tabs 中的位置");
            }}
        }}
        return [];
    }}
    """

def save_tags_to_txt(tags_dict):
    """將标签保存到 TXT 文件"""
    tags_dict = eval(tags_dict)
    if not tags_dict:
        return
    for name, tags in tags_dict.items():
        filename = WD14_DIR / f"{name}.txt"
        with open(filename, "w") as f:
            f.write(tags)
    gr.Info("The label has been successfully saved")


def on_ui_tabs():
    def sync_opts_to_components():
        return [
            gr.update(value=shared.opts.wd14_model),
            gr.update(value=shared.opts.wd14_model),
            gr.update(value=shared.opts.wd14_model),
            gr.update(value=shared.opts.wd14_threshold),
            gr.update(value=shared.opts.wd14_threshold),
            gr.update(value=shared.opts.wd14_threshold),
        ]

    with gr.Blocks(analytics_enabled=False) as tagger_interface:
        with gr.Tabs(elem_id="tabs"):
            # WD14 Tagger
            with gr.Tab(label=I18N["Single Image"][default_lang], id="wd14_single_tab"):  # 单张图片
                with gr.Row():
                    with gr.Column(variant="panel"):
                        input_image_wd14 = gr.Image(
                            label=I18N["Input Image"][default_lang],
                            type="pil",
                            sources=["upload", "webcam"],
                            height=520,
                            object_fit="contain",
                            elem_id="wd14_single_input",
                        )
                        model_selector1 = gr.Dropdown(
                            label=I18N["Select Tagger Model"][default_lang],
                            choices=tagger_backend.model_configs_list,
                            value=shared.opts.wd14_model,
                            elem_id="wd14_model_selector1",
                        )
                        threshold_slider1 = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=shared.opts.wd14_threshold,
                            step=0.05,
                            label=I18N["Threshold"][default_lang],
                            elem_id="wd14_threshold_slider1",
                        )
                        with gr.Row():
                            interrogate_btn1 = gr.Button(
                                I18N["Interrogate"][default_lang],
                                variant="primary",
                                elem_id="wd14_run_btn1",
                            )
                            unload_btn1 = gr.Button(
                                I18N["Unload Model"][default_lang],
                                variant="secondary",
                                elem_id="wd14_unload_btn1",
                            )
                    with gr.Column(variant="panel"):
                        tags_output1 = gr.Textbox(
                            label=I18N["Output Tags"][default_lang],
                            lines=10,
                            show_copy_button=True,
                            interactive=False,
                            elem_id="wd14_tags_output_single",
                        )
                        rating_output = gr.Label(
                            label=I18N["Rating"][default_lang],
                            elem_id="wd14_rating_output",
                        )
                        with gr.Row():
                            send_to_txt2img_wd14_1 = gr.Button(
                                I18N["Send to Txt2Img"][default_lang],
                                elem_id="wd14_send_txt2img_btn",
                            )
                            send_to_img2img_wd14_1 = gr.Button(
                                I18N["Send to Img2Img"][default_lang],
                                elem_id="wd14_send_img2img_btn",
                            )
            with gr.Tab(label=I18N["Batch Process"][default_lang], id="wd14_batch_tab"):  # 批量图片
                with gr.Row():
                    with gr.Column(variant="panel"):
                        batch_input_wd14 = gr.File(
                            label=I18N["Input Batch Images"][default_lang],
                            file_types=[".jpg", ".jpeg", ".png", ".bmp", ".gif"],
                            file_count="multiple",
                            elem_id="wd14_batch_input",
                        )
                        model_selector2 = gr.Dropdown(
                            label=I18N["Select Tagger Model"][default_lang],
                            choices=tagger_backend.model_configs_list,
                            value=shared.opts.wd14_model,
                            elem_id="wd14_model_selector2",
                        )
                        threshold_slider2 = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=shared.opts.wd14_threshold,
                            step=0.05,
                            label=I18N["Threshold"][default_lang],
                            elem_id="wd14_threshold_slider2",
                        )
                        with gr.Row():
                            interrogate_btn2 = gr.Button(
                                I18N["Interrogate"][default_lang],
                                variant="primary",
                                elem_id="wd14_run_btn2",
                            )
                            unload_btn2 = gr.Button(
                                I18N["Unload Model"][default_lang],
                                variant="secondary",
                                elem_id="wd14_unload_btn2",
                            )
                    with gr.Column(variant="panel"):
                        tags_output2 = gr.Textbox(
                            label=I18N["Output Tags"][default_lang],
                            lines=10,
                            show_copy_button=True,
                            interactive=False,
                            elem_id="wd14_tags_output_batch",
                        )
                        with gr.Row():
                            save_txt_btn_wd14_2 = gr.Button(
                                I18N["Save Tags to Txt"][default_lang],
                                variant="secondary",
                                elem_id="wd14_save_txt_btn2",
                            )
            with gr.Tab(label=I18N["Batch from Folder"][default_lang], id="wd14_folder_tab"):  # 文件夹图片
                with gr.Row():
                    with gr.Column(variant="panel"):
                        folder_input_wd14 = gr.Textbox(
                            label=I18N["Input Folder"][default_lang],
                            placeholder="Enter the path of the folder containing images",
                            elem_id="wd14_folder_input",
                        )
                        model_selector3 = gr.Dropdown(
                            label=I18N["Select Tagger Model"][default_lang],
                            choices=tagger_backend.model_configs_list,
                            value=shared.opts.wd14_model,
                            elem_id="wd14_model_selector3",
                        )
                        threshold_slider3 = gr.Slider(
                            minimum=0.0,
                            maximum=1.0,
                            value=shared.opts.wd14_threshold,
                            step=0.05,
                            label=I18N["Threshold"][default_lang],
                            elem_id="wd14_threshold_slider3",
                        )
                        with gr.Row():
                            interrogate_btn3 = gr.Button(
                                I18N["Interrogate"][default_lang],
                                variant="primary",
                                elem_id="wd14_run_btn3",
                            )
                            unload_btn3 = gr.Button(
                                I18N["Unload Model"][default_lang],
                                variant="secondary",
                                elem_id="wd14_unload_btn3",
                            )
                    with gr.Column(variant="panel"):
                        tags_output3 = gr.Textbox(
                            label=I18N["Output Tags"][default_lang],
                            lines=10,
                            show_copy_button=True,
                            interactive=False,
                            elem_id="wd14_tags_output_folder",
                        )
                        with gr.Row():
                            save_txt_btn_wd14_3 = gr.Button(
                                I18N["Save Tags to Txt"][default_lang],
                                variant="secondary",
                                elem_id="wd14_save_txt_btn3",
                            )
            
            

            # --- 事件綁定 ---
            tagger_interface.load(
                fn=sync_opts_to_components,
                inputs=[],
                outputs=[model_selector1,model_selector2,model_selector3,
                         threshold_slider1,threshold_slider2,threshold_slider3],
                show_progress="hidden"
            )

            model_selector1.change(
            fn=sync_value,
            inputs=[model_selector1],
            outputs=[model_selector2, model_selector3],
            )
            model_selector2.change(
                fn=sync_value,
                inputs=[model_selector2],
                outputs=[model_selector1, model_selector3],
            )
            model_selector3.change(
                fn=sync_value,
                inputs=[model_selector3],
                outputs=[model_selector1, model_selector2],
            )
            threshold_slider1.change(
                fn=sync_value,
                inputs=[threshold_slider1],
                outputs=[threshold_slider2, threshold_slider3],
            )
            threshold_slider2.change(
                fn=sync_value,
                inputs=[threshold_slider2],
                outputs=[threshold_slider1, threshold_slider3],
            )
            threshold_slider3.change(
                fn=sync_value,
                inputs=[threshold_slider3],
                outputs=[threshold_slider1, threshold_slider2],
            )
            interrogate_btn1.click(
                fn=tagger_backend.predict,
                inputs=[input_image_wd14, model_selector1, threshold_slider1],
                outputs=[tags_output1, rating_output],
            )
            interrogate_btn2.click(
                fn=tagger_backend.multi_predict,
                inputs=[batch_input_wd14, model_selector2, threshold_slider2],
                outputs=[tags_output2],
            )
            interrogate_btn3.click(
                fn=tagger_backend.folder_predict,
                inputs=[folder_input_wd14, model_selector3, threshold_slider3],
                outputs=[tags_output3],
            )
            unload_btn1.click(fn=tagger_backend.unload_model, inputs=[], outputs=[tags_output1])
            unload_btn2.click(fn=tagger_backend.unload_model, inputs=[], outputs=[tags_output2])
            unload_btn3.click(fn=tagger_backend.unload_model, inputs=[], outputs=[tags_output3])
            send_to_txt2img_wd14_1.click(fn=None, inputs=[], outputs=[], _js=get_send_js_code("txt2img"))
            send_to_img2img_wd14_1.click(fn=None, inputs=[], outputs=[], _js=get_send_js_code("img2img"))
            save_txt_btn_wd14_2.click(fn=save_tags_to_txt, inputs=[tags_output2], outputs=[])
            save_txt_btn_wd14_3.click(fn=save_tags_to_txt, inputs=[tags_output3], outputs=[])

    return [(tagger_interface, "Tagger", "tagger_tab")]

def on_ui_settings():
    # 插件专属分类：(唯一标识, 显示名称)
    section = ("wd14_setting", "WD14")
    #语言
    shared.opts.add_option(
        "wd14_language",
        shared.OptionInfo(
            "English",
            I18N["Language"][default_lang],
            gr.Dropdown,
            {"choices": ["English", "简体中文", "繁體中文"]},
            section=section
        )
    )
    #wd14模型
    shared.opts.add_option(
        "wd14_model",
        shared.OptionInfo(
            "wd-vit-tagger-v3",
            I18N["Select Tagger Model"][default_lang],
            gr.Dropdown,
            {"choices": tagger_backend.model_configs_list},
            section=section
        )
    )
    #threshold
    shared.opts.add_option(
        "wd14_threshold",
        shared.OptionInfo(
            0.35,
            I18N["Threshold"][default_lang],
            gr.Slider,
            {"minimum": 0.0, "maximum": 1.0, "step": 0.05},
            section=section
        )
    )

#----------------------------------------------------------------
# 路徑設定
current_file_path = Path(os.path.abspath(__file__))
EXTENSION_DIR = current_file_path.parent.parent
SYS_DIR = EXTENSION_DIR.parent.parent
OUTPUT_DIR = SYS_DIR / "output" / "tagger_output"
print(f"[Tagger-all] OUTPUT_DIR: {OUTPUT_DIR}")
CSV_DIR = EXTENSION_DIR / "csv"
MODELS_DIR = SYS_DIR / "models" / "tagger_models"
print(f"[Tagger-all] model_dirs: {MODELS_DIR}")
WD14_DIR = OUTPUT_DIR / "wd14_output"

if not os.path.exists(MODELS_DIR):
    os.mkdir(MODELS_DIR)
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)
if not os.path.exists(WD14_DIR):
    os.mkdir(WD14_DIR)

with open(EXTENSION_DIR / "language.json", "r", encoding="utf-8") as f1:
    I18N = json.load(f1)  # 语言

try:
    default_lang = shared.opts.wd14_language
except:
    default_lang="English"

# --main--
tagger_backend = WD14Tagger(MODELS_DIR, CSV_DIR)

script_callbacks.on_ui_tabs(on_ui_tabs)    
script_callbacks.on_ui_settings(on_ui_settings)
