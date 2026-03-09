import launch
import os

# 标记文件路径（扩展目录下）
marker_file = os.path.join(os.path.dirname(__file__), "tagger_deps_installed")

#WD14
required_packages = ["onnxruntime-gpu", 
                     "onnxruntime", 
                     "Pillow>=10.2.0"]
if not os.path.exists(marker_file):
    with open(marker_file, "w") as f:
        f.write("Installed")# 创建标记文件
    print("[Tagger-all]checking Python packages...")
    if not launch.is_installed(required_packages[0]) and not launch.is_installed(required_packages[1]):
        try:
            launch.run_pip(f"install {required_packages[0]}", f"{required_packages[0]} requirements for forge Tagger")
        except Exception:
            launch.run_pip(f"install {required_packages[1]}", f"{required_packages[1]} requirements for forge Tagger")
    for pkg in required_packages[2:]:
        if not launch.is_installed(pkg):
            print(f"[Tagger-all]Package '{pkg}' is not installed. Installing...")
            try:
                launch.run_pip(f"install {pkg}", f"{pkg} requirements for forge Tagger")
            except Exception as e:
                print(f"Warning: install {pkg} failed: {e}")
                os.remove(marker_file)  # 安装失败，删除标记文件以便下次重试
                break

