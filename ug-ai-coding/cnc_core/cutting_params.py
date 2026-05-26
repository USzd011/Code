"""切削参数计算器 - 14种材料 x 10种刀具"""
import math
from dataclasses import dataclass
from typing import List
from enum import Enum

class Material(str, Enum):
    Q235 = "Q235碳钢"
    STEEL_45 = "45号钢"
    CR40 = "40Cr合金钢"
    CR40NI = "40CrNiMo"
    CR12MOV = "Cr12MoV冷作模具钢"
    H13 = "H13热作模具钢"
    CR40MO = "40CrMo"
    CR20MO = "20CrMo"
    TC4 = "TC4钛合金"
    INCONEL718 = "Inconel718高温合金"
    AL6061 = "AL6061铝合金"
    AL7075 = "AL7075铝合金"
    CU110 = "紫铜C110"
    POM = "POM聚甲醛"

class ToolType(str, Enum):
    FACE_MILL = "面铣刀"
    END_MILL = "立铣刀"
    BALL_MILL = "球头铣刀"
    TURNING_TOOL = "车刀"
    DRILL = "钻头"
    REAMER = "铰刀"
    TAP = "丝锥"
    BORE = "镗刀"
    GROOVE = "切槽刀"
    THREAD_TURNING = "螺纹车刀"

@dataclass
class CuttingParams:
    spindle_speed: float
    feed_rate: float
    axial_depth: float
    radial_depth: float
    cutting_speed: float
    feed_per_tooth: float
    material: str
    tool_type: str
    tool_diameter: float

MATERIAL_PROFILES = {
    Material.Q235:      {"hardness": 120, "thermal": 52, "strength": 1.0, "max_speed": 200},
    Material.STEEL_45:  {"hardness": 180, "thermal": 45, "strength": 1.2, "max_speed": 180},
    Material.CR40:      {"hardness": 250, "thermal": 42, "strength": 1.4, "max_speed": 150},
    Material.CR40NI:    {"hardness": 280, "thermal": 40, "strength": 1.5, "max_speed": 140},
    Material.CR12MOV:   {"hardness": 580, "thermal": 25, "strength": 1.6, "max_speed": 100},
    Material.H13:       {"hardness": 520, "thermal": 28, "strength": 1.5, "max_speed": 110},
    Material.CR40MO:    {"hardness": 260, "thermal": 41, "strength": 1.4, "max_speed": 145},
    Material.CR20MO:    {"hardness": 200, "thermal": 44, "strength": 1.2, "max_speed": 170},
    Material.TC4:       {"hardness": 330, "thermal": 6.7, "strength": 2.0, "max_speed": 60},
    Material.INCONEL718:{"hardness": 350, "thermal": 11, "strength": 2.2, "max_speed": 45},
    Material.AL6061:    {"hardness": 90,  "thermal": 167, "strength": 0.5, "max_speed": 500},
    Material.AL7075:    {"hardness": 120, "thermal": 130, "strength": 0.6, "max_speed": 450},
    Material.CU110:     {"hardness": 80,  "thermal": 385, "strength": 0.4, "max_speed": 400},
    Material.POM:       {"hardness": 70,  "thermal": 0.3, "strength": 0.3, "max_speed": 600},
}

TOOL_PROFILES = {
    ToolType.FACE_MILL:     {"feed_coeff": 0.10, "axial_coeff": 1.0, "flutes": 4},
    ToolType.END_MILL:      {"feed_coeff": 0.08, "axial_coeff": 0.8, "flutes": 4},
    ToolType.BALL_MILL:     {"feed_coeff": 0.06, "axial_coeff": 0.5, "flutes": 3},
    ToolType.TURNING_TOOL:  {"feed_coeff": 0.12, "axial_coeff": 1.2, "flutes": 1},
    ToolType.DRILL:         {"feed_coeff": 0.15, "axial_coeff": 3.0, "flutes": 2},
    ToolType.REAMER:        {"feed_coeff": 0.10, "axial_coeff": 0.3, "flutes": 6},
    ToolType.TAP:           {"feed_coeff": 1.0,  "axial_coeff": 0.1, "flutes": 4},
    ToolType.BORE:          {"feed_coeff": 0.08, "axial_coeff": 0.6, "flutes": 3},
    ToolType.GROOVE:        {"feed_coeff": 0.04, "axial_coeff": 0.2, "flutes": 1},
    ToolType.THREAD_TURNING:{"feed_coeff": 1.0,  "axial_coeff": 0.1, "flutes": 1},
}

def calc_spindle_speed(cutting_speed: float, diameter: float) -> float:
    if diameter <= 0: return 0
    return round(cutting_speed * 1000 / (math.pi * diameter))

def calc_feed_rate(rpm: float, fz: float, flutes: int) -> float:
    return round(rpm * fz * flutes)

def calculate_params(material: Material, tool_type: ToolType,
                     tool_diameter: float, operation: str = "roughing") -> CuttingParams:
    mp = MATERIAL_PROFILES[material]
    tp = TOOL_PROFILES[tool_type]
    
    hardness_factor = max(0.3, 1.0 - (mp["hardness"] - 70) / 600)
    thermal_factor = min(1.0, mp["thermal"] / 50)
    base_speed = mp["max_speed"] * hardness_factor * thermal_factor
    
    if operation == "finishing": base_speed *= 0.7
    if tool_diameter < 6: base_speed *= 0.8
    elif tool_diameter < 10: base_speed *= 0.9
    
    cutting_speed = round(base_speed, 1)
    spindle_speed = calc_spindle_speed(cutting_speed, tool_diameter)
    
    if tool_type in (ToolType.TAP, ToolType.THREAD_TURNING):
        feed_per_tooth = round(tool_diameter * 0.075, 3)
    else:
        fz_base = tp["feed_coeff"] * hardness_factor
        if operation == "finishing": fz_base *= 0.5
        feed_per_tooth = round(fz_base, 4)
    
    feed_rate = calc_feed_rate(spindle_speed, feed_per_tooth, tp["flutes"])
    
    depth_scale = 0.5 if operation == "roughing" else 0.05
    axial_depth = round(tool_diameter * tp["axial_coeff"] * depth_scale, 2)
    radial_coeff = 0.3 if tool_type != ToolType.TURNING_TOOL else 1.0
    radial_depth = round(tool_diameter * radial_coeff * depth_scale, 2)
    
    return CuttingParams(
        spindle_speed=spindle_speed, feed_rate=feed_rate,
        axial_depth=axial_depth, radial_depth=radial_depth,
        cutting_speed=cutting_speed, feed_per_tooth=feed_per_tooth,
        material=material.value, tool_type=tool_type.value,
        tool_diameter=tool_diameter
    )

def get_all_materials() -> List[str]:
    return [m.value for m in Material]

def get_all_tool_types() -> List[str]:
    return [t.value for t in ToolType]
