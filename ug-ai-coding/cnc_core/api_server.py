"""REST API 服务 - FastAPI"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cnc_core.cutting_params import Material, ToolType, calculate_params, get_all_materials, get_all_tool_types
from cnc_core.gcode_generator import (
    generate_gcode, Operation, Tool, Workpiece, GCodeProgram
)
from cnc_core.post_processor import PostProcessor, apply_postproc, generate_post_header
from cnc_core.toolpath_simulator import (
    simulate_toolpath, SimulationResult, generate_test_toolpath,
    ToolPathPoint, BoundingBox, CollisionZone
)
from cnc_core.process_planner import plan_process, Feature, ProcessPlan
from cnc_core.database import init_database, save_process_plan, get_all_plans, log_operation

# ========== FastAPI App ==========
app = FastAPI(
    title="UG AI 自动编程插件 API",
    description="零件图纸 → 工艺规划 → G代码生成 → 刀路仿真 → 机床验证",
    version="1.0.0"
)

# 初始化数据库
init_database()

# ========== Pydantic Models ==========
class CutRequest(BaseModel):
    material: str
    tool_type: str
    tool_diameter: float
    operation: str = "roughing"  # roughing / finishing

class Hole(BaseModel):
    x: float = 0
    y: float = float
    depth: float = 10

class FeatureInput(BaseModel):
    type: str
    name: str
    x: float = 0
    y: float = 0
    z: float = 0
    length: float = 0
    width: float = 0
    height: float = 0
    diameter: float = 0
    depth: float = 0
    hole_count: int = 1
    hole_positions: list = None
    thread_pitch: float = 0
    thread_diameter: float = 0
    material_name: str = "45号钢"

class GCodeRequest(BaseModel):
    operation: str
    material: str
    tool_type: str
    tool_diameter: float
    workpiece_length: float
    workpiece_width: float
    workpiece_height: float
    workpiece_x: float = 0
    workpiece_y: float = 0
    workpiece_z: float = 0
    holes: List[Hole] = None
    post_processor: str = "FANUC"

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str

# ========== API Endpoints ==========

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        timestamp=__import__('datetime').datetime.now().isoformat(),
        version="1.0.0"
    )

@app.get("/materials")
async def list_materials():
    """获取所有材料列表"""
    return {"materials": get_all_materials()}

@app.get("/tool-types")
async def list_tool_types():
    """获取所有刀具类型列表"""
    return {"tool_types": get_all_tool_types()}

@app.post("/cutting-params")
async def get_cutting_params(req: CutRequest):
    """计算切削参数"""
    try:
        material = Material(req.material)
    except ValueError:
        raise HTTPException(400, f"未知材料: {req.material}")
    
    try:
        tool_type = ToolType(req.tool_type)
    except ValueError:
        raise HTTPException(400, f"未知刀具类型: {req.tool_type}")
    
    params = calculate_params(material, tool_type, req.tool_diameter, req.operation)
    return {
        "spindle_speed": params.spindle_speed,
        "feed_rate": params.feed_rate,
        "axial_depth": params.axial_depth,
        "radial_depth": params.radial_depth,
        "cutting_speed": params.cutting_speed,
        "feed_per_tooth": params.feed_per_tooth,
        "material": params.material,
        "tool_type": params.tool_type,
        "tool_diameter": params.tool_diameter
    }

@app.post("/generate-gcode")
async def generate_gcode_api(req: GCodeRequest):
    """生成G代码"""
    try:
        op = Operation(req.operation)
    except ValueError:
        raise HTTPException(400, f"未知操作: {req.operation}")
    
    try:
        material = Material(req.material)
    except ValueError:
        raise HTTPException(400, f"未知材料: {req.material}")
    
    try:
        tool_type = ToolType(req.tool_type)
    except ValueError:
        raise HTTPException(400, f"未知刀具类型: {req.tool_type}")
    
    # 计算切削参数
    cut_params = calculate_params(material, tool_type, req.tool_diameter, "roughing")
    
    # 创建刀具和工件
    tool = Tool(
        type=tool_type.value,
        diameter=req.tool_diameter,
        tool_number=1
    )
    workpiece = Workpiece(
        name="Part",
        length=req.workpiece_length,
        width=req.workpiece_width,
        height=req.workpiece_height,
        x_origin=req.workpiece_x,
        y_origin=req.workpiece_y,
        z_origin=req.workpiece_z
    )
    
    # 生成G代码
    program = generate_gcode(
        operation=op,
        tool=tool,
        workpiece=workpiece,
        params={
            "spindle_speed": cut_params.spindle_speed,
            "feed_rate": cut_params.feed_rate,
            "axial_depth": cut_params.axial_depth,
            "radial_depth": cut_params.radial_depth,
            "cutting_speed": cut_params.cutting_speed,
            "feed_per_tooth": cut_params.feed_per_tooth,
            "start_time": __import__('datetime').datetime.now().isoformat()
        },
        holes=req.holes
    )
    
    # 后处理
    post_type = PostProcessor(req.post_processor)
    gcode_str = apply_postproc(program.to_string(), post_type)
    
    # 保存数据库
    save_process_plan(
        part_name="Part",
        material=req.material,
        tool_list=[{"type": tool_type.value, "diameter": req.tool_diameter}],
        parameters={"cutting_params": {
            "spindle_speed": cut_params.spindle_speed,
            "feed_rate": cut_params.feed_rate,
            "axial_depth": cut_params.axial_depth,
            "radial_depth": cut_params.radial_depth,
            "cutting_speed": cut_params.cutting_speed,
        }},
        gcode=gcode_str
    )
    
    return {
        "program": program.to_string(),
        "gcode": gcode_str,
        "post_processor": post_type.value,
        "cutting_params": {
            "spindle_speed": cut_params.spindle_speed,
            "feed_rate": cut_params.feed_rate,
            "axial_depth": cut_params.axial_depth,
            "radial_depth": cut_params.radial_depth,
            "cutting_speed": cut_params.cutting_speed,
            "feed_per_tooth": cut_params.feed_per_tooth,
        },
        "tool_info": {
            "type": tool.type,
            "diameter": tool.diameter,
            "number": tool.tool_number
        }
    }

@app.post("/plan-process")
async def plan_process_api(features: List[FeatureInput], material: str = "45号钢"):
    """自动生成工艺路线"""
    feat_list = [
        Feature(
            type=f.type, name=f.name, x=f.x, y=f.y, z=f.z,
            length=f.length, width=f.width, height=f.height,
            diameter=f.diameter, depth=f.depth,
            hole_count=f.hole_count, hole_positions=f.hole_positions or [],
            thread_pitch=f.thread_pitch, thread_diameter=f.thread_diameter
        ) for f in features
    ]
    
    plan = plan_process(feat_list, material)
    
    return {
        "part_name": plan.part_name,
        "material": plan.material,
        "total_time": plan.total_time,
        "steps_count": len(plan.steps),
        "created_at": plan.created_at,
        "steps": [
            {
                "step": s.step_num,
                "type": s.type.value,
                "description": s.description,
                "tool_type": s.tool_type,
                "tool_diameter": s.tool_diameter,
                "spindle_speed": s.spindle_speed,
                "feed_rate": s.feed_rate,
                "axial_depth": s.axial_depth,
                "radial_depth": s.radial_depth,
                "estimated_time": s.estimated_time,
            }
            for s in plan.steps
        ]
    }

@app.post("/simulate")
async def simulate(request: dict):
    """刀路仿真与碰撞检测"""
    points_data = request.get("points", [])
    if not points_data:
        raise HTTPException(400, "需要刀路点数据")
    
    points = [ToolPathPoint(**p) for p in points_data]
    wp_bbox = BoundingBox(**request.get("workpiece", {}))
    zones_data = request.get("zones", [])
    zones = [CollisionZone(BoundingBox(**z["bbox"]), z["zone_type"], z["name"]) for z in zones_data]
    
    result = simulate_toolpath(
        points, wp_bbox, zones,
        request.get("tool_diameter", 10),
        request.get("tool_length", 80)
    )
    
    return {
        "total_points": result.total_points,
        "cutting_points": result.cutting_points,
        "air_points": result.air_points,
        "total_time": round(result.total_time, 2),
        "max_spindle": result.max_spindle,
        "max_feed": result.max_feed,
        "collisions": [
            {"type": c.type, "location": c.location, "description": c.description, "severity": c.severity}
            for c in result.collisions
        ],
        "warnings": result.warnings,
    }

@app.get("/plans")
async def list_plans():
    """获取所有工艺方案"""
    plans = get_all_plans()
    return {"plans": plans}

@app.get("/demo-plan")
async def demo_plan():
    """工艺编排演示"""
    from cnc_core.process_planner import run_demo_plan as demo
    demo()
    return {"message": "Demo completed"}

@app.get("/demo-sim")
async def demo_sim():
    """刀路仿真演示"""
    from cnc_core.toolpath_simulator import run_demo_simulation as demo
    demo()
    return {"message": "Demo completed"}
