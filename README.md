# 🖤 ZERO — BHRT Identity Stripping Engine v3.0

> **Remove personal identity from text. Preserve structure. Self-training AI core.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.9%2B-green)](https://python.org)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)](https://streamlit.io)

---

## What is ZERO?

ZERO is a **hybrid identity stripping engine** that combines:

- **Static Rule Engine** (regex, dictionaries, PII patterns)
- **Silent Learning System** (co-occurrence patterns, context rules)
- **ZERO Mind AI Core** (self-training neural system — no cloud, no API)

Unlike traditional anonymization tools that add noise or use generic placeholders, ZERO **learns from every strip** to make increasingly intelligent decisions about what to remove and what to preserve.

### Key Differentiators

| Feature | Traditional Tools | ZERO |
|---------|-------------------|------|
| Approach | Static rules / Noise injection | **Behavioral + AI** |
| Training | Pre-configured | **Self-training** |
| Cloud Dependency | Required | **Zero** |
| Hinglish Support | ❌ | **✅ Native** |
| Structure Preservation | Low-Medium | **High (AI-aware)** |
| Reversibility | Possible | **Impossible** |
| Code Size | 100K+ lines | **~2K lines** |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 3: ZERO MIND (AI Core)              │
│    Self-training neural module — learns from every strip     │
│    No external API, no cloud dependency, local evolution      │
├─────────────────────────────────────────────────────────────┤
│                 LAYER 2: BHRT ENGINE (Static + Learned)      │
│    Static rules + Silent learned patterns + Context rules    │
├─────────────────────────────────────────────────────────────┤
│                  LAYER 1: STRUCTURE PRESERVER                │
│    Semantic coherence, topic distribution, behavioral signal │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation

```bash
git clone https://github.com/yourusername/zero-bhrt.git
cd zero-bhrt
pip install -r requirements.txt
```

---

## Usage

### Streamlit UI

```bash
streamlit run app.py
```

### Python API

```python
from bhrt_engine_v3 import process

result = process("Main aaj bahut udaas hoon. Mera boss ne mujhe daanta.")

print(result.structure_text)
print(result.behavioral_pattern)
print(result.privacy_score)
print(result.zero_dissolved_text)  # AI-powered dissolution
```

### CLI

```bash
# Process text
python bhrt_engine_v3.py "Your text here"

# View stats
python bhrt_engine_v3.py --stats

# View ZERO Mind stats
python bhrt_engine_v3.py --zero-stats

# Export learned model
python bhrt_engine_v3.py --export-model
```

---

## How ZERO Mind Learns

1. **Correlation Mapping**: Tracks which non-identity words consistently appear near identity tokens
2. **Proxy Identity Detection**: Words that correlate strongly become flagged as "proxy identities"
3. **Replacement Scoring**: Every replacement strategy is scored by structure preservation
4. **Confidence Calibration**: High-scoring strategies are reused; low-scoring ones decay
5. **Structural Embeddings**: 64-dimensional position-aware embeddings for context understanding

All learning is **local** — no data leaves your machine.

---

## File Structure

```
zero-bhrt/
├── app.py                 # Streamlit UI (v3.0)
├── bhrt_engine_v3.py      # Main engine (Static + ZERO integration)
├── zero_mind.py           # AI Core (self-training neural system)
├── requirements.txt       # Dependencies
├── README.md             # This file
├── bhrt_memory.json      # BHRT learned patterns (auto-generated)
└── zero_mind.json        # ZERO Mind memory (auto-generated)
```

---

## Market Context

- **Differential Privacy Market**: $1.34B (2024) → $13B+ (2033)
- **Privacy-Preserving AI**: $39B by 2035
- **DPDP Act 2023**: India mandates data anonymization
- **Gap**: No existing tool handles behavioral identity + Hinglish + self-training

---

## License

Apache 2.0 — J.B.S. Mandloi

---

> *"Those who understand require no mention. Those who do not would not benefit from one."*
