# SP-002 / S-010 新手 clean-room 独立 UAT

## 任务理解与边界

本 lane 以陌生新手视角验证当前公共候选的真实入口：从新建临时目录重放 `doctor`、`export`、`bootstrap`、`install`、已安装 core、`upgrade` 与可恢复 `uninstall`，并核对错误恢复、身份/绝对路径隔离及声明边界。本报告只记录独立执行观察，不修改 Builder 产物，也不批准 release、push、production 或普遍适用。

最大声明强度为 `execution_bound`（仅受本次实际执行约束）和 focused tests 的 `test_bound`（仅受指定测试约束）。它们不能合并为“公共候选完成”。

## Read Manifest

| 表面 | 读取状态 | 用途或证据边界 |
| --- | --- | --- |
| [仓库硬门](../../../AGENTS.md) | 已读 | 固定 validation read-mostly、唯一写范围和中文输出要求。 |
| [SGE governed checkpoints](../../../.codex/skills/sge-governed-checkpoints/SKILL.md) 与 `references/checklists.md` | 已读 | 应用 Validation Agent、Context Bootstrap、SGC v1 与 claim ceiling。 |
| [S-010 lane card](SP002_S010_UATLaneTaskCard.json) | 已校验并读取 | 指定摘要校验通过：`card_id=sp002-s010-newcomer-uat-v1`；固定验收 ID、唯一输出和最大声明。 |
| [SP-002 Loop Goal](SP002_SGEOpenSourceNewcomerReadiness_LoopGoal.md) | 已读相关完整目标面 | 对照 SP002-MH-04/05/07/09、Session DAG、Completion Rule 和发布边界。 |
| [ERBE Contract](SP002_ERBE_Contract.json) / [Cases](SP002_ERBE_Cases.json) | 已读 | 对照 lifecycle predicate、C01/C02/C04/C05/C06/C07 与禁止折叠。 |
| [Quick Start](../../../docs/Quick_Start_CN.md) / [Beginner Guide](../../../docs/Beginner_Guide_CN.md) | 已读 | 逐条核对可复制命令、恢复说明和用户可读性。 |
| [public export manifest](../../../public_export_manifest_v1.json) | 已读并实际导出 | 核对 allowlist、default-deny、候选状态及 forbidden surfaces。 |
| [public lifecycle 工具](../../../tools/sge_public.py) | 已读相关实现并实际执行 | 核对返回码、backup、trash 与 doctor 扫描边界。 |
| [SGC v1 canonical contract](../../../kb/data/strategy/strategy_sgc_structural_contract_v1.json) | 已读相关声明边界 | 防止 doctor/test/UAT 与 release/production 的错误折叠。 |
| `Dashboard/Sessions.md`、最终 OPCM、最终 closeout、最终 Semantic/Validation Review | 本 lane 未作为完成证据读取 | 这些属于 S-011 / Goal 最终收束；缺失不妨碍给出 S-010 的失败判定，但禁止据此声称 SP-002 完成。 |
| 远端 release、网络、provider、生产环境 | 按 card 明确跳过 | 超出本 lane authority；不影响本次本地 clean-room 观察。 |

Context Bootstrap 使用 `validation` profile 在 `/tmp/sp002_s010_uat_context_bootstrap.json` 校验通过。首次临时包因漏列认知域返回 `epistemic_search_space_narrowed`，补齐读取域与四个 mandatory validation surfaces 后通过；这属于 lane 启动包自检，不是被测候选失败。

## 逐步观察

本次临时根目录为 `/tmp/sge-s010-uat.uletUI`；源仓库之外的写入仅发生在该临时目录。命令输出摘要如下。

| 步骤 | 命令或检查 | 观察 | 判定 |
| --- | --- | --- | --- |
| 1 | `python3 tools/sge_public.py doctor` | `public_doctor:pass`，返回码 0。 | 通过 SP002-C01 的当前实现检查，但见 Blocking Finding B1。 |
| 2 | `python3 tools/sge_public.py export /tmp/sge-s010-uat.uletUI/exported` | `exported:47`；实际 48 个文件含 `EXPORT_METADATA.json`。allowlist 47/47，无缺失、无额外文件。 | allowlist exactness 通过。 |
| 3 | 对 exported candidate 再跑 `doctor` | `public_doctor:pass`，返回码 0。 | 导出物可自检，但不证明 manifest 自身无身份残留。 |
| 4 | `bootstrap` 新目标 | 创建 README、AGENTS、profile 与 Dashboard 最小表面，返回码 0。 | 通过。 |
| 5 | 从 exported candidate `install` | `installed:17`，返回码 0。 | core 安装通过。 |
| 6 | 执行已安装的 intake guard | 输出 Task Intake Evaluation Guard，返回码 0。 | SP002-C07 通过；无 optional extension 也能执行 core。 |
| 7 | `upgrade` | `upgraded:17`，返回码 0；`.sge-backups/` 中有 17 个备份文件。 | 可恢复升级路径通过本次执行。 |
| 8 | 对非空目录执行 `bootstrap` | 返回码 1，精确输出 `destination_must_be_empty`。 | SP002-C05 可信负例通过。 |
| 9 | 对无 install record 的目录执行 `uninstall` | 返回码 1，精确输出 `uninstall_requires_install_record`。 | SP002-C06 可信负例通过。 |
| 10 | allowlisted 文档注入 `/Users/xiaomei/private-fixture` 后跑 `doctor` | 返回码 1，输出 `identity_or_private_residue:docs/Quick_Start_CN.md:/Users/xiaomei`。 | SP002-C04 负例通过；scanner 对普通 allowlisted 文件有效。 |
| 11 | `uninstall --target` | `uninstalled_recoverable`，返回码 0；core 原路径消失，`.sge-trash/` 中保留 1 个 `SKILL.md`，目标 `AGENTS.md` 仍存在。 | recoverable uninstall 通过且未覆盖目标 authority。 |
| 12 | 导出物边界 | `Dashboard/` 文件数为 0。 | 私有执行面目录隔离通过。 |
| 13 | `python3 -m unittest tests.test_public_candidate tests.test_loop_orchestrator` | 7 tests 通过。 | focused regression 通过；不能替代新手 UAT。 |

## Blocking Findings

### B1：导出包自身携带私有绝对路径和项目身份 token，doctor 因显式跳过 manifest 而误报通过

严重度：P0，阻断 SP002-MH-09、S-010 有界通过以及任何“导出物无私有身份/绝对路径残留”的声明。

具体复现：

```bash
python3 tools/sge_public.py export /tmp/sge-s010-uat.uletUI/exported
rg -n '/Users/xiaomei|semx-cli|semx-kb|S-384|S-485|audio-transcriptor' \
  /tmp/sge-s010-uat.uletUI/exported/public_export_manifest_v1.json
python3 /tmp/sge-s010-uat.uletUI/exported/tools/sge_public.py doctor
```

实际证据：scan 命中 exported manifest 第 57 行：

```text
"forbidden_surfaces": ["/Users/xiaomei", "semx-cli", "semx-kb", "S-384", "S-485", "audio-transcriptor"]
```

随后 doctor 仍输出 `public_doctor:pass`。根因可定位到 [tools/sge_public.py](../../../tools/sge_public.py)：`validate()` 在扫描正文前对 `public_export_manifest_v1.json` 直接 `continue`，因此 manifest 自身不受 identity/private residue 检查。

影响：ERBE 的 `private_identity_tokens_rejected` 对普通 allowlisted 文件成立，但没有覆盖导出 manifest 这一真实公开文件；Loop Goal 的 SP002-MH-09 要求新 repo/示例/卸载无私有路径或产品身份残留，本次导出物不满足。`doctor pass` 与“没有残留”发生 forbidden collapse 风险。

Required Builder repair：将公开 manifest 的扫描规则改为不携带私有具体身份，或把私有 denylist 放到不会被导出的内部验证输入；同时让 doctor 对最终导出集合（包括 manifest）执行可审计扫描，并加入 manifest-self-residue 回归例。修复后必须从新空目录重跑本报告全部 lifecycle 和 scan。

### B2：公开新手文档没有给出 export 与 upgrade 的可复制命令，完整 lifecycle 不是按文档可重放

严重度：P1，阻断 Loop Goal Completion Rule 第 5 项和“新手只按 Guide/Quick Start 可完成全部指定 lifecycle”的声明。

具体证据：

- [Quick Start](../../../docs/Quick_Start_CN.md) 只列出 doctor、bootstrap、install、intake guard 和 uninstall；没有 export 或 upgrade。
- [Beginner Guide](../../../docs/Beginner_Guide_CN.md) 同样没有 export 命令；只描述“升级失败”的恢复语义，没有提供 upgrade 命令、成功标志或备份检查命令。
- 本 lane 必须额外运行 `python3 tools/sge_public.py --help`、`export --help` 和 `upgrade --help` 才能确定参数，说明完整路径并非从新手文档直接可复制。

Required Builder repair：在 Quick Start 或 Beginner Guide 中补齐从候选源到 clean staging 的 export 命令、从 exported source 安装/升级的命令、预期成功输出与 backup 恢复检查；明确运行目录和 source/target 含义。修复后由独立 newcomer lane 仅依文档重放，不借助源码或 `--help` 补全主路径。

## Nonblocking Findings

### N1：运行时输出把 `/tmp` 规范化为 `/private/tmp`

工具输出中的目标路径从文档输入 `/tmp/...` 显示为 `/private/tmp/...`，这是 macOS 路径解析结果，不是用户私有身份残留。本次 target 内容扫描没有命中 `/Users/...`、Semx token 或其他 manifest deny token，因此该现象不单独阻断；文档若追求跨平台可读性，可补一句说明。

### N2：现有 focused tests 证明实现合同，不证明文档可发现性

7 个测试全部通过，且覆盖 allowlist、lifecycle 和部分负例；但测试直接调用实现 API，不会发现 B2 的文档缺命令问题，也因当前设计跳过 manifest 而未发现 B1。后续应保留测试通过事实，同时避免把它上推为独立 newcomer acceptance。

## Scope Narrowing / Overclaim 检查

- Scope narrowing：未缩窄 card 指定的 doctor、export、bootstrap、install、upgrade、uninstall、恢复、身份/路径和 claim boundary；各项均有实际观察。
- Overclaim：发现。当前 `doctor:pass` 若解释为“所有导出文件无私有身份残留”，超过实现实际检查范围；manifest 自身被豁免。
- Public/release/production：严格分轴。本报告不批准发布、不证明生产就绪、不证明任意仓库适用。

## KB / Dashboard Truth Split 与语义升级

本报告是 S-010 execution memory，写入 Dashboard 合适；没有稳定治理 truth 获得批准，因此不更新 `kb/`。B1 是现有 public/private contract 的实现违反，不是新合同；B2 是当前文档验收缺口。两项都应先由 Builder 在现有 S-010/S-008 范围修复，不需要用新增语义规则掩盖。

本 lane 不启动新的 Semantic Reviewer：没有新增 glossary、public/private authority、acceptance posture 或 release claim；这里只按冻结合同报告实现与文档不一致。最终 S-011 仍需按 Goal 运行既定 Semantic Review。

## 有界 Verdict

`fail`（S-010 newcomer UAT 阻断）：lifecycle 的执行与恢复路径大部分通过，但 exported manifest 仍暴露私有绝对路径/项目身份 token，且新手文档缺少 export/upgrade 的可复制主路径。因此当前证据不支持 S-010 “有界通过”，也不支持 SP-002/public candidate 完成。

允许声明：本次 clean-room 中 doctor、allowlist export、bootstrap、install、core intake、upgrade backup、两条恢复负例和可恢复 uninstall 按观察通过。

禁止声明：导出物无私有身份/绝对路径残留；新手仅凭当前文档可重放完整 lifecycle；release 已授权；production ready；SP-002 complete。

Required Builder repair：修复 B1 与 B2 后，使用新的空临时目录进行独立 re-UAT；在此之前 verdict 保持 `fail`。

---

## 2026-09-02 B1/B2 修复后的 Delta UAT

### Delta 边界与 Read Manifest

本轮先校验 [Delta UAT lane card](SP002_S010_DeltaUATLaneTaskCard.json)，结果为 `pass`（表示 card 结构、引用摘要和 delegation identity 与指定值一致）。本轮采用 delta-only Validation，不重读完整 baseline，也不修改实现；父 snapshot 为本报告前一版。

| Delta 表面 | 读取状态 | 与 B1/B2 的关系 |
| --- | --- | --- |
| [public export manifest](../../../public_export_manifest_v1.json) | 已读修复后文件 | B1：具体私有 token 已从 public manifest 移除，改用不嵌入身份的 `content_policy`。 |
| [public lifecycle 工具](../../../tools/sge_public.py) | 已读修复后文件 | B1：doctor 不再跳过 manifest；对所有 allowlisted 文件应用通用 Unix home-path 检查。 |
| [Quick Start](../../../docs/Quick_Start_CN.md) | 已读修复后文件 | B2：补齐 export、staging source、upgrade、backup 定位及 recoverable uninstall 主路径。 |
| [Beginner Guide](../../../docs/Beginner_Guide_CN.md) | 已读修复后文件 | B2：补齐 export/upgrade 命令、成功输出、source/target 语义和恢复说明。 |
| [focused public candidate tests](../../../tests/test_public_candidate.py) | 已读修复后文件 | 新增 manifest-self-identity 与完整文档 lifecycle 回归，并保留 lifecycle/负例测试。 |

未重读表面：Loop Goal、ERBE、KB、其他 Dashboard/closeout 和非 delta tests。本轮沿用已验证 parent snapshot 的原始目标与 claim ceiling；card 固定摘要均通过，未出现 rebaseline trigger。该限制意味着新 verdict 只回答 B1、B2 及其直接影响的 S-010 范围，不回答 SP-002 最终完成。

### 仅按文档的全新空目录重放

新临时根目录：`/tmp/sge-s010-delta-uat.oNARLQ`。为避免占用文档中的共享固定目录，本轮只把文档的 `/tmp/sge-public-candidate` 与 `/tmp/sge-demo` 等价替换为该全新根目录下的同名子目录；命令顺序、参数和 source/target 关系均来自修复后的 Quick Start/Beginner Guide，没有借助 `--help` 或源码补全主路径。

| 文档步骤 | 实际观察 | 结果 |
| --- | --- | --- |
| source `doctor` | `public_doctor:pass`，返回码 0 | 通过 |
| `export` 到 clean staging | `exported:47`，返回码 0 | 通过 |
| `bootstrap` 空 target | `bootstrapped`，返回码 0 | 通过 |
| 从 staging `install` | `installed:17`，返回码 0 | 通过 |
| 执行已安装 intake guard | guard 正常输出，返回码 0 | 通过 |
| 从 staging `upgrade` | `upgraded:17`，返回码 0 | 通过 |
| `find .sge-backups -name SKILL.md` | 找到 1 个旧 core `SKILL.md` | 通过 |
| exported candidate 再跑 `doctor` | `public_doctor:pass`，返回码 0 | 通过 |
| recoverable `uninstall` | 返回码 0；当前 core 消失，`.sge-trash/` 保留 1 个 `SKILL.md`，target `AGENTS.md` 仍存在 | 通过 |
| `python3 -m unittest tests.test_public_candidate` | 6 tests 通过 | 通过；仅作 focused regression，不替代本次 UAT |

### B1 独立复现结果：已关闭

对最终 exported candidate 根目录执行递归 scan；该目录中已确认 `public_export_manifest_v1.json` 存在，因此 manifest 自身包含在扫描范围内：

```bash
rg -n -i '/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|[A-Za-z]:\\Users\\[A-Za-z0-9._-]+|xiaomei|semx-cli|semx-kb|S-384|S-485|audio-transcriptor' \
  /tmp/sge-s010-delta-uat.oNARLQ/sge-public-candidate
```

实际结果：`rg` 返回码 1，即没有命中；`manifest_present=yes`。随后 exported candidate 的 doctor 返回 `public_doctor:pass`。

本 scan 检查的是私有身份 token 和私有 home 绝对路径。文档刻意使用的 `/tmp/...` disposable clean-room 路径属于公开操作参数，不解释为私有身份残留。

B1 原失败指纹“manifest 第 57 行含 `/Users/xiaomei` 等具体 token，同时 doctor 因跳过 manifest 而 pass”本轮无法复现：manifest 已不含这些 token，且 `validate()` 已扫描 manifest 正文。结论：B1 在当前 delta snapshot 内关闭。

### B2 独立复现结果：已关闭

本轮没有运行 CLI `--help` 来补全步骤。仅按 Quick Start/Beginner Guide 即可发现并顺序完成：doctor → export → bootstrap → install → core guard → upgrade → backup 定位 → recoverable uninstall；staging source 与 target project 的角色也有明确解释。

B2 原失败指纹“文档缺 export/upgrade，可执行者必须借助 `--help` 才能完成 lifecycle”本轮无法复现。结论：B2 在当前 delta snapshot 内关闭。

### Delta Findings

- Blocking findings：无。B1、B2 的原始 failure fingerprints 均未复现。
- Nonblocking findings：命令输出在 macOS 上仍会把 `/tmp/...` 规范化显示为 `/private/tmp/...`；这是平台路径解析，不包含用户身份，也不影响文档参数和恢复性。
- Scope/overclaim：未发现本轮新增 scope narrowing。doctor、测试与一次 clean-room 重放只支持当前候选和当前环境的有界证据，不支持 release、production、普遍适用或 SP-002 最终完成。
- KB/Dashboard：本轮只追加 S-010 execution evidence；没有稳定 truth 变化，不更新 KB。实现修复本身由 Builder delta files 承载，本 lane 未修改它们。

### 新的有界 Verdict

`pass-with-findings`（B1/B2 delta UAT 有界通过）：B1 的 manifest-self private residue 与 doctor skip 问题、B2 的文档 lifecycle 缺口，在当前修复后的 delta snapshot 中均已独立复现为“不再发生”；受影响的 SP002-MH-04、SP002-MH-05、SP002-MH-07、SP002-MH-09 仅就 B1/B2 和本次重放范围获得支持。

这里的 `pass-with-findings` 表示允许后续 S-010/S-011 消费本次 delta evidence；唯一 finding 是 macOS `/tmp` 显示规范化，属于非阻断观察。它不批准 release，不证明 production ready，不证明任意仓库适用，也不等于 `SP-002 complete`。最终状态仍需 S-011 的完整 OPCM、Validation、Semantic Review、closeout 与 post-closeout reconciliation。
