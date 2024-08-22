from pathlib import Path
# 获取当前脚本的绝对路径
current_script_path = Path(__file__).resolve()
# 获取当前脚本所在的目录
current_script_dir = current_script_path.parent
# 获取项目的根目录
dir_path = current_script_dir.parent  # 根据需要调整级别
dir_path = Path(dir_path)  # 替换为你的实际目录路径
