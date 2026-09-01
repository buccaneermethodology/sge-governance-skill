audio-transcriptor-skill 设计方案 V1.0

一、Skill 的定位
建议 Skill 名称：
audio-transcriptor
核心职责：
将本地音频/视频文件转写为可追溯的文本资产，并在不改变原意的前提下生成适合阅读的清洗稿。
它不是会议总结 Skill，也不是文章生成 Skill。
边界要明确：
Audio/Video
   ↓
Normalize
   ↓
ASR / Whisper
   ↓
Raw Transcript
   ↓
Clean Transcript
   ↓
Metadata / Evidence
可选后处理：
Clean Transcript
   ↓
Summary / Article / Analysis
后处理不应该污染原始转写轨道。

⸻

二、推荐的 V1 功能范围
V1 建议只做 7 件事：
1. 接收本地音频或视频路径；
2. 检查文件和依赖；
3. 用 FFmpeg 统一音频；
4. 调用本地 Whisper；
5. 保留 raw transcript；
6. 使用 Coding Agent/LLM 清洗文本；
7. 输出 metadata 和完整 artifact 目录。
明确不做：
* Speaker diarization；
* 自动识别具体人员姓名；
* 复杂会议纪要；
* 自动生成文章；
* 云端 Whisper API；
* 自动上传任何音频；
* 原文不支持的信息补全。
这样 V1 比较容易真正做到稳定。

⸻

三、推荐目录结构
Skill 本身：
audio-transcript/
├── SKILL.md
├── README.md
├── scripts/
│   ├── transcribe.sh
│   ├── normalize_audio.sh
│   ├── check_env.sh
│   └── build_metadata.py
├── references/
│   ├── terminology.md
│   ├── transcript-cleaning-rules.md
│   └── usage-examples.md
├── prompts/
│   └── clean-transcript.md
├── schemas/
│   └── transcript_metadata.schema.json
└── tests/
    ├── fixtures/
    └── test_cli.sh
运行以后，每个音频建议形成独立 artifact 目录：
meeting-2026-08-31/
├── source/
│   └── original.m4a
├── normalized/
│   └── audio.wav
├── transcript/
│   ├── raw.txt
│   ├── raw.json
│   ├── raw.srt
│   └── clean.md
├── metadata.json
├── issues.json
└── run.log
不过原始文件最好默认不复制，避免大文件重复占空间。更推荐：
{
  "source_path": "/Users/xiaomei/Documents/audio/meeting.m4a"
}
只记录引用。

⸻

四、核心 Pipeline
建议内部划分为 6 个 Stage。
Stage 0 — Input Validation
检查：
path exists
file readable
supported extension
ffmpeg available
whisper available
model available
output dir writable
支持格式至少：
m4a
mp3
wav
aac
flac
mp4
mov
输出：
input_status = PASS / FAIL
如果失败，不进入后续阶段。

⸻

五、Stage 1 — Audio Normalization
不要把所有格式直接扔给 Whisper。
统一通过 FFmpeg 转为：
16 kHz
mono
PCM WAV
例如逻辑：
ffmpeg \
  -i input.m4a \
  -ar 16000 \
  -ac 1 \
  normalized.wav
为什么值得做这一层：
* 减少不同输入格式带来的变量；
* 方便重跑；
* 方便定位转写问题；
* 视频也可以统一提取音轨；
* downstream 更稳定。

⸻

六、Stage 2 — Raw Transcription
这里推荐使用：
whisper.cpp
而不是云 API。
V1 默认：
engine: whisper.cpp
language: auto or zh
model: medium
建议支持 CLI 参数覆盖：
audio-transcript input.m4a \
  --language zh \
  --model medium
Raw Transcript 必须尽量保持 ASR 输出，不要让 LLM直接修改。
至少输出：
raw.txt
raw.json
raw.srt
其中：
raw.txt
纯文本。
raw.json
保留 segment 和 timestamp。
例如：
{
  "segments": [
    {
      "start": 0.0,
      "end": 8.7,
      "text": "我们现在做的是L2a事实提取..."
    }
  ]
}
raw.srt
方便以后回听。
这是很重要的 provenance。

⸻

七、Stage 3 — Terminology Normalization
这是你的场景里特别值得做的一层。
例如 Whisper 可能识别：
SG
SGE
S G E

L二A
L2A
L2a

OPC
O P C

Flow Encoding
Flow-Encoding
FlowE
建议建立：
references/terminology.md
例如：
# Canonical terminology

| Variant | Canonical |
|---|---|
| flow encoding | Flow-Encoding |
| flowe | FlowE |
| l2a | L2a |
| l2b | L2b |
| fact extraction | Fact Extraction |
| process extraction | Process Extraction |
| sge | SGE |
| bmac | BMAC |
| opc | OPC |
| semantic governance engineering | Semantic Governance Engineering |
但这里一定要有一个原则：
只允许做 canonical spelling normalization，不允许改变语义。
例如：
“L二A”
可以修正成：
L2a
但：
“我听起来可能是 SAG”
不应该直接改成 SAG。
不确定时：
[疑似：SAG]

⸻

八、Stage 4 — Clean Transcript
这一层才使用 Codex / LLM。
输入：
raw transcript
+ terminology
+ cleaning rules
输出：
clean.md
清洗规则必须严格。
建议写入：
references/transcript-cleaning-rules.md
核心规则：
MUST:
- preserve meaning
- preserve uncertainty
- preserve technical terminology
- remove meaningless filler when safe
- repair punctuation
- create readable paragraphs

MUST NOT:
- summarize
- infer missing content
- rewrite arguments
- improve logic
- silently resolve ambiguous terms
- invent speaker identity
遇到听不清：
[听不清]
有弱推断：
[疑似：Workflow]
不要静默“帮用户修对”。

⸻

九、推荐 clean.md 格式
例如：
# FlowE L2a 回顾会转写

## Metadata

- Source: `meeting.m4a`
- Language: zh
- ASR engine: whisper.cpp
- Model: medium
- Generated: 2026-08-31

---

## Transcript

我们现在做的是 L2a 的 Fact Extraction。

最开始的问题是，整个 Workflow 虽然已经能生成，但是质量比较差……

……

> [听不清 00:18:42–00:18:47]

……
如果有 timestamp，建议保留关键位置。

⸻

十、Stage 5 — Metadata / Evidence
这是我认为这个 Skill 应该比普通转写工具多做的一步。
生成：
metadata.json
推荐 schema：
{
  "schema_version": "1.0",
  "source": {
    "path": "/Users/xiaomei/Documents/audio/meeting.m4a",
    "sha256": "...",
    "bytes": 12345678
  },
  "normalization": {
    "sample_rate": 16000,
    "channels": 1
  },
  "transcription": {
    "engine": "whisper.cpp",
    "model": "medium",
    "language": "zh"
  },
  "artifacts": {
    "raw_txt": "transcript/raw.txt",
    "raw_json": "transcript/raw.json",
    "raw_srt": "transcript/raw.srt",
    "clean_md": "transcript/clean.md"
  },
  "issues": [],
  "status": "PASS"
}
建议额外记录：
source sha256
model identity
skill version
cleaning rules digest
terminology digest
这样未来 Skill、模型或词表更新以后，你可以明确知道：
为什么这次结果和上次不一样。

⸻

十一、Issues Contract
不要所有问题都只写进日志。
建议：
issues.json
例如：
[
  {
    "type": "low_confidence_segment",
    "timestamp": "00:18:42",
    "text": "...",
    "severity": "warning"
  }
]
推荐 issue types：
input_invalid
ffmpeg_failure
model_missing
transcription_failure
low_confidence_segment
unknown_terminology
cleaning_ambiguity
empty_transcript
后续如果扩展 diarization，可以增加：
speaker_ambiguity
speaker_overlap

⸻

十二、CLI 设计
最终用户接口应该非常简单：
audio-transcript \
"/Users/xiaomei/Documents/audio/FlowE回顾会.m4a"
默认生成：
./FlowE回顾会_transcript/
高级参数：
audio-transcript input.m4a \
  --language zh \
  --model medium \
  --output ./output \
  --terminology ./my-terms.md
建议 V1 参数：
--language
--model
--output
--terminology
--raw-only
--no-clean
--force
--keep-normalized
其中：
--raw-only
只做：
audio → Whisper → raw
不调用 LLM。
这非常重要。

⸻

十三、Skill 调用行为
未来你在 Codex 里只需要说：
使用 audio-transcript 转写 /Users/xiaomei/Documents/audio/FlowE-review.m4a
Skill 应自行：
1. validate
2. normalize
3. transcribe
4. clean
5. generate metadata
6. report artifacts
最后只返回：
PASS

Source:
...

Artifacts:
- raw transcript
- clean transcript
- metadata
- issues

Issues:
2 low-confidence segments
而不是在聊天窗口中直接塞几万字 transcript。

⸻

十四、SKILL.md 建议结构
核心可以这样定义：
# audio-transcript

## Purpose

Convert local audio/video files into traceable raw and cleaned transcripts.

## Primary contract

Audio is source evidence.
Raw transcription MUST remain immutable.
Clean transcript MUST be derived from raw transcript.
Cleaning MUST NOT add semantic content.

## Workflow

1. validate input
2. normalize audio
3. transcribe
4. preserve raw artifacts
5. normalize terminology
6. clean transcript
7. emit metadata and issues

## Authority

The skill MAY:
- normalize audio
- generate transcripts
- fix punctuation
- normalize known terminology

The skill MUST NOT:
- invent missing speech
- infer speaker identity
- summarize unless explicitly requested
- overwrite raw transcript
这个 authority boundary 很重要。

⸻

十五、安装层设计
不要让 Skill 自己随意安装软件。
建议安装单独做：
brew install ffmpeg
brew install whisper-cpp
然后：
audio-transcript doctor
输出：
ffmpeg: PASS
whisper.cpp: PASS
model: PASS
Codex: PASS
如果缺少模型：
MODEL_MISSING
而不是自动联网下载。
这样更可控。

⸻

十六、模型策略
第一版我建议：
default = medium
理由：
你的音频很多属于：
中文
+
英文技术术语
+
多人讨论
+
产品名
+
缩写
small 模型可能速度快，但专业术语错误会明显增加。
后续可以做 profile：
fast:
  model = small

balanced:
  model = medium

accuracy:
  model = large
然后用户可以：
audio-transcript meeting.m4a --profile accuracy

⸻

十七、缓存和幂等性
这个 Skill 很适合做缓存。
cache key：
source_hash
+
model
+
language
+
transcription_config
如果全部一致：
raw transcription reuse
Clean transcript 再使用另一组 key：
raw_hash
+
cleaning_rule_hash
+
terminology_hash
+
cleaner_identity
这样：
修改术语表时：
不重新跑 Whisper
只重新 clean
这是一个很有价值的设计。

⸻

十八、Artifact 不可变规则
建议明确：
raw.txt
raw.json
raw.srt
一旦生成：
immutable
重新运行生成新的 run：
runs/
├── 20260831T120000Z/
└── 20260901T090000Z/
或者使用：
raw-r001.txt
raw-r002.txt
Clean transcript 可以重生成，但不能静默覆盖已经发布的版本。

⸻

十九、建议增加一个 manifest
例如：
manifest.json
记录：
source
↓
normalized audio
↓
raw transcript
↓
clean transcript
可以看成一个很轻量的 lineage graph。
例如：
{
  "source_sha256": "...",
  "normalized_sha256": "...",
  "raw_sha256": "...",
  "clean_sha256": "..."
}
这样以后做 audit 很方便。

⸻

二十、V1 Acceptance Criteria
我建议第一版至少达到以下验收条件：
1. .m4a/.mp3/.wav/.mp4 可以成功输入；
2. 音频能够标准化为 16kHz mono；
3. Whisper 能输出 raw TXT；
4. 能输出 timestamp JSON 或 SRT；
5. raw transcript 永不被 clean stage 修改；
6. clean transcript 不允许总结或补充内容；
7. 专业术语支持 terminology normalization；
8. 所有运行生成 metadata；
9. source / raw / clean 都有 hash；
10. 同输入、同模型配置可以 cache；
11. 模型变化必须触发重新 transcription；
12. 词表变化只需要重新 clean；
13. 任意 stage failure 都必须生成明确 issue；
14. --raw-only 可以完全不使用 LLM；
15. 整个过程不需要任何 LLM API Key 来完成 Whisper transcription。

⸻

二十一、测试策略
至少准备三个 fixture。
Fixture A — 普通中文
30 秒。
验证：
基本中文识别
Fixture B — 中英技术混合
例如：
Flow-Encoding
L2a
SGE
BMAC
OPC
Fact Extraction
Workflow
验证：
terminology normalization
Fixture C — 模糊音频
包含：
低音量
停顿
含混词
验证：
不能偷偷猜
必须产生 ambiguity
另外测试：
不存在文件
错误格式
缺 ffmpeg
缺 model
重复执行
terminology changed

⸻

二十二、V2 再考虑 Speaker Diarization
V1 不建议做。
V2 可以增加：
Speaker 1
Speaker 2
Speaker 3
然后再允许用户手工 mapping：
{
  "Speaker 1": "晓梅",
  "Speaker 2": "团队成员A"
}
不要自动猜姓名。

⸻

二十三、V3 可以扩展成 Audio-as-Data Pipeline
到后面这个 Skill 可以不仅转写。
可以变成：
Audio
 ↓
Transcript
 ↓
Semantic Extraction
 ↓
Meeting Artifact
例如：
Decision
Issue
Action Item
Question
Finding
Risk
Claim
Evidence
但我建议一定让这一层独立于 transcript。
不要：
audio → meeting summary
而是：
Audio Truth
 ↓
Raw Transcript
 ↓
Clean Transcript
 ↓
Meeting Semantics
 ↓
Summary / Article
这样 lineage 才清楚。

⸻

二十四、推荐最终架构
                         audio-transcript
                               │
                               ▼
                        Input Validation
                               │
                               ▼
                           FFmpeg
                               │
                               ▼
                       normalized.wav
                               │
                               ▼
                         whisper.cpp
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
             raw.txt        raw.json        raw.srt
                │
                │ immutable
                ▼
        Terminology Normalization
                │
                ▼
          Transcript Cleaning
                │
                ▼
             clean.md
                │
        ┌───────┴────────┐
        ▼                ▼
   metadata.json      issues.json
        │
        ▼
      manifest
上面这一层完成以后，再允许其他 Skill：
meeting-summary
article-writer
semantic-extractor
SGE-review
消费 clean.md。

⸻

二十五、建议的实施顺序
我建议不要一次完成全部设计。
M0 — Environment
完成：
ffmpeg
whisper.cpp
model
只验证一条真实音频。
M1 — Raw Transcript
实现：
audio → normalized.wav → raw.txt/json/srt
这是第一个真正 Gate。
M2 — Artifact Governance
增加：
metadata
hash
issues
manifest
cache
M3 — Clean Transcript
增加：
terminology
cleaning rules
clean.md
M4 — Skill Packaging
再封装成：
audio-transcript Skill
M5 — Real Audio Validation
用你刚才那份 FlowE 回顾会音频跑一次完整 replay。
最后人工比较：
Audio
↔ Raw
↔ Clean
确认没有明显语义失真。

⸻

我建议 V1 冻结成这条能力边界
一句话定义就是：
audio-transcript V1 是一个 local-first、traceable、non-semantic-expansive 的 Audio → Raw Transcript → Clean Transcript pipeline。
其中最关键的三个设计原则是：
Raw 不可覆盖。
Clean 不得扩写。
Summary 与 Transcript 分轨。
如果这三个原则守住了，这个 Skill 后面无论接会议总结、文章创作、SGE 分析还是知识提取，都比较容易继续扩展，而不会从一开始就把“音频事实”和“AI解释”混在一起。
