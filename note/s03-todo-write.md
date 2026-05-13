# S03 TodoWrite 学习笔记

## 本课主题

S03 在 S02 的工具调用循环之上新增 `TodoManager` 和 `todo` 工具，让 agent 在执行多步骤任务时先拆分计划，再持续更新进度。

本课核心不是让程序替模型写死流程，而是让 harness 提供一个结构化计划板：模型自己规划、执行、标记进度；harness 负责校验状态、展示进度，并在模型忘记更新时提醒。

## 我已经理解的内容

- S03 的核心机制是 TodoWrite，也就是让模型维护一个 todo list。
- TodoWrite 解决的问题是长任务中模型容易跑偏、忘记目标、用户看不见进度。
- agent loop 没有被重写，仍然是“模型输出 tool_use -> harness 执行工具 -> tool_result 回填”的循环。
- S03 只是在原有循环上增加了 `todo` 工具和 nag reminder。
- `rounds_since_todo >= 3` 时，harness 会注入 `<reminder>Update your todos.</reminder>`，提醒模型更新 todo。
- 对于“大范围任务”，例如重构认证模块，S03 比 S02 更适合，因为任务需要拆成多个可推进的小步骤。
- `todo` 工具返回的是结构化任务状态渲染，用户可以看到任务拆解和完成进度。

## 需要修正的理解

### 同一时间只能有一个 in_progress

我一开始认为下面的 todo 更新是合法的：

```json
[
  {"id": "1", "text": "Read hello.py", "status": "in_progress"},
  {"id": "2", "text": "Refactor hello.py", "status": "in_progress"}
]
```

实际是不合法的。`TodoManager` 明确限制同一时间只能有一个 `in_progress`：

```python
if in_progress_count > 1:
    raise ValueError("Only one task can be in_progress at a time")
```

原因是 agent 需要有唯一的当前焦点，这样进度才清晰、可观察、可推进。

### TodoWrite 不是为了写死决策

我一开始对“为什么让模型自己维护 todo”不够清楚。正确理解是：harness 不应该规定下一步必须做什么，否则就变成硬编码 workflow。

S03 的设计是：

```text
模型负责计划和更新进度
harness 负责提供工具、校验状态、提醒更新
```

这样既保留了模型的自主性，又让执行过程变得可见、可约束。

## 实操中遇到的问题

### Python 环境问题

一开始执行 `python agents/s03_todo_write.py` 没有进入预期流程，是因为 Windows 的 `python` 指向了 Microsoft Store 占位符，且 `pip` 不在 PATH 中。

处理方式：

- 删除 WindowsApps 下的 `python.exe` / `python3.exe` 商店别名。
- 安装真实 Python 3.12。
- 将以下路径加入 PATH：

```text
C:\Users\lilintao\AppData\Local\Programs\Python\Python312
C:\Users\lilintao\AppData\Local\Programs\Python\Python312\Scripts
```

### API Base URL 问题

最初 `.env` 中使用的是：

```env
ANTHROPIC_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
```

这会导致 Anthropic SDK 请求 Messages API 时返回 404。后来改成：

```env
ANTHROPIC_BASE_URL=https://token-plan-cn.xiaomimimo.com/anthropic
```

脚本才成功进入模型调用流程。

### Tool Calling 兼容性问题

运行 S03 时出现：

```text
> todo:
Error: 'items'
```

这说明模型或兼容接口调用 `todo` 工具时，没有按 schema 传入必需的 `items` 字段。这不是 Python 环境问题，也不是文件系统问题，而是 tool calling 兼容性或模型遵循工具 schema 的问题。

文件工具已经能正常运行，例如 `write_file` 成功创建了 `hello.py`，但 S03 的 TodoWrite 教学效果没有完全正常。

## 本课总结

S03 的关键收获是：计划不应该由 harness 写死，而应该由模型自己维护；harness 的职责是提供结构化工具、校验约束、展示状态，并在模型偏离时提醒。

一句话总结：

```text
没有计划的 agent 走哪算哪；有 TodoWrite 的 agent 才能让长任务变得可见、可控、可推进。
```

## 后续复盘问题

- 为什么 `todo` 是工具，而不是直接写进 system prompt？
- 如果模型连续多轮不更新 todo，nag reminder 会如何改变上下文？
- 如果要让当前兼容模型更稳定地调用 `todo`，是否需要修改工具 schema 或增加容错逻辑？
