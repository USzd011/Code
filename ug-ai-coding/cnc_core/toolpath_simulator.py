"""刀路仿真与碰撞检测引擎"""
import math
from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from enum import Enum

class CollisionType(str, Enum):
    TOOL_WORKPIECE = "刀具-工件碰撞"
    TOOL_CLAMP = "刀具-夹具碰撞"
    TOOL_SPINDLE = "刀具-主轴碰撞"
    OVERCUT = "过切"
    UNDERCUT = "欠切"
    AIR_CUT = "空刀"

@dataclass
class Collision:
    type: str
    location: Tuple[float, float, float]
    description: str
    severity: str  # CRITICAL / WARNING / INFO

@dataclass
class ToolPathPoint:
    x: float
    y: float
    z: float
    feed: float = 0
    spindle: int = 0
    tool_num: int = 0
    move_type: str = "G0"  # G0/G1

@dataclass
class BoundingBox:
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float

@dataclass
class CollisionZone:
    """碰撞区域定义"""
    bbox: BoundingBox
    zone_type: str  # WORKPIECE / CLAMP / FIXTURE
    name: str

@dataclass
class SimulationResult:
    total_points: int = 0
    cutting_points: int = 0
    air_points: int = 0
    collisions: List[Collision] = field(default_factory=list)
    total_time: float = 0.0  # 预估加工时间 分钟
    max_spindle: int = 0
    max_feed: float = 0
    warnings: List[str] = field(default_factory=list)

def simulate_toolpath(
    tool_path_points: List[ToolPathPoint],
    workpiece_bbox: BoundingBox,
    collision_zones: List[CollisionZone],
    tool_diameter: float,
    tool_length: float
) -> SimulationResult:
    """
    刀路仿真与碰撞检测
    
    Args:
        tool_path_points: 刀路点序列
        workpiece_bbox: 工件包围盒
        collision_zones: 碰撞区域列表
        tool_diameter: 刀具直径
        tool_length: 刀具长度
    
    Returns:
        SimulationResult
    """
    result = SimulationResult()
    result.total_points = len(tool_path_points)
    
    for i, pt in enumerate(tool_path_points):
        result.max_spindle = max(result.max_spindle, pt.spindle)
        result.max_feed = max(result.max_feed, pt.feed)
        
        # 判断是切削还是空刀
        if pt.move_type == "G1" and pt.feed > 0:
            in_material = (
                workpiece_bbox.min_x - tool_diameter <= pt.x <= workpiece_bbox.max_x + tool_diameter and
                workpiece_bbox.min_y - tool_diameter <= pt.y <= workpiece_bbox.max_y + tool_diameter and
                workpiece_bbox.min_z <= pt.z <= workpiece_bbox.max_z
            )
            if in_material:
                result.cutting_points += 1
            else:
                result.air_points += 1
                result.collisions.append(Collision(
                    type=CollisionType.AIR_CUT,
                    location=(pt.x, pt.y, pt.z),
                    description=f"空刀: 点{i} X={pt.x:.3f} Y={pt.y:.3f} Z={pt.z:.3f}",
                    severity="INFO"
                ))
        
        # 碰撞检测
        for zone in collision_zones:
            z = zone.bbox
            in_zone = (
                z.min_x - tool_diameter/2 <= pt.x <= z.max_x + tool_diameter/2 and
                z.min_y - tool_diameter/2 <= pt.y <= z.max_y + tool_diameter/2 and
                z.min_z <= pt.z <= z.max_z
            )
            if in_zone:
                result.collisions.append(Collision(
                    type=CollisionType.TOOL_WORKPIECE,
                    location=(pt.x, pt.y, pt.z),
                    description=f"碰撞: 刀具接近{zone.name} (X={pt.x:.3f} Y={pt.y:.3f} Z={pt.z:.3f})",
                    severity="CRITICAL"
                ))
        
        # 刀具长度检查
        if pt.z < -tool_length + 5:
            result.collisions.append(Collision(
                type=CollisionType.TOOL_SPINDLE,
                location=(pt.x, pt.y, pt.z),
                description=f"刀具过长: Z={pt.z:.3f} 超过安全深度 (工具长={tool_length})",
                severity="WARNING"
            ))
        
        # 计算加工时间（G1 移动）
        if pt.move_type == "G1" and pt.feed > 0 and i > 0:
            prev = tool_path_points[i-1]
            dist = math.sqrt(
                (pt.x - prev.x)**2 + (pt.y - prev.y)**2 + (pt.z - prev.z)**2
            )
            if dist > 0:
                time_min = dist / pt.feed  # 分钟
                result.total_time += time_min
    
    # 生成警告
    if result.air_points > result.cutting_points * 0.3:
        result.warnings.append("空刀比例过高，优化刀路可提升效率")
    if result.total_time > 60:
        result.warnings.append(f"预估加工时间 {result.total_time:.1f} 分钟，超出1小时阈值")
    
    critical_count = sum(1 for c in result.collisions if c.severity == "CRITICAL")
    if critical_count > 0:
        result.warnings.append(f"发现 {critical_count} 个关键碰撞，必须修正!")
    
    return result

def generate_test_toolpath() -> List[ToolPathPoint]:
    """生成测试刀路用于验证仿真引擎"""
    points = [
        ToolPathPoint(10, 10, 5, 0, 0, 1, "G0"),
        ToolPathPoint(10, 10, 2, 1000, 3000, 1, "G1"),
        ToolPathPoint(20, 10, 2, 1000, 3000, 1, "G1"),
        ToolPathPoint(20, 20, 2, 1000, 3000, 1, "G1"),
        ToolPathPoint(10, 20, 2, 1000, 3000, 1, "G1"),
        ToolPathPoint(10, 10, 2, 1000, 3000, 1, "G1"),
        ToolPathPoint(10, 10, 5, 0, 0, 1, "G0"),
    ]
    return points

def run_demo_simulation():
    """运行仿真演示"""
    # 模拟数据
    points = generate_test_toolpath()
    wp_bbox = BoundingBox(5, 5, 0, 25, 25, 10)
    zones = [
        CollisionZone(
            BoundingBox(0, 0, -1, 8, 8, 10),
            "CLAMP", "夹具A"
        )
    ]
    
    result = simulate_toolpath(points, wp_bbox, zones, 10, 80)
    
    print("=" * 60)
    print("刀路仿真结果")
    print("=" * 60)
    print(f"总点数: {result.total_points}")
    print(f"切削点数: {result.cutting_points}")
    print(f"空刀点数: {result.air_points}")
    print(f"预估加工时间: {result.total_time:.2f} 分钟")
    print(f"最大主轴转速: {result.max_spindle} RPM")
    print(f"最大进给: {result.max_feed} mm/min")
    print(f"碰撞数: {len(result.collisions)}")
    if result.warnings:
        print(f"警告: {len(result.warnings)}")
        for w in result.warnings:
            print(f"  ⚠️ {w}")
    if result.collisions:
        print("\n碰撞详情:")
        for c in result.collisions:
            sev = "🔴" if c.severity == "CRITICAL" else ("🟡" if c.severity == "WARNING" else "🟢")
            print(f"  {sev} [{c.severity}] {c.type}: {c.description}")

if __name__ == "__main__":
    run_demo_simulation()
