# sd-forge-wd14-tagger
|  | |
| :--- | :--- |
| English | [README.md](README.md) |
| **简体中文** | [README_Zh-CN.md](README_Zh-CN.md) |
| 繁體中文 | [README_Zh-TW.md](README_Zh-TW.md) |

---

## 📷 用户页面

<div align="center">
  <img src="example/single image.jpg" alt="single image">
  <p><em>单张图片</em></p>
</div>
<div align="center">
  <img src="example/Batch Process.jpg" alt="Batch Process">
  <p><em>批量处理</em></p>
</div>
<div align="center">
  <img src="example/Batch from Folder.jpg" alt="Batch from Folder">
  <p><em>文件夹批量处理</em></p>
</div>

## ✨ 特点

   支持SD-WebUI-forge和Neo分支

   模型暂不支持自动下载，请自行手动下载模型文件并放到对应的模型目录。
   
   模型文件放置`SD-WebUI-Forge/model/tagger_models`,模型必须是以`.onnx`为文件后缀的模型文件！

   模型文件夹需运行插件自动生成。

   

## 📥 下载

### 方法一：通过 WebUI 内置插件安装器 (推荐)
1. 打开 WebUI，进入 `Extensions` -> `Install from URL`。
2. URL 填入：`https://github.com/Tao256/sd-forge-wd14-tagger.git`。
3. 点击 `Install`，安装完成后重启 WebUI。

### 方法二：手动下载
1. 前往 [Releases](https://github.com/Tao256/sd-forge-wd14-tagger/releases/tag/sd-webui-WD14) 页面下载最新版本的压缩包。
2. 将解压后的文件夹放入 `SD-WebUI-Forge/extensions/` 目录下。
3. 重启 WebUI，插件将自动加载。

## 🧠 模型

| 模型  | 置信度阈值 | 模型下载 | 说明  |
| :--- | :--- | :--- | :--- |
| wd-convnext-tagger-v3 | 0.3–0.5 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-eva02-large-tagger-v3) <br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-convnext-tagger-v3) | 纯卷积架构推理快，显存占用适中，适合批量处理 |
| wd-eva02-large-tagger-v3 | 0.4–0.6 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-eva02-large-tagger-v3)<br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-eva02-large-tagger-v3) | 能更好地捕捉图像整体氛围与风格，标签关联性强 | 
| wd-swinv2-tagger-v3 | 0.35–0.55 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-swinv2-tagger-v3)<br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-swinv2-tagger-v3) | 对发色、眼色、服装风格等典型动漫特征识别准确率高 | 
| wd-vit-tagger-v3 | 0.3–0.45 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-vit-tagger-v3)<br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-vit-tagger-v3) | 生成的标签之间语义关联性强，适合提示词直接使用 | 
| wd-vit-large-tagger-v3 | 0.35–0.5 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-vit-large-tagger-v3)<br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-vit-large-tagger-v3) | ViT-Large 参数量更大，对复杂构图、细节特征的识别能力更强 | 

## 🔗 参考链接

1. **项目主页**: [https://github.com/Tao256/sd-forge-wd14-tagger](https://github.com/Tao256/sd-forge-wd14-tagger)
2. **Stable Diffusion WebUI Neo**: [https://github.com/lllyasviel/stable-diffusion-webui-forge](https://github.com/lllyasviel/stable-diffusion-webui-forge)
3. **WD14 Tagger**:[https://github.com/picobyte/stable-diffusion-webui-wd14-tagger](https://github.com/picobyte/stable-diffusion-webui-wd14-tagger)

