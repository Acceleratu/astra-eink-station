# Astra A: estimated API cost of designing the board

**454.66 USD** at GPT-6 Astra Standard rates listed on November 15, 2026, assuming the same model and the same context reuse. This estimate covers electronics design through the first goal: 2,440 calls across the main agent and eight subagents. Enclosure design was a later goal. [Official GPT-6 Astra rates](https://developers.openai.com/api/docs/models/gpt-6-astra)

| Category | Tokens | USD per million | Estimated cost |
|---|---:|---:|---:|
| New inputs | 3,866,385 | 10.00 | 38.66 USD |
| Generated output, including reasoning | 952,948 | 50.00 | 47.65 USD |
| Cached input tokens | 368,347,392 | 1.00 | 368.35 USD |
| **Total** | **373,166,725** | | **454.66 USD** |

**The 4,819,333 tokens counted by the goal would cost 86.31 USD.** That count combines uncached input and generated output. The reuse of instructions, conversation history, and prior results explains the 368,347,392 cache reads. These represent 81.02% of the estimated cost. Out of the 952,948 output tokens, 279,656 are reasoning tokens and are already included in the 47.65 USD. Sessions recorded zero write tokens in cache, and the longest input had 245,316 tokens, below the 272,000 threshold for long context. [Processing and cache rates](https://developers.openai.com/api/docs/models/gpt-6-astra)

## Breakdown by activity

Each row includes that agent’s uncached input, cache reads and generated output. Activities are assigned by agent role. Per-row amounts are rounded to two decimal places.

| Activity | Calls | New tokens + output | Estimated cost with cache |
|---|---:|---:|---:|
| Coordination, integration into Fusion and delivery | 576 | 722,046 | 101.46 USD |
| Manufacturing, assembly and CAM checks | 304 | 582,193 | 57.81 USD |
| PCB placement and routing | 302 | 645,888 | 53.55 USD |
| Independent audit | 270 | 680,023 | 51.38 USD |
| Solar power, USB, and battery | 252 | 528,850 | 48.96 USD |
| E-paper display | 227 | 548,859 | 46.60 USD |
| Radio and antenna | 230 | 475,297 | 40.67 USD |
| Firmware | 148 | 281,471 | 28.00 USD |
| Wake-up, RTC and sensors | 131 | 354,706 | 26.22 USD |
| **Total** | **2,440** | **4,819,333** | **454.66 USD** |

The estimate covers tokens before VAT. Separately billed API tools can add per-call charges. [Tool pricing](https://developers.openai.com/api/docs/pricing#tools)
