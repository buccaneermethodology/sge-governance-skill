# SP-004/S-024 公共边界 readable card

## 场景：公共候选身份、定位器与历史残留隔离

```gherkin
Given manifest 声明私有 source、公共 project、Skill 和 candidate 四个不同身份
And provenance policy 将不可随包提供的来源标记为 typed private 或 external
And semx deny token 作为隔离控制而不是产品依赖
And locator inventory 覆盖 Dashboard/Archives、Dashboard/Agent_Logs、Dashboard/Artifacts 三个 private surface
And 未声明的相对 private locator 与缺失 semx deny token 必须 fail closed
When 运行 public candidate 与 repository doctor gates
Then 身份冲突、私有历史相对链接和 active public residue 必须 fail closed
And 通过只表示当前本地候选范围的结构性证据，不表示 rights、release 或远端状态
```

## 证据入口

- `public_export_manifest_v1.json`：身份矩阵、locator policy、residue policy。
- `Dashboard/tools/doctor.py`：公共身份、locator 与 residue gate。
- `tests/test_public_candidate.py`、`tests/test_repository_quality.py`：可重算测试。
