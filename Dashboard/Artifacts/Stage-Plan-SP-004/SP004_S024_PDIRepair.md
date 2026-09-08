# S-024 PDI 阻断修复

## 关键结论中文展开

本 PDI 修复了 S-024 Validation 发现的两个可复现门禁缺陷，并生成了同一份 S-023 冻结 case identity 绑定的 RED/GREEN 证据。`pass` 只表示当前本地门禁和测试范围通过；不表示 rights、release、远端状态或 SP-004 完成。

## 阻断逐项处置

| blocker | disposition | root cause | fix | verification | recurrence prevention | residual risk | status |
|---|---|---|---|---|---|---|---|
| Locator gate 未强制 typed disposition，且未覆盖 `Dashboard/Archives/`、`Dashboard/Agent_Logs/`、`Dashboard/Artifacts/` | 修复并保留在当前 S-024 范围 | 旧 gate 只查两个目录的字符串，未建立 locator 类型、解析结果和完整 private surface inventory | `Dashboard/tools/doctor.py` 新增 `resolve_typed_locator`、`inventory_public_locators`；in-package 必须可解析，external/private 必须显式 typed；三类 Dashboard surface 默认 private 且不得进入 public allowlist | trusted RED `SP004-RED-03`；独立 GREEN `SP004-GREEN-07/10`；repository doctor 与 32 tests 通过 | 每次 doctor 都重建 inventory；新增负 fixture 拒绝未声明相对 private locator；readable card 固化该行为 | 未覆盖未列入当前 manifest 的外部 provider 权利事实；仍需后续 independent Validation 复核最终 diff | repaired_and_locally_verified |
| `semx` deny-token presence/classification 可被删除或误分类而通过 | 修复并保留在当前 S-024 范围 | 旧 gate 只搜索主动依赖词，没有验证 deny token 仍存在于 policy 和 control context | `check_public_residue` 要求 `semx` 出现在 deny-token policy、allowlisted control context 和完整 forbidden classes；主动词按 `product_cli/product_kb/product_audio` 分类并 fail-closed | trusted RED `SP004-RED-05`；独立 GREEN `SP004-GREEN-09`；正负 fixture 与 doctor 通过 | 维护 positive control witness、negative missing-token fixture 和 active-class fixture；readable card 说明控制语义 | 仅证明当前 allowlisted candidate 的静态隔离，不证明任意未来候选或运行时依赖没有新增 | repaired_and_locally_verified |
| durable trusted RED/GREEN evidence 缺失 | 修复并生成证据，不改变冻结合同 | Validation review 识别到普通 unittest 不能替代 ERBE execution evidence | 新增 [ERBE RED/GREEN evidence](SP004_S024_ERBE_RED_GREEN.json)，绑定 S-023 Contract/Cases hash 与 case identity，明确 `contract_verdict`、`execution_verdict` 和环境 error 分离 | 3 个 trusted RED、3 个 independent GREEN；环境错误数组为空；测试数 32 | 后续修复必须复用冻结 case identity，且任何环境/fixture/path 错误只能记录为 `error` | 本 artifact 只覆盖 GAP-MH-07/09/10，不关闭其他 S-024 或后续 Session | evidence_created |

## 验证交接包

- Read Manifest：S-024 PDI repair card、S-024 Validation Review/State Snapshot、S-023 frozen Contract/Cases、doctor、public manifest、三组测试和 readable card。
- 写入面仅为 card 声明的 `Dashboard/tools/doctor.py`、测试、readable card、本 PDI 和 ERBE artifact；未修改 S-023 Contract/Cases/expected/claim ceiling。
- 运行：`python3 -m unittest discover -s tests -p 'test_*.py'`（32/32）；`python3 Dashboard/tools/doctor.py --repo .`（pass）；`git diff --check`（pass）。
- Closeout language verdict：`not applicable for this repair artifact`（本文件不是 Session closeout；最终 closeout 仍需独立 Validation 和语言门禁）。

## 明确非目标与剩余风险

本次不执行远端访问、rights confirmation、release、Git handoff 或 production readiness 判断；不关闭 S-025/S-026/S-027/S-028/S-029。S-024 仍需独立 Validation 读取本 artifact、最终 diff 和 Dashboard 状态后给出唯一 verdict。

## KB/Dashboard 复核

本次没有批准新的稳定 canonical policy，因此不更新 `kb/`；实现和证据属于当前 Dashboard execution memory。若后续批准 typed locator 或 deny-token 规则成为稳定公共政策，再做最小 Contract Delta Scan 和 JSON-first KB promotion。

## 后续候选

下一步是独立 Validation delta review；在该 review 完成前，不得将本 repair 写成 `S-024 Done`、`SP-004 complete`、rights approved、release authorized 或 remote success。
