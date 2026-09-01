# TCO Generator 使用说明

> **迁移状态（2026-07-19）**：本目录的 Generator 对新的通用 KYM/TCO authoring 已标记为 deprecated。新的通用入口是独立 `kym-tco` 项目及全局 `build-kym`、`build-tco-coverage` Skill。当前 Semx RCP/SAG model、Coverage model 和既有输出仍由本 Generator 兼容维护；在所有 Semx 消费面完成迁移、严格 Coverage 与完整 verify parity 再次通过前，不得删除本文件或改变其现有 authority boundary。

本文说明 `Dashboard/tools/visualization/` 下的 TCO Generator 与 TCO model 如何工作、如何使用、何时更新，以及它们能保证什么、不能保证什么。

## 1. 定位

TCO 是 `Testing Coverage Outline`，在这里表示围绕 KYM `Business Rules` 分支整理出来的业务功能覆盖树。

TCO 的基本对象是单功能 `M`。一个 `M` 必须是真实可实现、可讨论、可跟踪、可测试的功能模块或功能节点。每个 `M` 使用 TSP 建模：

- `Topic`：一句话说明这个功能是什么。
- `Scope`：从实现角度看，为了实现这个功能，需要覆盖哪些组成部分、接口、规则、数据对象或行为面。
- `Purpose`：说明这个功能为什么存在；如果没有它，会造成什么缺口。

TCO 不是 Dashboard truth source，也不是 KB canonical truth。它是从 KYM 文档和人工语义整理得到的可浏览读模型，用于帮助理解和检查 Business Rules 的功能覆盖情况。

## 2. 文件

当前目录中的核心文件：

```text
Dashboard/tools/visualization/tco_generator.py
Dashboard/tools/visualization/kym_business_rules_tco_model.json
Dashboard/tools/visualization/kym_business_rules_tco_coverage_model.json
Dashboard/tools/visualization/business_rules_to_tco_model_prompt.md
Dashboard/tools/visualization/tco_coverage_model_prompt.md
Dashboard/tools/visualization/kym_business_rules_tco_provider_trial_summary.json
Dashboard/tools/visualization/kym_business_rules_tco_validation_summary.json
Dashboard/tools/visualization/README.md
```

默认输入：

```text
semx-kb/bm-doc/KYM/4. RCP+SAG KYM.md
```

默认输出：

```text
.semx/latest/visualization/kym_business_rules_tco.html
.semx/latest/visualization/kym_business_rules_tco.json
.semx/latest/visualization/kym_business_rules_tco_manifest.json
.semx/latest/visualization/kym_business_rules_tco_coverage.json
.semx/latest/visualization/kym_business_rules_tco_coverage_manifest.json
```

## 3. 一键生成

在 repo 根目录运行：

```bash
python3 Dashboard/tools/visualization/tco_generator.py
```

如果需要显式指定输入、模型或输出目录：

```bash
python3 Dashboard/tools/visualization/tco_generator.py \
  --source "semx-kb/bm-doc/KYM/4. RCP+SAG KYM.md" \
  --model Dashboard/tools/visualization/kym_business_rules_tco_model.json \
  --coverage-model Dashboard/tools/visualization/kym_business_rules_tco_coverage_model.json \
  --output-dir .semx/latest/visualization \
  --section "Business Rules"
```

运行成功后，终端会输出 manifest 摘要。重点看这些字段：

- `node_count`：TCO 中的 M 数量。
- `ref_info_node_count`：有 Ref Info 的 M 数量。
- `empty_ref_info_node_count`：Ref Info 为空的 M 数量。
- `missing_ref_count`：模型中 `ref_titles` 未匹配回原文的数量。

理想状态下，`missing_ref_count` 应为 `0`。

Coverage 默认只做 repo inventory，不运行测试。如果需要实际运行 coverage model 中声明的 maintained gate：

```bash
python3 Dashboard/tools/visualization/tco_generator.py --verify
```

只验证某一个或几个 TCO node 引用的 gate：

```bash
python3 Dashboard/tools/visualization/tco_generator.py --verify --verify-node runtime_state_schema
python3 Dashboard/tools/visualization/tco_generator.py --verify --verify-node runtime_state_schema --verify-node sag_observation_graph
```

更严格地检查 coverage model：

```bash
python3 Dashboard/tools/visualization/tco_generator.py --strict-coverage
```

## 4. 生成机制

Generator 的机制是确定性的，但 TCO model 的语义内容不是自动推理出来的。

生成流程：

1. 读取 `--source` 指向的 KYM Markdown。
2. 找到 `--section` 指定的 bullet section，默认是 `Business Rules`。
3. 将该 section 的 bullet 解析成原文树。
4. 读取 `kym_business_rules_tco_model.json`。
5. 按 model 中的 `root` 和 `children` 建立 TCO 功能树。
6. 读取 `kym_business_rules_tco_coverage_model.json`，把人工确认的 repo evidence 叠加到对应 M。
7. 每个 `capability` / `policy` 必须有显式 coverage 记录；缺失时 fail closed。`group` 可以不写直接记录。
8. capability/policy 按各自 node target 计算 Coverage Gap；schema/policy/candidate 节点不再被全局强迫达到 Runtime。
9. group 只显示 `covered/partial/not_started` 聚合状态，不参与 capability/policy Coverage 数量统计。
10. 分别计算 selected runway、broader RCP 与 SAG future target profiles；一个 profile 达标不会关闭其他 profile。
11. 对每个 M 渲染：
   - `Topic`
   - `Ref Info`
   - `Scope`
   - `Purpose`
   - `Coverage`
   - `Sub M`
12. 根据每个 M 的 `ref_titles` 去原文 bullet 树中匹配补充信息，生成 Ref Info。
13. 输出 HTML、TCO JSON、Coverage JSON 和 manifest。

重要边界：

- Generator 负责结构渲染和基础校验。
- Generator 不负责自动判断哪些原文节点应该成为 M。
- Generator 不负责证明 TSP 的语义正确性。
- TSP 的语义质量来自 model 的人工/AI 协作整理和 review。
- Coverage model 只记录当前人工确认的 repo evidence；未确认项必须保持 `unknown` 或 `candidate_evidence`。
- Coverage 输出是派生证据统计，不是 Runtime Kernel / RCP / SAG 完成声明。

## 5. TCO model 结构

每个节点形如：

```json
{
  "id": "runtime_state_schema",
  "node_kind": "capability",
  "title": "State Schema",
  "topic": "定义一次 runtime run 的当前执行协调状态应如何表示。",
  "scope": [
    "state vocabulary",
    "state category table",
    "state record schema",
    "state evidence fields"
  ],
  "purpose": "让系统能明确保存和读取 run 当前处于哪个执行协调状态，并知道该状态携带哪些证据和边界信息。",
  "ref_titles": [
    "当前 Repo 的 runtime state contract 使用：INIT、INGESTED、..."
  ],
  "ref_depth": 1,
  "children": []
}
```

字段含义：

- `id`：稳定节点 ID，用于父子引用。
- `node_kind`：`group`、`capability` 或 `policy`。`group` 只组织功能域；`capability` 是可独立实现/测试的能力；`policy` 是可独立维护/验证的规则。
- `title`：显示名称。
- `topic`：TSP 的 Topic。
- `scope`：TSP 的 Scope。
- `purpose`：TSP 的 Purpose。
- `ref_titles`：可选。用于从 KYM 原文匹配 Ref Info。
- `ref_depth`：可选。匹配到原文 bullet 后向下保留几层文本。
- `children`：子 M 的 `id` 列表。

## 6. Scope、Sub M 和 Ref Info 的关系

`Scope` 不要求和 `Sub M` 一一对应。

`Scope` 表示实现该 M 时需要覆盖的组成部分。一部分 Scope 项可能已经足够重要、复杂或可跟踪，因此被提升为子 M，并在 `Sub M` 下展开自己的 TSP。另一部分 Scope 项可能只是横切关注点、显示要求、约束、格式要求或局部实现要求，不一定需要升级成 M。

判断规则：

- 如果某个 Scope 项需要独立设计、实现、测试、验收或长期跟踪，应提升为子 M。
- 如果某个 Scope 项只是父 M 的一项实现关注点，可以保留在 Scope 中，不必建子 M。
- 如果 Scope 项没有子 M 展开，但读者可能误解它，应给出简短补充说明。
- 不要为了让 Scope 和 Sub M 数量对齐而硬造 M。

例子：

`Runtime Control Surface` 的 Scope 可以包含：

```text
inspect state CLI
update state CLI
trace inspect CLI
trace verify CLI
graph inspect
operator-facing rejection/error display
```

前五项可以作为 CLI 类子 M 展开。`operator-facing rejection/error display` 可以暂时不是独立 M，而是横切显示要求：所有控制入口在遇到 rejection、error、blocked、review-required 时，都应输出一致的原因、证据引用、状态是否变化、trace/report link 和下一步提示。

当前 model 的 `scope` 字段是字符串列表。如果某个 Scope 项需要补充解释，可以先用简短文字写在该 Scope 项内；如果解释变长，应优先考虑后续扩展 model schema，例如增加结构化 `scope_notes`，而不是把长说明塞进 Scope。

## 7. Coverage 统计模型

Coverage 是独立叠加层，不写入 TCO model 的 TSP 字段。

Coverage model 文件：

```text
Dashboard/tools/visualization/kym_business_rules_tco_coverage_model.json
```

每条记录绑定一个 TCO node：

```json
{
  "tco_node_id": "state_schema",
  "coverage_state": "schema_validator",
  "claim_ceiling": "S-286 proves maintained state vocabulary ... only.",
  "evidence": [
    {"kind": "code", "ref": "semx/runners/runtime_state_contract.py"},
    {"kind": "command", "gate": "semx_runtime_state_contract_acceptance"}
  ],
  "scope_coverage": [
    {"scope": "state vocabulary", "coverage_state": "schema_validator", "notes": "Covered by maintained transition/state contract constants and tests."}
  ],
  "missing_scope_items": [],
  "notes": []
}
```

`coverage_state` 取值：

- `unknown`：还没有人工确认 repo evidence。
- `not_started`：确认没有开始或没有可用 repo evidence。
- `design_only`：只有设计、合同、Dashboard/KB 文档或计划证据。
- `schema_validator`：有 schema、validator、fixture 或直接 validator gate 证据。
- `test_bound`：有 maintained gate / deterministic test / audit evidence，但仍是测试边界证明。
- `bounded_runtime`：有真实但有界的 runtime 行为证据，例如 selected path、single boundary、test store、advisory runner。
- `integrated_runtime`：集成 runtime 行为证据。当前 model 应非常谨慎使用；不能用 support slice 或 validator gate 冒充。

父 M 不应手写“完成”。Generator 会为所有节点保守计算 effective coverage：

- `group` 的 direct state 只能是 `unknown/not_started`，否则校验失败。
- `capability` / `policy` 只要声明非 `unknown/not_started` 状态，就必须逐项覆盖 TCO model 的全部 Scope。
- effective coverage 取所有声明的 Sub M 与 Scope 中最低覆盖层级；任何 `unknown/not_started` 子 M 或 Scope 都会把整体保持在相应低层级。
- direct coverage 只保留为证据元数据，不参与抬高 effective coverage。
- Coverage 面板显示 `Scope completeness` 和 `Sub M completeness`，方便人类区分“有局部证据”与“声明范围完整覆盖”。
- capability 默认目标为 `bounded_runtime`，policy 默认目标为 `test_bound`；特例必须写入 coverage model 的 `target_state_overrides`。
- `Coverage Gap` 表示低于本节点目标，不再等同“低于 Runtime”。
- `unknown` 是尚未确认；`not_started` 是已确认没有 maintained evidence。HTML 分开显示二者。
- group 只显示聚合状态，不把最弱子项的 state 标签冒充自身实现状态。
- TCO model 的 `target_profiles` 用于区分当前 selected test runway、broader RCP 与 SAG future target。

证据类型：

- `code`、`schema`、`test`、`bdd`、`dashboard`、`kb`：`ref` 必须指向 repo 中存在的路径。
- `command`：`gate` 必须存在于 `tests/contract/run_maintained_validation.py --list`。
- `candidate_evidence`：只表示疑似相关，不能计入 covered，也不能支撑 `coverage_state` 抬升。

默认 inventory 只检查路径和 gate 注册，不运行 gate。此时 HTML 使用 `Declared evidence`，command 显示“未运行”，不得称为 confirmed/verified。`--verify` 会运行 coverage model 中声明的 maintained gate，并把 `pass/fail/timeout` 写入 coverage JSON；只有 pass 才计入 `Verified gates`。`--verify-node` 可以限制只运行指定 TCO node 引用的 gate。

## 8. Ref Info 的规则

Ref Info 不是每个 M 的必填项。大部分情况下，Ref Info 可以为空。

Ref Info 只用于保留没有进入 Scope 的补充信息，特别是：

- 原文中的解释、例子、背景说明。
- 当前实现状态。
- repo 现状。
- claim ceiling。
- authority boundary。
- 不应进入 TSP 的非功能实现信息。

不要把已经进入 Scope 的条目再完整复制到 Ref Info。否则 HTML 中会出现 Scope 与 Ref Info 大量重复，降低可读性。

## 9. model 什么时候生成和更新

`kym_business_rules_tco_model.json` 是语义中间层，不是 generator 自动生成的临时文件。

它通常在以下场景中创建或更新：

- 初次从 KYM `Business Rules` 建立 TCO 功能树。
- KYM 原文新增、删除或重写 Business Rules。
- 项目推进后，对某个功能的理解变细，需要把 Scope 项提升为新的 M。
- 原先作为 M 的节点后来发现只是说明性内容，需要降级为 Scope 项或 Ref Info。
- 用户 review 后指出 TSP 不真实、Scope 机械、Purpose 空泛或 Ref Info 重复。
- repo 实现暴露出新的可实现模块、接口、schema、validator、store、CLI、runtime behavior 或 governance rule。
- 某个功能项需要独立验收、独立测试或长期跟踪。

推荐更新流程：

1. 对照 KYM `Business Rules` 原文。
2. 判断哪些原文节点是真实可实现 M。
3. 为每个 M 写真实 TSP。
4. 将没有进入 Scope 的原文补充放入 `ref_titles`。
5. 检查 Scope 中哪些项已经有子 M 展开，哪些只是实现关注点。
6. 运行 generator。
7. 检查 manifest 和 HTML。
8. 人工 review 结构是否符合当前理解。

## 10. 正确性保证

Generator 可以保证的是结构和基础规则，不是完整语义真理。

当前脚本会检查：

- model schema 必须是 `semx.visualization.tco_model.v1`。
- 每个 node 必须有合法 `node_kind`，且 ID 不得重复。
- 每个被引用的 child id 必须存在。
- 每个 M 必须有非空 `Topic`、`Scope`、`Purpose`。
- TSP 中不能出现机械 fallback 文案，例如：
  - `作为父节点范围内的聚合节点`
  - `补足该层级的可查看内容`
  - `未显式给出 Scope`
  - `包含子节点：`
- TSP 中不能出现应放入 Ref Info 的状态/claim 类内容，例如：
  - `当前 Repo`
  - `当前已经`
  - `尚无`
  - `不代表`
  - `claim ceiling`
  - `不能冒充`
  - `不能据此断言`
- coverage model schema 必须是 `semx.visualization.tco_coverage_model.v1`。
- coverage model 中的 `tco_node_id` 必须存在于当前 TCO 树。
- coverage model 中的 `coverage_state` 必须属于固定枚举。
- coverage model 必须覆盖每个 `capability` / `policy`；`group` 可以省略并完全派生。
- 非空 Coverage 不得遗漏、重复或引用 model 之外的 Scope。
- `group` 不得配置直接完成状态。
- `code/schema/test/bdd/dashboard/kb` evidence 的 `ref` 必须是 repo 中存在的路径。
- `command` evidence 的 `gate` 必须存在于 `tests/contract/run_maintained_validation.py --list`。
- `candidate_evidence` 不计入 confirmed coverage，不能单独支撑已覆盖状态。

Generator 会在 manifest 中报告：

- `missing_ref_count`
- `missing_refs`
- `ref_info_node_count`
- `empty_ref_info_node_count`
- `coverage_state_counts`
- `direct_coverage_state_counts`
- `node_kind_counts`
- `coverage_state_counts_by_kind`
- `warning_count`
- `verified_gate_count`
- `failed_verified_gates`

这些检查能发现一部分结构错误和明显的建模污染，但不能证明：

- M 划分一定完整。
- TSP 一定语义正确。
- Scope 一定覆盖了所有实现面。
- Ref Info 一定保留了所有重要原文补充。
- 当前 TCO 已经可以作为 implementation approval。
- Coverage state 等于 Runtime Kernel、RCP、SAG 或 production 已完成。
- `schema_validator` 或 `test_bound` 等于完整 runtime 行为。
- `candidate_evidence` 等于已确认实现证据。

## 11. 人工 Review 清单

每次大改 TCO model 后，应至少检查：

- 每个 M 是否是真实可实现功能点，而不是说明性标题。
- 每个 Topic 是否能一句话说明功能含义。
- 每个 Scope 是否从实现角度列出组成部分，而不是复制原文。
- 每个 Purpose 是否说明功能存在价值，而不是空泛描述。
- Scope 中没有当前实现状态、repo 现状、claim ceiling 或 authority boundary。
- Ref Info 没有重复复制 Scope。
- Ref Info 为空的节点是否确实没有额外补充信息。
- Scope 项没有子 M 展开时，是否需要补充说明。
- 子 M 是否确实属于父 M 的 Scope。
- KYM 原文中重要 Business Rules 是否已被覆盖，或有明确不纳入原因。
- Coverage state 是否低于或等于 claim ceiling。
- `bounded_runtime` 是否明确说明 bounded 边界。
- 父 M 的 Coverage 是否来自 rollup，而不是人工手写完成。
- 每个 capability/policy 的全部 Scope 是否逐项有 Coverage，完整度是否为 `total/total`。
- group 是否仅组织功能域，并且其 Coverage 没有掩盖 unknown/not_started 子项。
- `candidate_evidence` 是否只作为线索，不参与覆盖判定。
- Coverage 缺口是否保留为 `unknown` 或 `missing_scope_items`，而不是通过标题猜测补齐。

## 12. 快速校验命令

生成：

```bash
python3 Dashboard/tools/visualization/tco_generator.py
```

检查 Python 语法，不写 pycache：

```bash
python3 - <<'PY'
from pathlib import Path
for path in [Path("Dashboard/tools/visualization/tco_generator.py")]:
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
    print("compiled", path)
PY
```

检查 manifest：

```bash
python3 - <<'PY'
import json
from pathlib import Path
manifest = json.loads(Path(".semx/latest/visualization/kym_business_rules_tco_manifest.json").read_text())
print(json.dumps({
    "node_count": manifest["node_count"],
    "ref_info_node_count": manifest["ref_info_node_count"],
    "empty_ref_info_node_count": manifest["empty_ref_info_node_count"],
    "missing_ref_count": manifest["missing_ref_count"],
}, ensure_ascii=False, indent=2))
PY
```

检查 Coverage manifest：

```bash
python3 - <<'PY'
import json
from pathlib import Path
manifest = json.loads(Path(".semx/latest/visualization/kym_business_rules_tco_coverage_manifest.json").read_text())
print(json.dumps({
    "node_count": manifest["node_count"],
    "coverage_state_counts": manifest["coverage_state_counts"],
    "direct_coverage_state_counts": manifest["direct_coverage_state_counts"],
    "warning_count": manifest["warning_count"],
    "verified_gate_count": manifest["verified_gate_count"],
    "failed_verified_gates": manifest["failed_verified_gates"],
}, ensure_ascii=False, indent=2))
PY
```

低成本试跑一个节点的 maintained gate：

```bash
python3 Dashboard/tools/visualization/tco_generator.py --verify --verify-node runtime_state_schema
```

检查 TSP 和 Ref Info 分布：

```bash
python3 - <<'PY'
import json
from pathlib import Path
data = json.loads(Path(".semx/latest/visualization/kym_business_rules_tco.json").read_text())

def walk(node):
    yield node
    for child in node.get("children", []):
        yield from walk(child)

nodes = list(walk(data))
missing_tsp = [n["id"] for n in nodes if not n.get("topic") or not n.get("scope") or not n.get("purpose")]
ref_nodes = [n["id"] for n in nodes if n.get("ref_info")]
print("nodes", len(nodes))
print("missing_tsp", missing_tsp)
print("ref_nodes", len(ref_nodes), ref_nodes)
print("empty_ref_nodes", len(nodes) - len(ref_nodes))
PY
```

## 13. 权威边界

TCO 输出是 read model。

- KYM Markdown 是本视图的原文输入。
- `kym_business_rules_tco_model.json` 是当前人工整理的语义模型。
- HTML/JSON 是从 model 派生的浏览视图。
- `semx-kb/` 仍然是 canonical truth。
- `Dashboard/` 仍然是 execution memory。

不要把 TCO HTML 的存在理解成某个功能已经实现、验证通过、进入生产，或已经获得 KB truth authority。
