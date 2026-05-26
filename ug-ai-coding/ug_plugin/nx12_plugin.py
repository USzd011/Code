"""UG/NX 12.0 插件主程序"""
# 注意: 实际使用时需要在 UG NX 环境中运行
# 此文件为插件框架结构，需根据实际 UG Open API 调整

import sys
import os
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class NXPlugin:
    """UG NX 12.0 插件主类"""
    
    def __init__(self):
        self.title = "UG AI Auto Programming"
        self.version = "1.0.0"
        self.author = "4号腾云"
        self.description = "AI 自动编程插件 - 从零件到G代码"
        
        # 检查依赖
        self._check_dependencies()
    
    def _check_dependencies(self):
        """检查依赖"""
        try:
            import nxopen
            self.nxopen_available = True
        except ImportError:
            self.nxopen_available = False
    
    def create_tab(self, the_session, base_dialog):
        """在 UG 中创建 UI 标签页"""
        if not self.nxopen_available:
            print("[UG AI] nxopen 不可用，跳过 UI 创建")
            return None
        
        # 创建标签页
        tab = base_dialog.create_tab(self.title)
        
        # 创建工艺配置面板
        config_panel = self._create_config_panel(tab)
        
        # 创建 G代码预览面板
        gcode_panel = self._create_gcode_panel(tab)
        
        return tab
    
    def _create_config_panel(self, tab):
        """创建工艺配置面板"""
        from cnc_core.cutting_params import get_all_materials, get_all_tool_types
        
        # 材料选择
        materials = get_all_materials()
        # 刀具类型
        tool_types = get_all_tool_types()
        
        # 在 UG UI 中创建控件
        # 实际实现需要 NX Open API
        return {
            "materials": materials,
            "tool_types": tool_types,
        }
    
    def _create_gcode_panel(self, tab):
        """创建G代码预览面板"""
        # 在 UG UI 中创建文本区域显示G代码
        return {"type": "text_display"}
    
    def generate_program(self, part_data: dict, process_params: dict) -> str:
        """
        一键生成G代码
        
        Args:
            part_data: 零件数据
            process_params: 工艺参数
        
        Returns:
            G代码字符串
        """
        from cnc_core.gcode_generator import (
            generate_gcode, Operation, Tool, Workpiece
        )
        from cnc_core.cutting_params import Material, ToolType, calculate_params
        from cnc_core.post_processor import PostProcessor, apply_postproc
        
        # 生成G代码
        tool = Tool(
            type=process_params.get("tool_type", "立铣刀"),
            diameter=process_params.get("tool_diameter", 10),
            tool_number=1
        )
        workpiece = Workpiece(
            name=part_data.get("name", "Part"),
            length=part_data.get("length", 100),
            width=part_data.get("width", 80),
            height=part_data.get("height", 20),
        )
        
        cut_params = calculate_params(
            Material.STEEL_45,
            ToolType.END_MILL,
            10, "roughing"
        )
        
        program = generate_gcode(
            operation=Operation.MILLING,
            tool=tool,
            workpiece=workpiece,
            params={
                "spindle_speed": cut_params.spindle_speed,
                "feed_rate": cut_params.feed_rate,
                "axial_depth": cut_params.axial_depth,
                "radial_depth": cut_params.radial_depth,
                "cutting_speed": cut_params.cutting_speed,
                "feed_per_tooth": cut_params.feed_per_tooth,
            }
        )
        
        gcode = apply_postproc(program.to_string(), PostProcessor.FANUC)
        return gcode

def main():
    """插件入口"""
    plugin = NXPlugin()
    print(f"[UG AI] 插件启动: {plugin.title} v{plugin.version}")
    print(f"[UG AI] nxopen 可用: {plugin.nxopen_available}")
    
    if not plugin.nxopen_available:
        print("[UG AI] 提示: 在 UG NX 12.0 环境中运行此插件")
        print("[UG AI] 或使用 API 模式: curl http://localhost:8000/generate-gcode")

if __name__ == "__main__":
    main()
