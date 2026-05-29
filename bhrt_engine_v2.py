"""
BHRT Identity Stripping Engine v2.0
====================================
Silent Self-Learning System

Features:
  1. Static Rules (pronouns, PII, names, emotions)
  2. Silent learned patterns from memory (no user awareness)
  3. Context-aware stripping
  4. Passive behavioral observation & adaptation
  5. Local evolution (no cloud)
"""

import re
import json
import hashlib
import hmac
import base64
import uuid
import math
import os
import time
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional

# ══════════════════════════════════════════════════════
#  MEMORY LOADER
# ══════════════════════════════════════════════════════

def load_memory() -> Dict:
    memory_path = os.path.join(os.path.dirname(__file__), 'bhrt_memory.json')
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "learned_words": {},
        "learned_patterns": {},
        "context_rules": {},
        "observation_log": [],
        "user_feedback": {"corrections": [], "total_processed": 0},
        "evolution_stats": {"started_with": 0, "current_total": 0, "total_processed": 0}
    }

def save_memory(memory: Dict):
    memory_path = os.path.join(os.path.dirname(__file__), 'bhrt_memory.json')
    with open(memory_path, 'w', encoding='utf-8') as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# ══════════════════════════════════════════════════════
#  CONSTANTS
# ══════════════════════════════════════════════════════

PERSONAL_PRONOUNS = {
    'en': {'i','me','my','mine','myself','we','our','ours','ourselves',
           'you','your','yours','he','him','his','she','her','hers',
           'they','them','their','theirs'},
    'hi': {'main','mujhe','mera','meri','mere','hum','hamara','hamari',
           'hamare','aap','apka','apki','apke','tum','tumhara','tumhari',
           'vo','voh','uska','uski','unka','unki','mai','apna','apni'},
}

EMOTION_VOCAB = {
    'negative': {
        'en': {'devastated','sad','depressed','angry','frustrated','scared','worried',
               'anxious','ashamed','guilty','horrible','terrible','awful','bad',
               'failed','failure','mistake','regret','pain','hurt','cry','hate',
               'fear','afraid','nervous','upset','disappointed','hopeless'},
        'hi': {'dukhi','pareshan','gussa','dara','chinta','takleef','bura','ghabra',
               'udaas','thaka','hurt','naaraz','sharminda','darr','dard','rona',
               'nafrat','bewafa','toota','broken','lose','haara','haar'}
    },
    'positive': {
        'en': {'happy','joy','love','proud','excited','amazing','wonderful',
               'great','excellent','fantastic','brilliant','good','best'},
        'hi': {'khush','mast','accha','badhiya','shukriya','pyaar','mazaa'}
    }
}

SUBJECTIVE_MARKERS = {
    'en': {'think','feel','believe','seems','probably','maybe','perhaps',
           'guess','suppose','assume','hope','wish','want','need','should',
           'could','would','might','opinion','personally','honestly','literally'},
    'hi': {'lagta','sochta','samajhta','laga','lagti','sochti','chahta',
           'chahti','umeed','shayad','lage','lagey','mujhe lagta','main sochta'}
}

TEMPORAL_PERSONAL = {
    'en': {'today','yesterday','tomorrow','tonight','now','currently','recently',
           'lately','always','never','sometimes','often','already','yet','still'},
    'hi': {'aaj','kal','parso','abhi','filhaal','abhi tak','pehle','baad mein',
           'hamesha','kabhi','aksar','pehle se','abhi bhi'}
}

NAME_PATTERNS = [
    r'\b[A-Z][a-z]{2,15}\s[A-Z][a-z]{2,15}\b',
    r'\b[A-Z][a-z]{2,15}\b(?=\s+(?:from|said|told|wrote|is|was|has|had|will))',
    r'\bMr\.?\s+[A-Z][a-z]+\b',
    r'\bMrs\.?\s+[A-Z][a-z]+\b',
    r'\bMs\.?\s+[A-Z][a-z]+\b',
    r'\bDr\.?\s+[A-Z][a-z]+\b',
]

PII_PATTERNS = {
    'phone':    r'\b(?:\+91|0)?[6-9]\d{9}\b|\b\d{3}[-.\\s]?\d{3}[-.\\s]?\d{4}\b',
    'email':    r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b',
    'location': r'\b(?:Mumbai|Delhi|Bangalore|Chennai|Kolkata|Hyderabad|Pune|'
                r'Ahmedabad|Jaipur|Lucknow|Kanpur|Nagpur|Indore|Bhopal|'
                r'New York|London|Paris|Tokyo|Dubai|Singapore)\b',
    'age':      r'\b(?:age|aged|years?\s+old|saal\s+ka|saal\s+ki)\s*:?\s*\d+\b',
    'money':    r'₹\s*[\d,]+|Rs\.?\s*[\d,]+|\$\s*[\d,]+',
    'aadhaar':  r'\b\d{4}\s?\d{4}\s?\d{4}\b',
    'pan':      r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
}

STRUCTURE_INDICATORS = {
    'action_verbs': {'meeting','discuss','present','deliver','complete','build',
                     'create','develop','launch','execute','manage','lead',
                     'propose','review','approve','reject','submit','report'},
    'quantifiers':  {'months','weeks','days','hours','percent','members','team',
                     'projects','tasks','items','phases','steps','stages'},
    'domain_words': {'project','career','business','strategy','deadline','budget',
                     'target','goal','milestone','client','product','service',
                     'revenue','performance','quality','process','system'}
}

BEHAVIORAL_PATTERNS = {
    'CONFLICT_PROFESSIONAL': ['conflict','disagree','argue','dispute','professional','work','colleague'],
    'GROWTH_LEARNING': ['learn','improve','grow','skill','course','training','certificate'],
    'LEADERSHIP_EXECUTION': ['lead','team','manage','decision','responsibility','drive'],
    'CRISIS_MANAGEMENT': ['crisis','urgent','emergency','fix','resolve','critical'],
    'STAKEHOLDER_NEGOTIATION': ['negotiate','client','stakeholder','deal','contract','agreement'],
    'TRAUMA_NARRATIVE': ['bhag','bhagna','darr','dar','marna','maar','sex','bhalu'],
    'RELATIONSHIP_INTIMATE': ['gf','bf','pyaar','love','kiss','wife','husband'],
    'EXPLICIT_CONTENT': ['sex','chudai','kiss','fuck','chod'],
}

# ══════════════════════════════════════════════════════
#  DATA STRUCTURES
# ══════════════════════════════════════════════════════

@dataclass
class IdentityToken:
    token: str
    category: str
    position: int
    confidence: float
    lang: str
    source: str = "static"

@dataclass
class ZenodoOutput:
    structure_text: str
    structure_tags: List[str]
    semantic_vector: Dict
    topic_distribution: Dict
    behavioral_pattern: str
    identity_tokens_found: int
    identity_types_found: List[str]
    pii_types_removed: List[str]
    i_identity: float
    i_pattern: float
    i_noise: float
    privacy_score: float
    utility_score: float
    bhrt_score: float
    identity_hash: str
    salt_destroyed: bool
    vps_impossible: bool
    processing_id: str
    input_length: int
    output_length: int
    language_detected: str
    timestamp: float
    learned_words_used: int = 0
    context_rules_triggered: List[str] = field(default_factory=list)

# ══════════════════════════════════════════════════════
#  PHASE 1: TOKENIZER + LANGUAGE DETECTION
# ══════════════════════════════════════════════════════

def detect_language(text: str) -> str:
    hindi_chars = len(re.findall(r'[ऀ-ॿ]', text))
    hinglish_markers = len(re.findall(
        r'\b(hai|tha|thi|hain|kya|nahi|nhi|ko|ka|ki|ke|se|mein|pe|par|aur|lekin|phir|toh|bhi|hi|sirf|bahut|accha|badhiya)\b',
        text, re.IGNORECASE))
    total = len(text.split())
    if hindi_chars > 5:
        return 'hi'
    elif hinglish_markers / max(total, 1) > 0.1:
        return 'hinglish'
    return 'en'

def tokenize(text: str) -> List[Tuple[str, int]]:
    tokens = []
    for i, match in enumerate(re.finditer(r'\S+', text)):
        tokens.append((match.group(), i))
    return tokens

# ══════════════════════════════════════════════════════
#  PHASE 2: IDENTITY DETECTION (Static + Learned)
# ══════════════════════════════════════════════════════

def detect_identity_tokens(text: str, lang: str, memory: Dict) -> List[IdentityToken]:
    found = []
    text_lower = text.lower()
    tokens_with_pos = tokenize(text)
    learned_words = memory.get("learned_words", {})
    learned_patterns = memory.get("learned_patterns", {})

    all_pronouns = PERSONAL_PRONOUNS.get('en', set()) | PERSONAL_PRONOUNS.get('hi', set())
    for token, pos in tokens_with_pos:
        clean = re.sub(r'[^\wऀ-ॿ]', '', token).lower()
        if clean in all_pronouns:
            found.append(IdentityToken(token, 'pronoun', pos, 0.99, lang, "static"))

    all_emotions = set()
    for valence in EMOTION_VOCAB.values():
        for l_vocab in valence.values():
            all_emotions |= l_vocab
    for token, pos in tokens_with_pos:
        clean = re.sub(r'[^\wऀ-ॿ]', '', token).lower()
        if clean in all_emotions:
            found.append(IdentityToken(token, 'emotion', pos, 0.95, lang, "static"))

    all_subj = SUBJECTIVE_MARKERS.get('en', set()) | SUBJECTIVE_MARKERS.get('hi', set())
    for token, pos in tokens_with_pos:
        clean = re.sub(r'[^\wऀ-ॿ]', '', token).lower()
        if clean in all_subj:
            found.append(IdentityToken(token, 'subjective', pos, 0.85, lang, "static"))

    all_temporal = TEMPORAL_PERSONAL.get('en', set()) | TEMPORAL_PERSONAL.get('hi', set())
    for token, pos in tokens_with_pos:
        clean = re.sub(r'[^\wऀ-ॿ]', '', token).lower()
        if clean in all_temporal:
            found.append(IdentityToken(token, 'temporal_personal', pos, 0.70, lang, "static"))

    for pattern in NAME_PATTERNS:
        for match in re.finditer(pattern, text):
            found.append(IdentityToken(match.group(), 'name', -1, 0.80, lang, "static"))

    for pii_type, pattern in PII_PATTERNS.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            found.append(IdentityToken(match.group(), f'pii_{pii_type}', -1, 0.99, lang, "static"))

    # Silent learned word application
    for token, pos in tokens_with_pos:
        clean = re.sub(r'[^\wऀ-ॿ]', '', token).lower()
        if clean in learned_words:
            word_info = learned_words[clean]
            if word_info.get("confidence", 0) >= 0.75:
                found.append(IdentityToken(token, word_info.get("category", "identity"), pos, word_info["confidence"], lang, "learned"))

    for pattern_key, pattern_info in learned_patterns.items():
        parts = pattern_key.split(' + ')
        if len(parts) == 2:
            if parts[1] == '*':
                word = parts[0]
                if word in text_lower:
                    for match in re.finditer(r'\b' + re.escape(word) + r'\b', text_lower):
                        found.append(IdentityToken(
                            text[match.start():match.end()],
                            pattern_info.get("category", "learned_pattern"),
                            -1, pattern_info.get("confidence", 0.8), lang, "learned_pattern"))
            else:
                if parts[0] in text_lower and parts[1] in text_lower:
                    for match in re.finditer(r'\b' + re.escape(parts[0]) + r'\b', text_lower):
                        found.append(IdentityToken(
                            text[match.start():match.end()],
                            pattern_info.get("category", "learned_pattern"),
                            -1, pattern_info.get("confidence", 0.8), lang, "learned_pattern"))

    seen = set()
    unique = []
    for it in found:
        key = (it.position, it.token.lower(), it.category)
        if key not in seen:
            seen.add(key)
            unique.append(it)

    return unique

# ══════════════════════════════════════════════════════
#  PHASE 3: CONTEXT-AWARE RULES
# ══════════════════════════════════════════════════════

def apply_context_rules(text: str, identity_tokens: List[IdentityToken], memory: Dict) -> Tuple[List[IdentityToken], List[str]]:
    context_rules = memory.get("context_rules", {})
    triggered_rules = []
    categories_present = set(it.category for it in identity_tokens)

    for rule_name, rule_info in context_rules.items():
        parts = rule_name.split(' + ')
        if len(parts) == 2:
            cat1, cat2 = parts[0], parts[1]
            if cat1 in categories_present:
                if cat2 == '*' or cat2 in categories_present:
                    triggered_rules.append(rule_name)

    return identity_tokens, triggered_rules

# ══════════════════════════════════════════════════════
#  PHASE 4: ZENODO PROJECTION
# ══════════════════════════════════════════════════════

def zenodo_projection(text: str, identity_tokens: List[IdentityToken], triggered_rules: List[str]) -> str:
    result = text
    token_to_category = {}
    for ident in identity_tokens:
        if ident.position >= 0:
            clean = re.sub(r'[^\wऀ-ॿ]', '', ident.token).lower()
            if clean:
                token_to_category[clean] = ident.category

    def replace_word_token(match):
        full_token = match.group(0)
        core = re.sub(r'[^\wऀ-ॿ]', '', full_token).lower()
        cat = token_to_category.get(core)
        if cat:
            return f'[{cat.upper()}]'
        return full_token

    result = re.sub(r"[\wऀ-ॿ]+(?:[''][\wऀ-ॿ]+)?", replace_word_token, result)

    pattern_idents = [(it.token, it.category) for it in identity_tokens if it.position < 0]
    seen_patterns = set()
    unique_patterns = []
    for token, cat in sorted(pattern_idents, key=lambda x: -len(x[0])):
        key = (token.lower(), cat)
        if key not in seen_patterns:
            seen_patterns.add(key)
            unique_patterns.append((token, cat))

    for token, cat in unique_patterns:
        result = re.sub(re.escape(token), f'[{cat.upper()}]', result, flags=re.IGNORECASE)

    if any('full_redact' in rule for rule in triggered_rules):
        result = re.sub(r'\b(?:ghum|ghoomna|picnic|mall|park)\b', '[ACTIVITY]', result, flags=re.IGNORECASE)
        result = re.sub(r'\b(?:bhalu|sher|kutta|billi)\b', '[ANIMAL]', result, flags=re.IGNORECASE)

    return result

# ══════════════════════════════════════════════════════
#  PHASE 5: STRUCTURE EXTRACTION
# ══════════════════════════════════════════════════════

def extract_structure(stripped_text: str, original_text: str, lang: str) -> Tuple[str, List[str], Dict, Dict, str]:
    tokens = [t for t, _ in tokenize(stripped_text.lower())]
    clean_tokens = [t for t in tokens if not (t.startswith('[') and t.endswith(']'))]

    tags = []
    semantic_vector = Counter()

    for token in clean_tokens:
        if token in STRUCTURE_INDICATORS['action_verbs']:
            tags.append(f'action:{token}')
            semantic_vector[f'action_{token}'] += 1
        if token in STRUCTURE_INDICATORS['quantifiers']:
            tags.append(f'quant:{token}')
            semantic_vector[f'quant_{token}'] += 1
        if token in STRUCTURE_INDICATORS['domain_words']:
            tags.append(f'domain:{token}')
            semantic_vector[f'domain_{token}'] += 1

    topic_distribution = {
        'professional': 0, 'personal_emotion': 0, 'logistical': 0,
        'financial': 0, 'trauma': 0, 'relationship': 0,
    }

    prof_words = {'project','career','business','strategy','deadline','client','meeting','team','lead','manage'}
    emotion_words = set()
    for v in EMOTION_VOCAB.values():
        for vocab in v.values():
            emotion_words |= vocab
    log_words = {'schedule','plan','timeline','process','system','step','phase'}
    fin_words = {'budget','revenue','cost','price','money','financial','₹','rs','$'}
    trauma_words = {'bhag','bhagna','darr','dar','marna','maar','sex','chudai'}
    rel_words = {'gf','bf','pyaar','love','kiss','wife','husband','dost','yaar'}

    for token in clean_tokens:
        if token in prof_words: topic_distribution['professional'] += 1
        if token in emotion_words: topic_distribution['personal_emotion'] += 1
        if token in log_words: topic_distribution['logistical'] += 1
        if token in fin_words: topic_distribution['financial'] += 1
        if token in trauma_words: topic_distribution['trauma'] += 1
        if token in rel_words: topic_distribution['relationship'] += 1

    total_topics = sum(topic_distribution.values())
    if total_topics > 0:
        topic_distribution = {k: round(v / total_topics, 3) for k, v in topic_distribution.items()}

    pattern_scores = {}
    for pattern_name, keywords in BEHAVIORAL_PATTERNS.items():
        score = sum(1 for kw in keywords if kw in clean_tokens)
        pattern_scores[pattern_name] = score

    best_pattern = max(pattern_scores, key=pattern_scores.get) if max(pattern_scores.values()) > 0 else 'GENERAL_UNSTRUCTURED'

    clean_text = re.sub(r'\[[A-Z_]+\]', '', stripped_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text, list(set(tags)), dict(semantic_vector), topic_distribution, best_pattern

# ══════════════════════════════════════════════════════
#  PHASE 6: IRREVERSIBILITY LOCK
# ══════════════════════════════════════════════════════

def irreversibility_lock(identity_tokens: List[IdentityToken]) -> Tuple[str, bool, bool, str]:
    processing_id = str(uuid.uuid4())
    identity_payload = json.dumps([
        {'token': it.token, 'category': it.category, 'lang': it.lang, 'source': it.source}
        for it in sorted(identity_tokens, key=lambda x: x.token)
    ], sort_keys=True)

    salt = os.urandom(32)
    identity_hash = hmac.new(salt, identity_payload.encode('utf-8'), hashlib.sha256).hexdigest()

    return identity_hash, True, True, processing_id

# ══════════════════════════════════════════════════════
#  PHASE 7: SILENT LEARNING ENGINE
# ══════════════════════════════════════════════════════

def _silent_learn(text: str, identity_tokens: List[IdentityToken], lang: str, memory: Dict) -> Dict:
    """
    Silently observe and evolve — no user-facing indication this is happening.
    Learns co-occurrence patterns, frequency boosts, and context upgrades.
    """
    learned_words = memory.setdefault("learned_words", {})
    learned_patterns = memory.setdefault("learned_patterns", {})
    observation_log = memory.setdefault("observation_log", [])

    tokens_lower = [re.sub(r'[^\wऀ-ॿ]', '', t).lower() for t, _ in tokenize(text)]

    # 1. Boost confidence for known learned words seen again
    for token in identity_tokens:
        if token.source == "learned":
            clean = re.sub(r'[^\wऀ-ॿ]', '', token.token).lower()
            if clean in learned_words:
                learned_words[clean]["seen"] = learned_words[clean].get("seen", 0) + 1
                learned_words[clean]["confidence"] = min(0.99, learned_words[clean].get("confidence", 0.8) + 0.002)

    # 2. Detect new co-occurrence patterns silently
    identity_set = set(re.sub(r'[^\wऀ-ॿ]', '', t.token).lower() for t in identity_tokens)
    non_identity = [t for t in tokens_lower if t and t not in identity_set and len(t) > 3]

    for ni_token in non_identity:
        # Check if this word appears near identity tokens repeatedly
        pattern_key = f"{ni_token} + *"
        if pattern_key in learned_patterns:
            learned_patterns[pattern_key]["seen"] = learned_patterns[pattern_key].get("seen", 0) + 1
            if learned_patterns[pattern_key]["seen"] >= 3:
                learned_patterns[pattern_key]["confidence"] = min(0.95, learned_patterns[pattern_key].get("confidence", 0.6) + 0.05)
        else:
            # Only log if it appears context-suspicious
            # (adjacent to known identity tokens)
            for it in identity_tokens:
                it_clean = re.sub(r'[^\wऀ-ॿ]', '', it.token).lower()
                if it_clean in tokens_lower and ni_token in tokens_lower:
                    it_idx = tokens_lower.index(it_clean) if it_clean in tokens_lower else -1
                    ni_idx = tokens_lower.index(ni_token) if ni_token in tokens_lower else -1
                    if it_idx >= 0 and ni_idx >= 0 and abs(it_idx - ni_idx) <= 3:
                        # Close proximity — candidate for learning
                        obs_key = f"{ni_token}|{it.category}"
                        obs_count = sum(1 for o in observation_log if o.get("key") == obs_key)
                        if obs_count >= 2:
                            # Seen enough times — graduate to learned
                            learned_words[ni_token] = {
                                "category": it.category,
                                "confidence": 0.72,
                                "seen": obs_count + 1,
                                "lang": lang,
                                "added_by": "silent_observation"
                            }
                        else:
                            observation_log.append({
                                "key": obs_key,
                                "word": ni_token,
                                "near_category": it.category,
                                "ts": time.time()
                            })

    # Trim log to last 500 observations
    if len(observation_log) > 500:
        memory["observation_log"] = observation_log[-500:]

    memory["evolution_stats"]["total_processed"] = memory["evolution_stats"].get("total_processed", 0) + 1
    memory["evolution_stats"]["current_total"] = len(learned_words)

    return memory

# ══════════════════════════════════════════════════════
#  FEEDBACK API (internal — not shown in UI)
# ══════════════════════════════════════════════════════

def _internal_add_word(word: str, category: str, memory: Dict) -> Dict:
    """Internal method to inject known words. Not exposed in UI."""
    learned_words = memory.setdefault("learned_words", {})
    clean = re.sub(r'[^\wऀ-ॿ]', '', word).lower()
    if clean:
        if clean in learned_words:
            learned_words[clean]["confidence"] = min(0.99, learned_words[clean]["confidence"] + 0.05)
            learned_words[clean]["seen"] += 1
        else:
            learned_words[clean] = {
                "category": category,
                "confidence": 0.90,
                "seen": 1,
                "lang": "hinglish",
                "added_by": "internal"
            }
    return memory

# ══════════════════════════════════════════════════════
#  METRICS
# ══════════════════════════════════════════════════════

def calculate_metrics(
    original_text: str, stripped_text: str, clean_text: str,
    identity_tokens: List[IdentityToken], semantic_vector: Dict
) -> Tuple[float, float, float, float, float, float]:
    orig_len = len(original_text.split())
    out_len = len(clean_text.split())
    ident_count = len(identity_tokens)

    i_identity = max(0.0, 1.0 - (ident_count / max(orig_len, 1)) * 2)
    if i_identity > 1:
        i_identity = 0.0

    structure_density = len(semantic_vector) / max(out_len, 1)
    i_pattern = min(1.0, structure_density * 5)

    i_noise = abs(orig_len - out_len) / max(orig_len, 1) * 0.5

    pii_types = set(it.category for it in identity_tokens if it.category.startswith('pii_'))
    privacy_score = min(100, (ident_count * 10) + (len(pii_types) * 15))
    if privacy_score < 30:
        privacy_score = 30

    utility_score = max(0, 100 - privacy_score * 0.3 - i_noise * 20)
    bhrt_score = (privacy_score * 0.5 + utility_score * 0.4 + (1 - i_noise) * 10)

    return (
        round(i_identity, 4), round(i_pattern, 4), round(i_noise, 4),
        round(privacy_score, 2), round(utility_score, 2), round(bhrt_score, 2)
    )

# ══════════════════════════════════════════════════════
#  MAIN PIPELINE
# ══════════════════════════════════════════════════════

def process(text: str, learn: bool = True) -> ZenodoOutput:
    timestamp = time.time()
    memory = load_memory()

    lang = detect_language(text)
    identity_tokens = detect_identity_tokens(text, lang, memory)
    identity_tokens, triggered_rules = apply_context_rules(text, identity_tokens, memory)
    stripped_text = zenodo_projection(text, identity_tokens, triggered_rules)
    clean_text, tags, semantic_vector, topic_dist, behavior = extract_structure(stripped_text, text, lang)
    identity_hash, salt_destroyed, vps_impossible, processing_id = irreversibility_lock(identity_tokens)

    if learn:
        memory = _silent_learn(text, identity_tokens, lang, memory)
        save_memory(memory)

    i_identity, i_pattern, i_noise, privacy_score, utility_score, bhrt_score = calculate_metrics(
        text, stripped_text, clean_text, identity_tokens, semantic_vector
    )

    pii_types = list(set(
        it.category.replace('pii_', '')
        for it in identity_tokens if it.category.startswith('pii_')
    ))
    identity_types = list(set(it.category for it in identity_tokens))
    learned_count = sum(1 for it in identity_tokens if it.source in ("learned", "learned_pattern"))

    return ZenodoOutput(
        structure_text=clean_text,
        structure_tags=tags,
        semantic_vector=semantic_vector,
        topic_distribution=topic_dist,
        behavioral_pattern=behavior,
        identity_tokens_found=len(identity_tokens),
        identity_types_found=identity_types,
        pii_types_removed=pii_types,
        i_identity=i_identity,
        i_pattern=i_pattern,
        i_noise=i_noise,
        privacy_score=privacy_score,
        utility_score=utility_score,
        bhrt_score=bhrt_score,
        identity_hash=identity_hash,
        salt_destroyed=salt_destroyed,
        vps_impossible=vps_impossible,
        processing_id=processing_id,
        input_length=len(text.split()),
        output_length=len(clean_text.split()),
        language_detected=lang,
        timestamp=timestamp,
        learned_words_used=learned_count,
        context_rules_triggered=triggered_rules,
    )

def to_json(output: ZenodoOutput) -> str:
    return json.dumps(asdict(output), indent=2, ensure_ascii=False, default=str)

def get_memory_stats() -> Dict:
    memory = load_memory()
    return {
        "learned_words": len(memory.get("learned_words", {})),
        "learned_patterns": len(memory.get("learned_patterns", {})),
        "context_rules": len(memory.get("context_rules", {})),
        "total_processed": memory.get("evolution_stats", {}).get("total_processed", 0),
        "version": memory.get("version", "2.0"),
    }

# ══════════════════════════════════════════════════════
#  CLI
# ══════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys

    demo_text = """
    Me or meri gf dono sath me ghum rahe the or or ek bhalu dikh gya 
    jo sex kre the vo bhi bhalu hum bhag gye fir
    """

    print("=" * 70)
    print("  BHRT Identity Stripping Engine v2.0")
    print("=" * 70)

    if len(sys.argv) > 1:
        if sys.argv[1] in ('-h', '--help'):
            print("""
Usage: python bhrt_engine_v2.py ["your text here"]
       python bhrt_engine_v2.py --stats
            """)
            sys.exit(0)
        elif sys.argv[1] == '--stats':
            print(json.dumps(get_memory_stats(), indent=2))
            sys.exit(0)
        input_text = ' '.join(sys.argv[1:])
    else:
        input_text = demo_text
        print("\n  [DEMO MODE]\n")

    result = process(input_text)
    print(f"Structure Text : {result.structure_text}")
    print(f"Pattern        : {result.behavioral_pattern}")
    print(f"Privacy Score  : {result.privacy_score}")
    print(f"BHRT Score     : {result.bhrt_score}")
    print(to_json(result))
