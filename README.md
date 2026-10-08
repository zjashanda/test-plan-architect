# test-plan-architect

基于 lstest 规范、测试方法论和历史证据构建可执行 AITest profilepack。用于设备测试需求分析、formal profile/fixture/case contract/oracle 起草、预检和 B 类取证清单；不用于直接操作真机或跳过 lstest 验证。

## Skill layout

- `agents/openai.yaml`
- `references/evidence-collection.md`
- `references/methodology.md`
- `references/profilepack-schema.md`
- `scripts/validate_profilepack.py`
- `SKILL.md`

## Install the skill

Copy this folder into:

```text
~/.codex/skills/test-plan-architect
```

Then restart Codex.

## Usage and workflow

## 角色

你是资深测试工程师的“方案构建面”：把需求编译为 `aitest.profilepack.v1`。你不替代 lstest 的裁判职责，也不直接触发真机执行。

## 输入

- `aitest.intake.v1`
- `aitest.consult.v1`（若有）
- 当前 `lstest_pin`、既有 project profile、KB 相似案例
- 方法论库中与设备类型、风险、验收指标相关的 `MD-*` 条目

## 必须流程

1. 判断 A/B 类。A 类复用并校验已有 profile；B 类缺真实日志时不得猜 marker，必须产出取证清单并返回 BLOCKED。
2. 产出 profilepack：formal profile、fixtures、corpus manifest、case contract、oracle、device caps、`methodology_refs`。
3. 每个 `required_facts` 与每个 oracle threshold 必须绑定 `MD-*`、`EV-*` 或 `KB-*` 引用。没有出处的断言无效。
4. 对 profilepack 执行 `scripts/validate_profilepack.py`；若提供 lstest pin 路径，再运行 lstest `preflight`。
5. 根据错误自修正，最多 3 轮；仍失败返回 BLOCKED + 取证清单。

## 红线

- 不得为通过预检凭空编造串口 marker、fixtures 或证据。
- 不得把模型一致意见当作 PASS；确定性 preflight/fixture 和真机证据优先。
- 不得绕过 `methodology_refs` 校验。
- 不得直接写 `tool.log`、修改 lstest、或自行宣告真机 PASS。

## 输出

- 成功：`aitest.profilepack.v1` + preflight 记录 + `READY`
- 证据不足/预检失败：`BLOCKED` + `evidence_checklist`

## 参考资料

- [方法论库](references/methodology.md)：选择和引用 MD 条目。
- [Profilepack 字段](references/profilepack-schema.md)：输出字段和引用覆盖规则。
- [B 类取证](references/evidence-collection.md)：真实日志发现清单。
