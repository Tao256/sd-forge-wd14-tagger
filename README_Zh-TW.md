# sd-forge-wd14-tagger
|  | |
| :--- | :--- |
| English | [README.md](README.md) |
| 簡體中文 | [README_Zh-CN.md](README_Zh-CN.md) |
| **繁體中文** | [README_Zh-TW.md](README_Zh-TW.md) |

---

## 📷 使用者頁面

<div align="center">
  <img src="example/single image.jpg" alt="single image">
  <p><em>單張圖片</em></p>
</div>
<div align="center">
  <img src="example/Batch Process.jpg" alt="Batch Process">
  <p><em>批次處理</em></p>
</div>
<div align="center">
  <img src="example/Batch from Folder.jpg" alt="Batch from Folder">
  <p><em>資料夾批次處理</em></p>
</div>

## ✨ 特色

   支援SD-WebUI-forge和Neo分支

   模型暫不支援自動下載，請自行手動下載模型檔案並放到對應的模型目錄。
   
   模型檔案放置於`SD-WebUI-Forge/model/tagger_models`，模型必須是以`.onnx`為檔案後綴的模型檔案！

   模型資料夾需執行外掛程式自動生成。

## 📥 下載

### 方法一：透過 WebUI 內建外掛安裝器 (推薦)
1. 開啟 WebUI，進入 `Extensions` -> `Install from URL`。
2. URL 填入：`https://github.com/Tao256/sd-forge-wd14-tagger.git`。
3. 點擊 `Install`，安裝完成後重新啟動 WebUI。

### 方法二：手動下載
1. 前往 [Releases](https://github.com/Tao256/sd-forge-wd14-tagger/releases/tag/sd-webui-WD14) 頁面下載最新版本的壓縮包。
2. 將解壓後的資料夾放入 `SD-WebUI-Forge/extensions/` 目錄下。
3. 重新啟動 WebUI，外掛程式將自動載入。

## 🧠 模型

| 模型  | 置信度閾值 | 模型下載 | 說明  |
| :--- | :--- | :--- | :--- |
| wd-convnext-tagger-v3 | 0.3–0.5 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-eva02-large-tagger-v3) <br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-convnext-tagger-v3) | 純卷積架構推理速度快，顯存佔用適中，適合批次處理 |
| wd-eva02-large-tagger-v3 | 0.4–0.6 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-eva02-large-tagger-v3)<br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-eva02-large-tagger-v3) | 能更好地捕捉圖像整體氛圍與風格，標籤關聯性強 | 
| wd-swinv2-tagger-v3 | 0.35–0.55 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-swinv2-tagger-v3)<br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-swinv2-tagger-v3) | 對髮色、眼色、服裝風格等典型動漫特徵辨識準確率高 | 
| wd-vit-tagger-v3 | 0.3–0.45 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-vit-tagger-v3)<br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-vit-tagger-v3) | 生成的標籤之間語義關聯性強，適合提示詞直接使用 | 
| wd-vit-large-tagger-v3 | 0.35–0.5 | [HuggingFace](https://huggingface.co/SmilingWolf/wd-vit-large-tagger-v3)<br>[Modelscope](https://www.modelscope.cn/models/fireicewolf/wd-vit-large-tagger-v3) | ViT-Large 參數量更大，對複雜構圖、細節特徵的辨識能力更強 | 

## 🔗 參考連結

1. **專案首頁**: [https://github.com/Tao256/sd-forge-wd14-tagger](https://github.com/Tao256/sd-forge-wd14-tagger)
2. **Stable Diffusion WebUI Neo**: [https://github.com/lllyasviel/stable-diffusion-webui-forge](https://github.com/lllyasviel/stable-diffusion-webui-forge)
3. **WD14 Tagger**:[https://github.com/picobyte/stable-diffusion-webui-wd14-tagger](https://github.com/picobyte/stable-diffusion-webui-wd14-tagger)