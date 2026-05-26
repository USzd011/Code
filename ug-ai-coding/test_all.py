"""UG AI 自动编程插件 - 测试套件"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cnc_core.cutting_params import (
    Material, ToolType, calculate_params, get_all_materials, get_all_tool_types
)
from cnc_core.gcode_generator import (
    generate_gcode, Operation, Tool, Workpiece, GCodeProgram
)
from cnc_core.post_processor import PostProcessor, apply_postproc
from cnc_core.toolpath_simulator import (
    simulate_toolpath, SimulationResult, generate_test_toolpath,
    ToolPathPoint, BoundingBox, CollisionZone
)
from cnc_core.process_planner import plan_process, Feature, ProcessPlan
from cnc_core.database import init_database

results = []

def test(name, func):
    try:
        func()
        results.append((name, "✅ PASS"))
        print(f"  ✅ {name}")
    except Exception as e:
        results.append((name, f"❌ FAIL: {e}"))
        print(f"  ❌ {name}: {e}")

print("=" * 60)
print("🧪 UG AI 自动编程插件 - 测试套件")
print("=" * 60)

# ===== 1. 切削参数测试 =====
print("\n📊 1. 切削参数计算器")

def test_materials_list():
    mats = get_all_materials()
    assert len(mats) == 14, f"期望14种材料，实际{len(mats)}种"
test("材料列表 (14种)", test_materials_list)

def test_tools_list():
    tools = get_all_tool_types()
    assert len(tools) == 10, f"期望10种刀具，实际{len(tools)}种"
test("刀具类型列表 (10种)", test_tools_list)

def test_steel_45_rough():
    p = calculate_params(Material.STEEL_45, ToolType.END_MILL, 10, "roughing")
    assert p.spindle_speed > 0, "主轴转速必须 > 0"
    assert p.feed_rate > 0, "进给速度必须 > 0"
    assert p.axial_depth > 0, "轴向切深必须 > 0"
    assert p.radial_depth > 0, "径向切深必须 > 0"
test("45号钢粗加工立铣 (D10)", test_steel_45_rough)

def test_tc4_rough():
    p = calculate_params(Material.TC4, ToolType.END_MILL, 8, "roughing")
    # 钛合金切削速度应该低
    assert p.cutting_speed < 50, f"钛合金Vc应该<50, 实际{p.cutting_speed}"
test("TC4钛合金粗加工立铣 (D8)", test_tc4_rough)

def test_al6061_rough():
    p = calculate_params(Material.AL6061, ToolType.FACE_MILL, 20, "roughing")
    # 铝合金切削速度应该高
    assert p.cutting_speed > 200, f"铝合金Vc应该>200, 实际{p.cutting_speed}"
test("AL6061粗加工面铣 (D20)", test_al6061_rough)

def test_finishing_vs_roughing():
    p1 = calculate_params(Material.STEEL_45, ToolType.END_MILL, 10, "roughing")
    p2 = calculate_params(Material.STEEL_45, ToolType.END_MILL, 10, "finishing")
    # 精加工参数应该更保守
    assert p2.spindle_speed < p1.spindle_speed, "精加工转速应该更低"
    assert p2.axial_depth < p1.axial_depth, "精加工切深应该更小"
test("粗加工 vs 精加工对比", test_finishing_vs_roughing)

def test_drill_params():
    p = calculate_params(Material.CR12MOV, ToolType.DRILL, 5, "roughing")
    assert p.tool_type == "钻头"
    assert p.spindle_speed > 0
test("Cr12MoV钻头 (D5)", test_drill_params)

def test_turning_params():
    p = calculate_params(Material.Q235, ToolType.TURNING_TOOL, 12, "roughing")
    assert p.radial_depth > p.axial_depth * 0.5, "车刀径向切深应该较大"
test("Q235车刀 (D12)", test_turning_params)

def test_all_materials_endmill():
    for mat in Material:
        p = calculate_params(mat, ToolType.END_MILL, 10, "roughing")
        assert p.spindle_speed > 0
        assert p.feed_rate > 0
test("所有材料 x 立铣刀", test_all_materials_endmill)

def test_all_tools_steel45():
    for tool in ToolType:
        p = calculate_params(Material.STEEL_45, tool, 10, "roughing")
        assert p.spindle_speed > 0
        assert p.feed_rate > 0
test("45号钢 x 所有刀具", test_all_tools_steel45)

# ===== 2. G代码生成测试 =====
print("\n📝 2. G代码生成器")

def test_face_milling_gcode():
    tool = Tool("面铣刀", 20, tool_number=10)
    wp = Workpiece("TestPart", 100, 80, 15, 0, 0, 0)
    prog = generate_gcode(
        Operation.FACE_MILLING, tool, wp,
        {"spindle_speed": 4000, "feed_rate": 2000, "axial_depth": 2, "radial_depth": 5}
    )
    gcode = prog.to_string()
    assert "O" in gcode, "应该有程序号"
    assert "G1" in gcode, "应该有G1指令"
    assert "M3" in gcode, "应该有主轴启动"
    assert "M5" in gcode, "应该有主轴停止"
test("面铣G代码", test_face_milling_gcode)

def test_drill_gcode():
    tool = Tool("钻头", 6, tool_number=20)
    wp = Workpiece("TestPart", 100, 80, 15, 0, 0, 0)
    holes = [{"x": 20, "y": 20, "depth": 10}]
    prog = generate_gcode(
        Operation.DRILLING, tool, wp,
        {"spindle_speed": 2000, "feed_rate": 200, "axial_depth": 5, "radial_depth": 0},
        holes=holes
    )
    gcode = prog.to_string()
    assert "G81" in gcode or "G83" in gcode, "应该有钻孔循环"
test("钻孔G代码", test_drill_gcode)

def test_peripheral_milling_gcode():
    tool = Tool("立铣刀", 10, tool_number=15)
    wp = Workpiece("TestPart", 100, 80, 15, 0, 0, 0)
    prog = generate_gcode(
        Operation.PERIPHERAL_MILLING, tool, wp,
        {"spindle_speed": 3000, "feed_rate": 1500, "axial_depth": 2, "radial_depth": 3}
    )
    gcode = prog.to_string()
    assert "G1" in gcode
    assert "M3" in gcode
test("轮廓铣G代码", test_peripheral_milling_gcode)

def test_pocket_milling_gcode():
    tool = Tool("立铣刀", 12, tool_number=16)
    wp = Workpiece("TestPart", 100, 80, 15, 0, 0, 0)
    prog = generate_gcode(
        Operation.POCKET_MILLING, tool, wp,
        {"spindle_speed": 3000, "feed_rate": 1500, "axial_depth": 3, "radial_depth": 4}
    )
    gcode = prog.to_string()
    assert "G1" in gcode
test("型腔铣G代码", test_pocket_milling_gcode)

def test_tapping_gcode():
    tool = Tool("丝锥", 8, tool_number=30)
    wp = Workpiece("TestPart", 100, 80, 15, 0, 0, 0)
    holes = [{"x": 30, "y": 30, "depth": 10}]
    prog = generate_gcode(
        Operation.TAPPING, tool, wp,
        {"spindle_speed": 500, "feed_rate": 50, "axial_depth": 2, "radial_depth": 0},
        holes=holes
    )
    gcode = prog.to_string()
    assert "G84" in gcode, "应该有攻丝循环"
test("攻丝G代码", test_tapping_gcode)

def test_boring_gcode():
    tool = Tool("镗刀", 20, tool_number=35)
    wp = Workpiece("TestPart", 100, 80, 15, 0, 0, 0)
    holes = [{"x": 50, "y": 50, "depth": 15}]
    prog = generate_gcode(
        Operation.BORING, tool, wp,
        {"spindle_speed": 1000, "feed_rate": 100, "axial_depth": 3, "radial_depth": 0},
        holes=holes
    )
    gcode = prog.to_string()
    assert "G76" in gcode, "应该有精镗循环"
test("镗孔G代码", test_boring_gcode)

def test_turning_gcode():
    tool = Tool("车刀", 12, tool_number=40)
    wp = Workpiece("TestPart", 50, 50, 60, 0, 0, 0)
    prog = generate_gcode(
        Operation.TURNING, tool, wp,
        {"spindle_speed": 2000, "feed_rate": 200, "axial_depth": 2, "radial_depth": 5}
    )
    gcode = prog.to_string()
    assert "G1" in gcode
test("车削G代码", test_turning_gcode)

def test_deep_drill_gcode():
    tool = Tool("钻头", 8, tool_number=22)
    wp = Workpiece("TestPart", 100, 80, 30, 0, 0, 0)
    holes = [{"x": 50, "y": 50, "depth": 40}]
    prog = generate_gcode(
        Operation.DEEP_DRILL, tool, wp,
        {"spindle_speed": 800, "feed_rate": 80, "axial_depth": 5, "radial_depth": 0},
        holes=holes
    )
    gcode = prog.to_string()
    assert "G83" in gcode, "深孔钻应该用G83"
test("深孔钻G代码", test_deep_drill_gcode)

def test_gcode_program_number():
    prog = GCodeProgram(title="Test")
    assert "O1000" in prog.to_string()
test("程序号格式", test_gcode_program_number)

# ===== 3. 后处理器测试 =====
print("\n🔧 3. 后处理器")

def test_fanuc_post():
    gcode = "M3 S3000\nM5\nG1 X10 Y10 F1000"
    result = apply_postproc(gcode, PostProcessor.FANUC)
    assert "M3" in result
    assert "S3000" in result
test("FANUC后处理", test_fanuc_post)

def test_siemens_post():
    gcode = "M3 S3000"
    result = apply_postproc(gcode, PostProcessor.SIEMENS)
    assert "M3" in result
test("SIEMENS后处理", test_siemens_post)

def test_gsk_post():
    gcode = "M3 S3000"
    result = apply_postproc(gcode, PostProcessor.GSK)
    assert "M3" in result
test("广数后处理", test_gsk_post)

def test_post_header():
    header = generate_post_header(PostProcessor.FANUC, "Test")
    assert "FANUC" in header
test("后处理头部", test_post_header)

# ===== 4. 刀路仿真测试 =====
print("\n🔬 4. 刀路仿真与碰撞检测")

def test_sim_basic():
    points = generate_test_toolpath()
    wp = BoundingBox(5, 5, 0, 25, 25, 10)
    zones = [CollisionZone(BoundingBox(0,0,-1,8,8,10), "CLAMP", "夹具")]
    result = simulate_toolpath(points, wp, zones, 10, 80)
    assert result.total_points == len(points)
    assert result.cutting_points >= 0
    assert result.total_time >= 0
test("基础仿真", test_sim_basic)

def test_sim_with_collision():
    points = generate_test_toolpath()
    wp = BoundingBox(5, 5, 0, 25, 25, 10)
    # 碰撞区域在刀路上
    zones = [CollisionZone(BoundingBox(12, 8, -1, 18, 12, 10), "CLAMP", "夹具A")]
    result = simulate_toolpath(points, wp, zones, 10, 80)
    assert len(result.collisions) > 0, "应该检测到碰撞"
test("碰撞检测", test_sim_with_collision)

def test_sim_air_cut():
    points = generate_test_toolpath()
    wp = BoundingBox(20, 20, 0, 30, 30, 10)  # 工件很小
    zones = []
    result = simulate_toolpath(points, wp, zones, 10, 80)
    assert result.air_points > 0, "应该有空刀"
    assert result.warnings, "应该有空刀警告"
test("空刀检测", test_sim_air_cut)

def test_sim_tool_length():
    points = [ToolPathPoint(10, 10, -90, 500, 1000, 1, "G1")]
    wp = BoundingBox(0, 0, 0, 20, 20, 10)
    zones = []
    result = simulate_toolpath(points, wp, zones, 10, 80)
    critical = [c for c in result.collisions if c.severity == "CRITICAL"]
    assert len(critical) > 0, "刀具过长应该报警"
test("刀具长度检查", test_sim_tool_length)

# ===== 5. 工艺编排测试 =====
print("\n📋 5. 工艺路线编排")

def test_plan_basic():
    features = [
        Feature("FACE", "基准面", diameter=80, length=100, width=80),
        Feature("HOLE", "安装孔", diameter=8, depth=20, hole_count=4),
    ]
    plan = plan_process(features, "45号钢")
    assert len(plan.steps) > 0, "应该有工序"
    assert plan.total_time > 0, "总时间应该 > 0"
test("基础工艺编排", test_plan_basic)

def test_plan_sequence():
    features = [
        Feature("FACE", "基准面", diameter=80, length=100, width=80),
        Feature("POCKET", "型腔A", length=50, width=40, height=15, diameter=12),
        Feature("HOLE", "安装孔", diameter=8, depth=20, hole_count=4),
        Feature("THREAD", "螺纹孔", thread_diameter=10, thread_pitch=1.5, hole_count=2),
    ]
    plan = plan_process(features, "45号钢")
    # 先面后孔
    face_idx = next((i for i, s in enumerate(plan.steps) if s.type.value == "端面加工"), -1)
    hole_idx = next((i for i, s in enumerate(plan.steps) if s.type.value == "钻孔"), -1)
    assert face_idx < hole_idx, "应该先面后孔"
test("工序顺序 (先面后孔)", test_plan_sequence)

def test_plan_total_time():
    features = [
        Feature("FACE", "基准面", diameter=80, length=100, width=80),
    ]
    plan = plan_process(features, "45号钢")
    calculated = sum(s.estimated_time for s in plan.steps)
    assert abs(plan.total_time - calculated) < 0.01, f"总时间不匹配: {plan.total_time} vs {calculated}"
test("总时间计算", test_plan_total_time)

def test_plan_to_string():
    features = [Feature("FACE", "基准面", diameter=80, length=100, width=80)]
    plan = plan_process(features, "45号钢")
    output = plan.to_string()
    assert "基准面" in output
    assert "端面加工" in output
test("工艺方案输出", test_plan_to_string)

# ===== 6. 数据库测试 =====
print("\n💾 6. 数据库")

def test_db_init():
    db_path = init_database()
    assert db_path.exists(), "数据库文件应该存在"
test("数据库初始化", test_db_init)

def test_save_plan():
    plan_id = save_process_plan("TestPart", "45号钢", [{"type": "立铣刀", "d": 10}],
                                 {"spindle_speed": 4000}, "O1000\nM3\nM5")
    assert plan_id > 0
test("保存工艺方案", test_save_plan)

def test_get_plan():
    init_database()
    plan_id = save_process_plan("GetTest", "Q235", [], {}, "O1001\nM3")
    plan = get_all_plans()
    assert len(plan) > 0, "应该有保存的方案"
test("查询工艺方案", test_get_plan)

# ===== 测试结果汇总 =====
print("\n" + "=" * 60)
print("📊 测试结果汇总")
print("=" * 60)

passed = sum(1 for _, r in results if "✅" in r)
failed = sum(1 for _, r in results if "❌" in r)
total = len(results)

for name, result in results:
    print(f"  {result} {name}")

print(f"\n总计: {total} | 通过: {passed} | 失败: {failed}")
if failed == 0:
    print("🎉 所有测试通过!")
else:
    print(f"⚠️  有 {failed} 个测试失败")
