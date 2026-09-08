# S-002 设计交接：通用 SGE 核心与项目配置

## 任务解释

本 Session 把固定 revision 的来源策略重新冻结为可执行的 SGE 治理核心，并用 audio-transcriptor profile 注入项目路径。它不实现音频转写，也不把 Semx 的产品阶段、KYM/TCO 数据或 runtime/SAG 执行器带入目标仓库。

## 已冻结边界

- canonical truth：`kb/data/strategy/`；阅读面：`kb/docs/strategy/`；执行状态：`Dashboard/`。逐文件来源裁决由 Dashboard execution ledger 承载；KB 中的 mapping 文件只定义可复用 policy，不承载本项目 56 个文件的进度或分类。
- 核心 Skill：`.codex/skills/sge-governed-checkpoints/`；不再依赖外部 Semx 路径。
- 产品设计：`kb/bm-doc/audio-transcriptor-skill_design_v1.0.md` 字节不变。
- optional extension：`build-kym`、`build-tco-coverage` 仅登记为未来领域扩展，不是核心依赖。

## 合同切片

1. 身份与 authority：profile 驱动根目录，禁止把来源身份当作目标身份。
2. SGC：claim/evidence 分层、SI-1..SI-6 与 forbidden collapses。
3. ERBE：适用性、冻结 cases、同 identity RED/GREEN、Builder write exclusions。
4. 来源映射：Dashboard ledger 对 56 个 strategy 表面逐项定类；KB mapping policy 只定义 decision vocabulary、canonical-source 追溯和 promotion 边界；Markdown 不直接升级为 truth。
5. 失败语义：observation≠truth、diff≠resolution、request≠decision、approved≠executed。

## Builder write exclusions

Builder 不得修改冻结的 profile、source manifest、canonical mapping、ERBE contract/cases/expected、RED evidence、claim ceiling 或原始产品设计；变更必须通过 Contract Patch、Scope Delta 与重新 RED。上述对象构成统一的 machine/prose write-exclusion 集合。

## Validation handoff

Validation 需独立检查上述文件、最终 diff、identity/path residue、56/56 mapping、JSON schema、ERBE/SGC contracts 与 Dashboard 状态；不得以工具自报或局部结构通过替代独立 verdict。

## 设计结论

`sge-governed-checkpoints` 是通用核心；项目 profile 是适配层；领域 Skill 和编排器均为可选层。该切片允许进入 S-003 tooling/registry 迁移，不允许声称产品或公共发布就绪。
