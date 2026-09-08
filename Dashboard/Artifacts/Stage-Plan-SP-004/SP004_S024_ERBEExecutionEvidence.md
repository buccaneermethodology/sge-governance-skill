# S-024 ERBE 执行证据

## 关键结论中文展开

本证据仅支持三组冻结 case identity 的本地 ERBE 执行：RED-03/05/06 均由最小临时 fixture 触发对应 gate 的失败；GREEN-07/09/10 在同一 identity 上从当前 durable inputs 独立重算通过。`contract_verdict=valid`、`execution_verdict=ok`，且环境错误为空。

冻结 Cases 的 fingerprint 是自然语言；当前 gate 的可执行输出是 `untyped_private_relative_locator`、`deny_token_missing`、`private_surface_in_public_allowlist`。三者分别由 fixture 直接触发冻结语义 fingerprint，Transcript 保留了 raw output 与 fixture digest；这不是 producer 字段自报。

## RED 结果

| case identity | 冻结 fingerprint | gate 实际 fingerprint | 结果 |
|---|---|---|---|
| `SP004-RED-03` | public locator points to private Dashboard relative path | `untyped_private_relative_locator` | `trusted_red`：匹配冻结语义 |
| `SP004-RED-05` | deny token is treated as product dependency or removed | `deny_token_missing` | `trusted_red`：匹配冻结语义 |
| `SP004-RED-06` | private Dashboard history enters public allowlist | `private_surface_in_public_allowlist` | `trusted_red`：匹配冻结语义 |

## GREEN 独立重算

`SP004-GREEN-07`、`SP004-GREEN-09`、`SP004-GREEN-10` 分别调用 `check_public_provenance_locators`、`check_public_residue`、`inventory_public_locators`，复用对应冻结 case identity，直接读取当前 manifest、README、doctor 与 public surface inventory；三项均 `pass`，无 findings。

## 证据与边界

- [执行 Transcript](SP004_S024_ERBEExecutionTranscript.json) 保存 runner identity、raw command/output、fixture/source digest 与环境错误。
- [冻结 Contract](SP004_S023_Contract.json) 与 [冻结 Cases](SP004_S023_Cases.json) 未修改；摘要分别为 `da0d15e9…f42a8b2` 与 `4ffb3b1a…8262fb3`。
- [PDI 修复](SP004_S024_PDIRepair.md) 与 [Delta Review](SP004_S024_DeltaValidationReview.md) 已读取；其既有 producer artifact 不被本证据当作独立 execution evidence。
- 未执行远端、rights、release、Git handoff 或 production readiness；不支持 S-024 全部完成、SP-004 完成或 Goal complete。

## 门禁结论

`contract_verdict=valid`：冻结 Contract/Cases identity 与 required case IDs 可定位。

`execution_verdict=ok`：六个指定 gate 调用均无环境、fixture、import 或 path error；三项 RED 的实现 fingerprint 与冻结语义一一对应，三项 GREEN 为独立重算通过。

最大主张：仅为 card 允许的 frozen-case execution evidence；不升级为 rights、release、远端或全量 Session 完成结论。
