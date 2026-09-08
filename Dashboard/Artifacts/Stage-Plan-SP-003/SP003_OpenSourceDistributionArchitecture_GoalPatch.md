# SP-003 Goal Patch：Open-source Distribution Architecture 实现阶梯

## Patch 身份

- Patch ID：`SP003-GP-001`。
- Base Goal：`SP-003`，revision `2`（公开仓名称修订后的基础合同）；机器 patch：[SP003-GP-001.json](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalPatch.json)。
- Base digest：由 [Goal Contract Base](../Stage-Plan-SP-003/SP003_OpenSourceDistributionArchitecture_GoalContract_Base.json) 的 `goal_patch.py validate-goal` 产生并绑定在机器 patch 中；名称修订后的当前摘要已重新计算。
- Sequence：`1`；target section：`implementation_ladder`。
- Scope Delta：`none`。本次只修订公开仓身份并重新绑定基础合同；本 Patch 仍只把已冻结的 Stage Plan DAG 解析为有序实现阶梯，不删除、替换、降级或延期任何 ODA-MH。

## Replacement

将单一最小安全入口扩展为 `S-016 → S-017 → S-018 → S-019 → S-020 → S-021 → S-022`：先冻结合同和负例，再进入维护者投影、用户生命周期、身份/权限、贡献回流、独立验证与最终对账。`S-016` 是实现入口，不是 Goal 终止条件。

## 设计理由

参考现有 kym-tco 双仓策略的 machine contract 结构，SP-003 明确 source/public repo、release identity、allowlist、file classes、export modes、forbidden features、license gate、packaging、maintenance 与 rollback；同时保留 SGE 自身的 `kb/` canonical truth、`Dashboard/` execution memory 和 independent Validation 边界。

## 不变边界

- `sge-governance-skill` 是唯一 canonical development source。
- `bm-sge-governance` 是 exact-allowlist deterministic public projection/distribution repo。
- 普通用户从公开仓 clone/install/upgrade，只需要 target；`--source` 只能作为高级/测试参数。
- public candidate、release authorization、GitHub mutation、published、production-ready 仍为不同状态轴。
- 本轮不执行任何远端写入，不创建 public repository。
