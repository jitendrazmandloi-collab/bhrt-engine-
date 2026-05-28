# BHRT Identity Stripping Engine

> **"Pattern se identity hatao. Structure bachao."**

A privacy-preserving text processing engine that strips personal identity from any text while preserving its semantic structure and behavioral patterns. Built for researchers, privacy engineers, and structural analysts who need to work with text data without exposing who wrote it.

---

## What It Does

| Input | Output |
|-------|--------|
| "My name is Rajesh and I felt devastated yesterday" | `[PRONOUN] [PRONOUN] [EMOTION] [TEMPORAL_PERSONAL]` + structural analysis |

The engine guarantees:
- **Identity removal**: `I(Z;I) -> 0` (mathematically irreversible)
- **Structure preservation**: Semantic patterns, topics, and behavioral archetypes remain intact
- **One-way transformation**: Original identity CANNOT be recovered
- **Multilingual**: Supports English, Hindi, and Hinglish

---

## Installation

```bash
 github.com/yourusername/bhrt-engine.git  →  github.com/jitendrazmandloi-collab/bhrt-engine.git 
pip install -r requirements.txt
```

Or install directly:
```bash
pip install .
```

---

## Quick Start

### Python API

```python
from bhrt_engine import process, to_json

text = """
My name is Rajesh Kumar and I am 32 years old.
I work at a company in Mumbai.
Yesterday, I had a terrible meeting with my client.
"""

result = process(text)

# Print clean structure
print(result.structure_text)
# Output: "at a company in . had a with ."

# Print behavioral pattern
print(result.behavioral_pattern)
# Output: "CONFLICT_PROFESSIONAL"

# Full JSON
print(to_json(result))
```

### Command Line

```bash
# Demo mode
python bhrt_engine.py

# Process your own text
python bhrt_engine.py "Your text here with personal details"

# From file
python bhrt_engine.py < input.txt
```

---

## Output Format

```json
{
  "structure_text": "Clean text with no identity",
  "structure_tags": ["action:meeting", "domain:client"],
  "semantic_vector": {"action_meeting": 1, "domain_client": 1},
  "topic_distribution": {
    "professional": 0.6,
    "personal_emotion": 0.2,
    "logistical": 0.1,
    "financial": 0.1
  },
  "behavioral_pattern": "CONFLICT_PROFESSIONAL",
  "identity_tokens_found": 12,
  "identity_types_found": ["pronoun", "emotion", "name", "pii_location"],
  "pii_types_removed": ["location", "age"],
  "i_identity": 0.0,
  "i_pattern": 0.85,
  "i_noise": 0.02,
  "privacy_score": 85.0,
  "utility_score": 72.5,
  "bhrt_score": 80.2,
  "identity_hash": "a1b2c3d4...",
  "salt_destroyed": true,
  "vps_impossible": true,
  "processing_id": "uuid-here"
}
```

---

## Architecture

```
Input Text
    |
[Phase 1] Language Detection + Tokenization
    |
[Phase 2] Identity Detection (names, PII, emotions, pronouns)
    |
[Phase 3] Zenodo Projection (strip identity subspace)
    |
[Phase 4] Structure Extraction (semantic pattern)
    |
[Phase 5] Irreversibility Lock (HMAC + salt destruction)
    |
Output: {structure_vector, tags, metrics} -- NO identity recoverable
```

---

## Detected Identity Categories

| Category | Examples |
|----------|----------|
| **Pronouns** | I, me, my, main, mera, hum |
| **Emotions** | sad, angry, dukhi, gussa, devastated |
| **Names** | Rajesh Kumar, Mr. Sharma, Dr. Patel |
| **PII** | Phone, email, Aadhaar, PAN, location, age, money |
| **Subjective markers** | think, feel, believe, lagta, sochta |
| **Temporal personal** | today, yesterday, aaj, kal, abhi |

---

## Behavioral Patterns Detected

- `CONFLICT_PROFESSIONAL` -- Workplace disagreements, disputes
- `GROWTH_LEARNING` -- Skill development, courses, improvement
- `LEADERSHIP_EXECUTION` -- Team management, decision-making
- `CRISIS_MANAGEMENT` -- Urgent problem-solving, critical fixes
- `STAKEHOLDER_NEGOTIATION` -- Client deals, contract discussions
- `GENERAL_UNSTRUCTURED` -- No clear pattern detected

---

## Privacy Guarantees

1. **Irreversible**: HMAC with destroyed salt -- no reconstruction possible
2. **Verifiable**: `identity_hash` proves processing occurred
3. **Measurable**: `privacy_score` and `utility_score` quantify the trade-off
4. **One-way**: Original text cannot be derived from output

---

## Use Cases

- **Privacy-preserving NLP**: Train models on de-identified text
- **Behavioral research**: Study patterns without exposing individuals
- **HR Analytics**: Analyze employee feedback anonymously
- **Therapy/Coaching**: Strip client identity, retain structural insights
- **Data Marketplaces**: Sell structural insights, not personal data

---

## Contributing

This is a structural tool, not a personality. Issues and PRs welcome.

---

## Author

**J.B.S. Mandloi** -- Creator of the Black Heart structural framework

> *"This engine is not written to represent a person. It is written to remove one."*

:black_heart:

---

## License
Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright 2026 J.B.S. Mandloi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

(LICENSE) file.
