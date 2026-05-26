"""工艺路线自动编排引擎"""
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from datetime import datetime

class ProcessStepType(str, Enum):
    """工序类型"""
    FACE = "端面加工"
    TURNING = "外圆车削"
    DRILLING = "钻孔"
    DEEP_DRILL = "深孔钻"
    MILLING = "面铣"
    PERIPHERAL = "轮廓铣"
    POCKET = "型腔铣"
    BORING = "镗孔"
    TAPPING = "攻丝"
    GROOVING = "切槽"
    THREAD = "螺纹车削"
    PARTING = "切断"

@dataclass
class Feature:
    """加工特征"""
    type: str  # FACE / CYLINDER / HOLE / POCKET / THREAD / GROOVE
    name: str
    x: float = 0
    y: float = 0
    z: float = 0
    length: float = 0
    width: float = 0
    height: float = 0
    diameter: float = 0
    depth: float = 0
    hole_count: int = 0
    hole_positions: list = field(default_factory=list)
    thread_pitch: float = 0
    thread_diameter: float = 0

@dataclass
class ProcessStep:
    """工序"""
    step_num: int
    type: ProcessStepType
    description: str
    tool_type: str
    tool_diameter: float
    spindle_speed: float
    feed_rate: float
    axial_depth: float
    radial_depth: float
    estimated_time: float  # 分钟

@dataclass
class ProcessPlan:
    """工艺方案"""
    part_name: str
    material: str
    steps: List[ProcessStep] = field(default_factory=list)
    total_time: float = 0
    created_at: str = ""
    
    def to_string(self) -> str:
        lines = [
            f"工艺方案: {self.part_name}",
            f"材料: {self.material}",
            f"总加工时间: {self.total_time:.1f} 分钟",
            f"工序数量: {len(self.steps)}",
            "",
            "-" * 60,
        ]
        for s in self.steps:
            lines.append(f"工序{step_num(s.step_num)}: {s.type.value}")
            lines.append(f"  描述: {s.description}")
            lines.append(f"  刀具: {s.tool_type} D={s.tool_diameter:.1f}mm")
            lines.append(f"  主轴: {s.spindle_speed:.0f} RPM")
            lines.append(f"  进给: {s.feed_rate:.0f} mm/min")
            lines.append(f"  切深: ap={s.axial_depth:.2f}mm ar={s.radial_depth:.2f}mm")
            lines.append(f"  预估: {s.estimated_time:.1f}分钟")
            lines.append("")
        return "\n".join(lines)

def step_num(n: int) -> str:
    return f"{n:02d}"

def plan_process(features: List[Feature], material: str, 
                 tool_library: List[dict] = None) -> ProcessPlan:
    """
    根据零件特征自动生成工艺路线
    
    编排原则：
    1. 先面后孔（先加工基准面，再加工孔）
    2. 先粗后精（先粗加工去除余量，后精加工保证精度）
    3. 先近后远（减少空行程）
    4. 同工序合并（相同刀具连续使用）
    
    Args:
        features: 零件特征列表
        material: 工件材料
        tool_library: 刀具库信息
    
    Returns:
        ProcessPlan 工艺方案
    """
    steps = []
    step_counter = 1
    
    # ===== 第一阶段：基准面加工 =====
    face_features = [f for f in features if f.type == "FACE"]
    if face_features:
        for face in face_features:
            steps.append(ProcessStep(
                step_num=step_counter,
                type=ProcessStepType.FACE,
                description=f"{face.name} - 端面粗加工",
                tool_type="面铣刀",
                tool_diameter=face.diameter if face.diameter > 0 else 50,
                spindle_speed=2000,
                feed_rate=2000,
                axial_depth=2.0,
                radial_depth=10.0,
                estimated_time=round(face.length * face.width / 10000 * 60, 1)
            ))
            step_counter += 1
    
    # ===== 第二阶段：外圆车削 =====
    turning_features = [f for f in features if f.type == "CYLINDER"]
    if turning_features:
        for turn in turning_features:
            steps.append(ProcessStep(
                step_num=step_counter,
                type=ProcessStepType.TURNING,
                description=f"{turn.name} - 外圆车削",
                tool_type="车刀",
                tool_diameter=turn.diameter if turn.diameter > 0 else 12,
                spindle_speed=1500,
                feed_rate=200,
                axial_depth=turn.height,
                radial_depth=turn.diameter * 0.2,
                estimated_time=round(turn.length / 200 * 60, 1)
            ))
            step_counter += 1
    
    # ===== 第三阶段：型腔/轮廓铣 =====
    mill_features = [f for f in features if f.type == "POCKET"]
    if mill_features:
        for pocket in mill_features:
            steps.append(ProcessStep(
                step_num=step_counter,
                type=ProcessStepType.POCKET,
                description=f"{pocket.name} - 型腔粗加工",
                tool_type="立铣刀",
                tool_diameter=pocket.diameter if pocket.diameter > 0 else 10,
                spindle_speed=3000,
                feed_rate=1500,
                axial_depth=pocket.height * 0.5,
                radial_depth=pocket.width * 0.3,
                estimated_time=round(pocket.length * pocket.width * pocket.height / 50000 * 60, 1)
            ))
            step_counter += 1
            # 精加工
            steps.append(ProcessStep(
                step_num=step_counter,
                type=ProcessStepType.POCKET,
                description=f"{pocket.name} - 型腔精加工",
                tool_type="立铣刀",
                tool_diameter=pocket.diameter if pocket.diameter > 0 else 10,
                spindle_speed=5000,
                feed_rate=800,
                axial_depth=pocket.height * 0.1,
                radial_depth=pocket.width * 0.05,
                estimated_time=round(pocket.length * pocket.width / 20000 * 60, 1)
            ))
            step_counter += 1
    
    # ===== 第四阶段：钻孔 =====
    hole_features = [f for f in features if f.type == "HOLE"]
    if hole_features:
        for hole in hole_features:
            # 钻头
            steps.append(ProcessStep(
                step_num=step_counter,
                type=ProcessStepType.DRILLING,
                description=f"{hole.name} - 钻孔 (Φ{hole.diameter:.1f} x {hole.hole_count}孔)",
                tool_type="钻头",
                tool_diameter=hole.diameter if hole.diameter > 0 else 6,
                spindle_speed=1000,
                feed_rate=100,
                axial_depth=hole.depth if hole.depth > 0 else 10,
                radial_depth=0,
                estimated_time=round(hole.hole_count * hole.depth / 100 * 60, 1)
            ))
            step_counter += 1
            
            # 铰孔（直径 > 8mm）
            if hole.diameter > 8:
                steps.append(ProcessStep(
                    step_num=step_counter,
                    type=ProcessStepType.BORING,
                    description=f"{hole.name} - 铰孔",
                    tool_type="铰刀",
                    tool_diameter=hole.diameter + 0.1,
                    spindle_speed=500,
                    feed_rate=50,
                    axial_depth=hole.depth * 0.5,
                    radial_depth=0,
                    estimated_time=round(hole.hole_count * 0.5, 1)
                ))
                step_counter += 1
    
    # ===== 第五阶段：攻丝 =====
    thread_features = [f for f in features if f.type == "THREAD"]
    if thread_features:
        for thread in thread_features:
            steps.append(ProcessStep(
                step_num=step_counter,
                type=ProcessStepType.TAPPING,
                description=f"{thread.name} - 攻丝 (M{thread.thread_diameter:.0f} x {thread.thread_pitch:.2f})",
                tool_type="丝锥",
                tool_diameter=thread.thread_diameter,
                spindle_speed=300,
                feed_rate=thread.thread_pitch * 800,
                axial_depth=thread.thread_pitch * 6,
                radial_depth=0,
                estimated_time=round(thread.hole_count * 1, 1)
            ))
            step_counter += 1
    
    # ===== 第六阶段：螺纹车削 =====
    thread_turn = [f for f in features if f.type == "THREAD_EXTERNAL"]
    if thread_turn:
        for tt in thread_turn:
            steps.append(ProcessStep(
                step_num=step_counter,
                type=ProcessStepType.THREAD,
                description=f"{tt.name} - 螺纹车削",
                tool_type="螺纹车刀",
                tool_diameter=tt.diameter if tt.diameter > 0 else 12,
                spindle_speed=800,
                feed_rate=tt.thread_pitch * 800 if tt.thread_pitch > 0 else 1.5 * 800,
                axial_depth=tt.thread_pitch * 0.65,
                radial_depth=0,
                estimated_time=round(tt.length / 100 * 60, 1)
            ))
            step_counter += 1
    
    # ===== 第七阶段：切槽 =====
    groove_features = [f for f in features if f.type == "GROOVE"]
    if groove_features:
        for groove in groove_features:
            steps.append(ProcessStep(
                step_num=step_counter,
                type=ProcessStepType.GROOVING,
                description=f"{groove.name} - 切槽",
                tool_type="切槽刀",
                tool_diameter=groove.width if groove.width > 0 else 2,
                spindle_speed=500,
                feed_rate=30,
                axial_depth=groove.width,
                radial_depth=0,
                estimated_time=round(groove.hole_count * 0.5, 1)
            ))
            step_counter += 1
    
    # 计算总时间
    total_time = sum(s.estimated_time for s in steps)
    
    return ProcessPlan(
        part_name=features[0].name if features else "Unknown",
        material=material,
        steps=steps,
        total_time=total_time,
        created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

def run_demo_plan():
    """运行工艺编排演示"""
    demo_features = [
        Feature("FACE", "基准面", diameter=80, length=100, width=80),
        Feature("CYLINDER", "外圆", diameter=40, length=60, height=5),
        Feature("POCKET", "型腔A", length=50, width=40, height=15, diameter=12),
        Feature("HOLE", "安装孔", diameter=8, depth=20, hole_count=4,
                 hole_positions=[(10,10), (10,70), (90,10), (90,70)]),
        Feature("THREAD", "螺纹孔", thread_diameter=10, thread_pitch=1.5, hole_count=2),
    ]
    
    plan = plan_process(demo_features, "45号钢")
    print(plan.to_string())

if __name__ == "__main__":
    run_demo_plan()
