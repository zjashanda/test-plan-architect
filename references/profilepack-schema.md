# profilepack 字段

`aitest.profilepack.v1` 最少包含：

- `lstest_profile`：schema_version=2 的 formal profile
- `corpus_manifest`：case_id/text/audio_sha256
- `case_contract.required_facts` 与 timeline
- `oracle.pass_criteria` / `oracle.thresholds`
- `device_caps`：串口角色、声卡 stable key、唤醒词
- `methodology_refs`：每个 required_facts 和 threshold 至少一个 MD/EV/KB 引用
- `profile_sha256` / `lstest_pin` / `preflight`

校验失败时不得进入 schedule。
