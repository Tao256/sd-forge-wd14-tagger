import csv
import gc 
import os
import gradio as gr
import numpy as np
from PIL import Image
import onnxruntime as ort

# --- 模型配置 ---
MODEL_CONFIGS = {
    "wd-vit-tagger-v3": {
        "repo_id": "SmilingWolf/wd-vit-tagger-v3",
        "onnx_filename": "wd-vit-tagger-v3.onnx", 
        "csv_filename": "wd-vit-tagger-v3.csv", 
        "size": 448
    },
    "wd-convnext-tagger-v3": {
        "repo_id": "SmilingWolf/wd-convnext-tagger-v3",
        "onnx_filename": "wd-convnext-tagger-v3.onnx", 
        "csv_filename": "wd-convnext-tagger-v3.csv", 
        "size": 448
    },
    "wd-swinv2-tagger-v3": {
        "repo_id": "SmilingWolf/wd-swinv2-tagger-v3",
        "onnx_filename": "wd-swinv2-tagger-v3.onnx", 
        "csv_filename": "wd-swinv2-tagger-v3.csv", 
        "size": 448
    },
    "wd-eva02-large-tagger-v3": {
        "repo_id": "SmilingWolf/wd-eva02-large-tagger-v3",
        "onnx_filename": "wd-eva02-large-tagger-v3.onnx", 
        "csv_filename": "wd-eva02-large-tagger-v3.csv", 
        "size": 448
    },
    "wd-vit-large-tagger-v3":{
        "repo_id": "SmilingWolf/wd-vit-large-tagger-v3",
        "onnx_filename": "wd-vit-large-tagger-v3.onnx", 
        "csv_filename": "wd-vit-large-tagger-v3.csv", 
        "size": 448
    }
}

class WD14Tagger:
    def __init__(self, models_dir, csv_dir):
        self.models_dir = models_dir
        self.csv_dir = csv_dir
        self.model_loaded = False
        self.current_model_id = None
        self.session = None
        self.tags = {} 
        self.model_configs = MODEL_CONFIGS
        self.model_configs_list=list(self.model_configs.keys())

    def load_tags(self, model_id, csv_filename):
        if model_id in self.tags:
            return True 

        tags_path = self.csv_dir / csv_filename

        if tags_path.exists():
            try:
                with open(tags_path, encoding="utf-8") as f:
                    reader = csv.reader(f)
                    model_tags = []
                    for i, row in enumerate(reader):
                        if len(row) > 1:
                            if i == 0 and ("name" in row or "tag" in row[1]):
                                continue
                            model_tags.append(row[1]) 
                
                self.tags[model_id] = model_tags 
                return True
            except Exception as e:
                print(f"[Tagger-all] {csv_filename} load failed: {e}")
                return False
        else:
            print(f"[Tagger-all]{tags_path} not found.")
            return False

    def unload_model(self):
        if self.model_loaded:
            del self.session
            self.session = None
            self.model_loaded = False
            self.current_model_id = None
            gc.collect() 
            return gr.Info("Model has been released")
        return gr.Info("No model loading")

    def load_model(self, model_id):
        if self.current_model_id == model_id and self.model_loaded:
            return
  
        if self.model_loaded:
            del self.session
            self.session = None
            self.model_loaded = False
            self.current_model_id = None
            gc.collect() 

        config = self.model_configs.get(model_id)
        if not config:
            return gr.Error(f"{model_id} could not be found.")
        
        if not self.load_tags(model_id, config["csv_filename"]):
            return gr.Error("csv failed to load")

        model_path = self.models_dir / config["onnx_filename"]

        if not model_path.exists():
            return gr.Error(f"({config['onnx_filename']}) could not be found。find：{model_path.resolve()}。")
        
        print(f'[Tagger-all]:Loading "{model_id}" from "{model_path}"...')
        try:
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            self.session = ort.InferenceSession(str(model_path), providers=providers)
            
            self.model_loaded = True
            self.current_model_id = model_id
        except Exception as e:
            self.unload_model() 
            return gr.Error(f"fail to load - {e}")

    def predict(self, image, model_id, threshold=0.35):
        if not image:
            return gr.Info("Please provide the image first"), "---"
        
        self.load_model(model_id)

        try:
            target_size = self.model_configs[model_id]['size']
            
            if image.mode != 'RGB':
                image = image.convert("RGB")
            
            image = image.resize((target_size, target_size), Image.LANCZOS)
            img_array = np.array(image, dtype=np.float32)
            img_array = img_array[:, :, ::-1] # BGR
            input_tensor = np.expand_dims(img_array, axis=0)
            
        except Exception as e:
            return gr.Error(f"Image preprocessing failed - {e}"), "---"

        try:
            print(f"[Tagger-all]loadding {model_id}")
            input_name = self.session.get_inputs()[0].name
            output_name = self.session.get_outputs()[0].name
            probs = self.session.run([output_name], {input_name: input_tensor})[0]
            probs = probs.flatten()
        except Exception as e:
            return gr.Error(f"ONNX inference execution failed - {e}"), "---"

        current_tags = self.tags[model_id]
        if len(current_tags) != len(probs):
             return gr.Error(f"Number of tags ({len(current_tags)}) ,Number of model outputs ({len(probs)}), Mismatch."), "---"
        
        tag_scores = zip(current_tags, probs)
        
        filtered_tags_with_scores = sorted(
            [(tag, score) for tag, score in tag_scores if score >= threshold],
            key=lambda x: x[1], 
            reverse=True
        )

        rating_tags = []
        general_tags = []
        rating_categories = ["general", "sensitive", "questionable", "explicit"] 

        for tag, score in filtered_tags_with_scores:
            if tag in rating_categories:
                rating_tags.append(tag)
            else:
                clean_tag = tag.replace("_", " ")
                general_tags.append(clean_tag)

        tags_str = ", ".join(general_tags)
        
        if rating_tags:
            rating_str = f"Rating: {rating_tags[0].upper()}"
        else:
            rating_str = "Rating: GENERAL"     
        return tags_str, rating_str

    def multi_predict(self, images_route, model_id, threshold=0.35):
        tags_strs=dict()
        if not images_route:
            return gr.Info("Please provide the image first")
        self.load_model(model_id)
        target_size = self.model_configs[model_id]['size']

        for i,image_route in enumerate(images_route):
            image = Image.open(image_route)
            if image.mode != 'RGB':
                image = image.convert("RGB")
            
            image = image.resize((target_size, target_size), Image.LANCZOS)
            img_array = np.array(image, dtype=np.float32)
            img_array = img_array[:, :, ::-1] # BGR
            input_tensor = np.expand_dims(img_array, axis=0)
            print(f"[Tagger-all]loadding {model_id} ,current image:{i+1}...")
            input_name = self.session.get_inputs()[0].name
            output_name = self.session.get_outputs()[0].name
            probs = self.session.run([output_name], {input_name: input_tensor})[0]
            probs = probs.flatten()
            current_tags = self.tags[model_id]
            if len(current_tags) != len(probs):
                return gr.Error(f"Number of tags ({len(current_tags)}) ,Number of model outputs ({len(probs)}), Mismatch.")
            tag_scores = zip(current_tags, probs)
            filtered_tags_with_scores = sorted(
                [(tag, score) for tag, score in tag_scores if score >= threshold],
                key=lambda x: x[1], 
                reverse=True
            )
            rating_tags = []
            general_tags = []
            rating_categories = ["general", "sensitive", "questionable", "explicit"]
            for tag, score in filtered_tags_with_scores:
                if tag in rating_categories:
                    rating_tags.append(tag)
                else:
                    clean_tag = tag.replace("_", " ")
                    general_tags.append(clean_tag)

            tags_str = ", ".join(general_tags)

            route=image_route.split("/")[-1] if "/" in image_route else image_route.split("\\")[-1]
            tags_strs[route] = tags_str
        return tags_strs
    
    def folder_predict(self,folder_route,model_id, threshold=0.35):
        image_routes = []
        if not folder_route:
            return gr.Info("Please provide the image folder path first")
 
        for filename in os.listdir(folder_route):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                image_route = os.path.join(folder_route, filename)
                image_routes.append(image_route)
        if not image_routes:
            return gr.Info("No valid image files were found in the folder")
        tags_str = self.multi_predict(image_routes, model_id, threshold)
        return tags_str








