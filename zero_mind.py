"""
ZERO Mind — Self-Training Identity Dissolution Network
=======================================================
No pre-trained models. No external APIs. Pure structural learning.

Core Philosophy:
  - Identity is not just PII — it is behavioral fingerprint
  - Every strip teaches the system something new
  - Structure preservation > identity removal (both must happen)
  - Local evolution, zero cloud dependency

Architecture:
  1. Structural Embedding Engine (positional + co-occurrence + syntactic)
  2. Identity Dissolution Network (context-aware replacement generation)
  3. Pattern Discovery System (proxy identity detection)
  4. Self-Training Loop (decision memory + confidence calibration)
  5. Evolution Report Engine (training metrics + growth visualization)

Author: J.B.S. Mandloi
Version: zero-1.0
License: Apache 2.0
"""

import re
import json
import math
import os
import time
import random
import hashlib
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field, asdict

import numpy as np

# ══════════════════════════════════════════════════════
#  CONFIGURATION
# ══════════════════════════════════════════════════════

ZERO_CONFIG = {
    "embedding_dim": 64,
    "context_window": 5,
    "learning_rate": 0.01,
    "confidence_threshold": 0.72,
    "proxy_discovery_threshold": 5,
    "max_decision_memory": 5000,
    "max_correlation_entries": 10000,
    "decay_factor": 0.995,
    "structure_weight": 0.6,
    "topic_weight": 0.4,
    "min_token_length": 3,
    "hindi_range": (2304, 2431),
}

# ══════════════════════════════════════════════════════
#  DATA STRUCTURES
# ══════════════════════════════════════════════════════

@dataclass
class ZeroDecision:
    original: str
    replacement: str
    category: str
    confidence: float
    strategy: str
    context_hash: str
    structure_score: float
    timestamp: float

@dataclass
class ZeroEvolution:
    total_processed: int
    total_decisions: int
    avg_confidence: float
    avg_structure_score: float
    proxy_identities_found: int
    new_patterns_this_session: int
    learning_velocity: float
    memory_size_kb: float
    version: str = "zero-1.0"

@dataclass
class ZeroResult:
    dissolved_text: str
    decisions: List[ZeroDecision]
    structure_score: float
    identity_score: float
    topic_distribution: Dict[str, float]
    behavioral_pattern: str
    evolution: ZeroEvolution
    processing_id: str


# ══════════════════════════════════════════════════════
#  ZERO MIND CORE
# ══════════════════════════════════════════════════════

class ZeroMind:
    """
    Self-training neural system for identity dissolution.

    No external dependencies beyond numpy.
    Learns locally from every text processed.
    """

    def __init__(self, memory_path: str = "zero_mind.json"):
        self.memory_path = memory_path
        self.config = ZERO_CONFIG

        # Memory banks
        self.decision_memory: Dict[str, dict] = {}
        self.correlation_map: Dict[str, Dict[str, int]] = defaultdict(dict)
        self.proxy_identities: Dict[str, dict] = {}
        self.replacement_memory: Dict[str, List[dict]] = {}
        self.structural_embeddings: Dict[str, List[float]] = {}
        self.session_stats = {
            "processed": 0,
            "decisions": 0,
            "new_patterns": 0,
            "confidence_sum": 0.0,
            "structure_sum": 0.0,
        }

        self._load()

    # ── Persistence ───────────────────────────────────

    def _load(self):
        if not os.path.exists(self.memory_path):
            return
        try:
            with open(self.memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.decision_memory = data.get('decisions', {})
            self.correlation_map = defaultdict(dict, data.get('correlations', {}))
            self.proxy_identities = data.get('proxies', {})
            self.replacement_memory = data.get('replacements', {})
            self.structural_embeddings = data.get('embeddings', {})
            # Decay old correlations on load
            self._decay_correlations()
        except Exception:
            pass

    def save(self):
        """Persist all learning to disk."""
        data = {
            'decisions': self._trim_decisions(),
            'correlations': dict(self.correlation_map),
            'proxies': self.proxy_identities,
            'replacements': self._trim_replacements(),
            'embeddings': self._trim_embeddings(),
            'total_processed': self.session_stats["processed"] + 
                               sum(d.get('count', 0) for d in self.decision_memory.values()),
            'version': 'zero-1.0',
            'last_saved': time.time(),
        }
        with open(self.memory_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _trim_decisions(self) -> Dict:
        if len(self.decision_memory) > self.config["max_decision_memory"]:
            # Keep highest-confidence decisions, trim oldest low-confidence
            sorted_items = sorted(
                self.decision_memory.items(),
                key=lambda x: (x[1].get('avg_structure_score', 0), x[1].get('count', 0)),
                reverse=True
            )
            return dict(sorted_items[:self.config["max_decision_memory"]])
        return self.decision_memory

    def _trim_replacements(self) -> Dict:
        trimmed = {}
        for k, v in self.replacement_memory.items():
            # Keep top 3 replacements per context
            sorted_v = sorted(v, key=lambda x: x.get('score', 0), reverse=True)
            trimmed[k] = sorted_v[:3]
        return trimmed

    def _trim_embeddings(self) -> Dict:
        # Keep embeddings for proxy identities + high-frequency tokens
        keep_tokens = set(self.proxy_identities.keys())
        for token, data in self.decision_memory.items():
            if data.get('count', 0) > 3:
                keep_tokens.add(token.split('|')[0])
        return {k: v for k, v in self.structural_embeddings.items() if k in keep_tokens}

    def _decay_correlations(self):
        """Gradually forget old correlations to prevent stale learning."""
        decay = self.config["decay_factor"]
        for token, corr in list(self.correlation_map.items()):
            for rem, count in list(corr.items()):
                new_count = int(count * decay)
                if new_count < 2:
                    del corr[rem]
                else:
                    corr[rem] = new_count
            if not corr:
                del self.correlation_map[token]

    # ── Tokenization & Language ───────────────────────

    def _tokenize(self, text: str) -> List[str]:
        """Language-aware tokenization."""
        # Handle Hindi + Hinglish + English
        tokens = re.findall(r"[\w\u0900-\u097F]+(?:['’][\w\u0900-\u097F]+)?", text)
        return tokens

    def _clean_token(self, token: str) -> str:
        return re.sub(r"[^\w\u0900-\u097F]", "", token).lower()

    def _is_hindi(self, token: str) -> bool:
        return any(ord(c) in range(2304, 2432) for c in token)

    # ── Structural Embedding Engine ───────────────────

    def _structural_embed(self, token: str, context: List[str], position: int) -> np.ndarray:
        """
        Create 64-dim structural embedding:
        - Position encoding (8 dims)
        - Co-occurrence fingerprint (32 dims)
        - Syntactic role vector (16 dims)
        - Frequency signature (8 dims)
        """
        # Position encoding (sinusoidal, like Transformers but tiny)
        pos_vec = self._position_encode(position, 8)

        # Co-occurrence with known structural words
        cooc_vec = self._cooccurrence_vector(token, context, 32)

        # Syntactic role detection
        role_vec = self._syntactic_role(token, context, position, 16)

        # Frequency in corpus
        freq_vec = self._frequency_signature(token, 8)

        return np.concatenate([pos_vec, cooc_vec, role_vec, freq_vec])

    def _position_encode(self, position: int, dim: int) -> np.ndarray:
        """Sinusoidal position encoding."""
        vec = np.zeros(dim)
        for i in range(dim):
            freq = 1.0 / (10000 ** (i / dim))
            if i % 2 == 0:
                vec[i] = math.sin(position * freq)
            else:
                vec[i] = math.cos(position * freq)
        return vec

    def _cooccurrence_vector(self, token: str, context: List[str], dim: int) -> np.ndarray:
        """What structural words co-occur with this token?"""
        vec = np.zeros(dim)
        structural_words = {
            'action': ['meeting', 'discuss', 'present', 'deliver', 'complete', 'build',
                      'create', 'develop', 'launch', 'execute', 'manage', 'lead',
                      'propose', 'review', 'approve', 'reject', 'submit', 'report',
                      'kiya', 'kari', 'kare', 'banaya', 'bheja', 'likha'],
            'quantifier': ['months', 'weeks', 'days', 'hours', 'percent', 'members',
                          'team', 'projects', 'tasks', 'items', 'phases', 'steps',
                          'mahine', 'din', 'ghante', 'percent', 'log'],
            'domain': ['project', 'career', 'business', 'strategy', 'deadline', 'budget',
                      'target', 'goal', 'milestone', 'client', 'product', 'service',
                      'revenue', 'performance', 'quality', 'process', 'system',
                      'kaam', 'naukri', 'business', 'target', 'budget'],
            'relation': ['boss', 'manager', 'client', 'team', 'colleague', 'friend',
                        'boss', 'manager', 'client', 'team', 'dost', 'yaar'],
            'emotion': ['happy', 'sad', 'angry', 'worried', 'excited', 'frustrated',
                       'khush', 'udaas', 'gussa', 'chinta', 'takleef'],
        }

        clean_context = [self._clean_token(t) for t in context]
        idx = 0
        for category, words in structural_words.items():
            score = sum(1 for w in words if w in clean_context) / max(len(clean_context), 1)
            vec[idx] = score
            idx += 1
            if idx >= dim:
                break

        # Fill remaining with proximity-weighted random for uniqueness
        for i in range(idx, dim):
            vec[i] = random.gauss(0, 0.01)

        return vec

    def _syntactic_role(self, token: str, context: List[str], position: int, dim: int) -> np.ndarray:
        """Detect grammatical role: Agent, Subject, Object, Modifier."""
        vec = np.zeros(dim)
        clean = self._clean_token(token)

        # Agent detection (sentence start, capitalized in English)
        if position == 0:
            vec[0] = 1.0  # Agent

        # Subject markers (Hinglish: ne, ki, ka, ko, se)
        subj_markers = {'ne', 'ki', 'ka', 'ko', 'se', 'ne', 'ki', 'ka'}
        if position > 0 and self._clean_token(context[position - 1]) in subj_markers:
            vec[1] = 1.0  # Subject

        # Object detection (end of sentence or before punctuation)
        if position == len(context) - 1:
            vec[2] = 1.0  # Object

        # Modifier detection (before nouns)
        if position < len(context) - 1:
            next_clean = self._clean_token(context[position + 1])
            if next_clean in {'project', 'kaam', 'meeting', 'team', 'budget', 'target'}:
                vec[3] = 1.0  # Modifier

        # Action verb detection
        action_verbs = {'kiya', 'kari', 'kare', 'banaya', 'bheja', 'likha', 'discuss',
                       'present', 'deliver', 'complete', 'build', 'create', 'manage'}
        if clean in action_verbs:
            vec[4] = 1.0  # Action

        return vec

    def _frequency_signature(self, token: str, dim: int) -> np.ndarray:
        """How often has this token been seen?"""
        vec = np.zeros(dim)
        clean = self._clean_token(token)

        total_seen = sum(
            d.get('count', 0) 
            for k, d in self.decision_memory.items() 
            if k.startswith(clean + '|')
        )

        # Log-scale frequency
        vec[0] = min(1.0, math.log1p(total_seen) / 5.0)

        # Proxy identity flag
        if clean in self.proxy_identities:
            vec[1] = self.proxy_identities[clean].get('confidence', 0)

        return vec

    # ── Identity Dissolution Network ──────────────────

    def dissolve(self, text: str, identity_tokens: List[dict]) -> ZeroResult:
        """
        Main entry point. Dissolve identity while preserving structure.

        Args:
            text: Original text
            identity_tokens: List of detected identity tokens from BHRT engine
                             Each: {'token': str, 'category': str, 'position': int}

        Returns:
            ZeroResult with dissolved text, decisions, and evolution metrics
        """
        processing_id = hashlib.sha256(
            (text + str(time.time())).encode()
        ).hexdigest()[:16]

        tokens = self._tokenize(text)
        dissolved_tokens = []
        decisions = []

        # Build identity lookup
        identity_map = {}
        for it in identity_tokens:
            clean = self._clean_token(it['token'])
            identity_map[clean] = it

        # Also check proxy identities
        proxy_hits = []
        for i, token in enumerate(tokens):
            clean = self._clean_token(token)
            if clean in self.proxy_identities:
                proxy_hits.append({
                    'token': token,
                    'position': i,
                    'category': 'proxy_identity',
                    'confidence': self.proxy_identities[clean]['confidence'],
                    'source': 'proxy'
                })

        # Merge proxy hits with identity tokens
        all_identity = {self._clean_token(it['token']): it for it in identity_tokens}
        for ph in proxy_hits:
            clean = self._clean_token(ph['token'])
            if clean not in all_identity:
                all_identity[clean] = ph

        # Process each token
        for i, token in enumerate(tokens):
            clean = self._clean_token(token)

            if clean in all_identity:
                # This is identity — dissolve it
                it = all_identity[clean]
                context = tokens[max(0, i-3):min(len(tokens), i+4)]

                replacement, confidence, strategy = self._generate_placeholder(
                    token, context, it, i
                )

                dissolved_tokens.append(replacement)

                # Compute structural embedding for this decision
                embed = self._structural_embed(token, context, i)
                embed_key = f"{clean}|{replacement}"
                self.structural_embeddings[embed_key] = embed.tolist()

                decisions.append(ZeroDecision(
                    original=token,
                    replacement=replacement,
                    category=it.get('category', 'IDENTITY'),
                    confidence=confidence,
                    strategy=strategy,
                    context_hash=hashlib.sha256(' '.join(context).encode()).hexdigest()[:12],
                    structure_score=0.0,  # Will be updated after full text
                    timestamp=time.time()
                ))
            else:
                dissolved_tokens.append(token)

        dissolved_text = self._reconstruct_text(text, tokens, dissolved_tokens)

        # Compute scores
        structure_score = self._structure_preservation_score(text, dissolved_text)
        identity_score = self._identity_removal_score(dissolved_text, all_identity)
        topic_dist = self._topic_distribution(dissolved_text)
        pattern = self._behavioral_pattern(dissolved_text)

        # Update decision structure scores
        for dec in decisions:
            dec.structure_score = structure_score

        # Learn from this session
        self._learn_from_session(text, dissolved_text, decisions, structure_score)

        # Build evolution report
        evolution = self._build_evolution()

        self.session_stats["processed"] += 1
        self.session_stats["decisions"] += len(decisions)
        self.session_stats["confidence_sum"] += sum(d.confidence for d in decisions)
        self.session_stats["structure_sum"] += structure_score

        # Auto-save every 10 processed texts
        if self.session_stats["processed"] % 10 == 0:
            self.save()

        return ZeroResult(
            dissolved_text=dissolved_text,
            decisions=decisions,
            structure_score=structure_score,
            identity_score=identity_score,
            topic_distribution=topic_dist,
            behavioral_pattern=pattern,
            evolution=evolution,
            processing_id=processing_id
        )

    def _reconstruct_text(self, original: str, original_tokens: List[str], 
                          dissolved_tokens: List[str]) -> str:
        """Preserve original spacing and punctuation."""
        result = original
        for orig, diss in zip(original_tokens, dissolved_tokens):
            if orig != diss:
                # Replace first occurrence, preserve case if possible
                result = result.replace(orig, diss, 1)
        return result

    def _generate_placeholder(self, token: str, context: List[str], 
                              identity_info: dict, position: int) -> Tuple[str, float, str]:
        """
        Generate context-aware placeholder instead of generic [CATEGORY].

        Strategies:
        1. learned_replacement — seen this context before, use best replacement
        2. structural_role — infer role and generate [CATEGORY_ROLE]
        3. default — fallback to [CATEGORY]
        """
        category = identity_info.get('category', 'IDENTITY').upper()
        clean = self._clean_token(token)
        context_key = ' '.join([self._clean_token(t) for t in context])

        # Strategy 1: Learned replacement
        if context_key in self.replacement_memory:
            candidates = self.replacement_memory[context_key]
            if candidates:
                best = max(candidates, key=lambda x: x.get('score', 0))
                if best.get('score', 0) > 0.7:
                    return best['replacement'], best['confidence'], 'learned_replacement'

        # Strategy 2: Structural role inference
        role = self._infer_structural_role(token, context, position)

        # Refine category based on role
        refined_category = self._refine_category(category, role, context)

        placeholder = f"[{refined_category}]"
        confidence = 0.75

        # Boost confidence if proxy identity
        if identity_info.get('source') == 'proxy':
            confidence = identity_info.get('confidence', 0.75)

        return placeholder, confidence, 'structural_role'

    def _infer_structural_role(self, token: str, context: List[str], 
                               position: int) -> str:
        """Infer grammatical role for richer placeholders."""
        clean = self._clean_token(token)

        if position == 0:
            return "AGENT"

        if position == len(context) - 1:
            return "OBJECT"

        prev = self._clean_token(context[position - 1]) if position > 0 else ""
        next_t = self._clean_token(context[position + 1]) if position < len(context) - 1 else ""

        # Hinglish subject markers
        if prev in {'ne', 'ki', 'ka', 'ko', 'se'}:
            return "SUBJECT"

        # Action detection
        action_verbs = {'kiya', 'kari', 'kare', 'banaya', 'bheja', 'likha', 'discuss',
                       'present', 'deliver', 'complete', 'build', 'create', 'manage',
                       'lead', 'execute', 'develop'}
        if next_t in action_verbs or prev in action_verbs:
            return "ACTOR"

        # Location detection
        location_markers = {'mein', 'pe', 'par', 'se', 'tak', 'in', 'at', 'from', 'to'}
        if prev in location_markers:
            return "LOCATION"

        # Time detection
        time_markers = {'aaj', 'kal', 'parso', 'abhi', 'pehle', 'baad', 'today',
                       'yesterday', 'tomorrow', 'now', 'then'}
        if prev in time_markers or next_t in time_markers:
            return "TIME_REF"

        return "ENTITY"

    def _refine_category(self, category: str, role: str, context: List[str]) -> str:
        """Combine category and role for precise placeholder."""
        # Map roles to more specific categories
        role_category_map = {
            "AGENT": f"{category}_INITIATOR",
            "SUBJECT": f"{category}_DOER", 
            "ACTOR": f"{category}_ACTOR",
            "OBJECT": f"{category}_TARGET",
            "LOCATION": "LOCATION",
            "TIME_REF": "TEMPORAL",
        }

        if role in role_category_map:
            return role_category_map[role]

        # Check for compound patterns
        clean_context = ' '.join([self._clean_token(t) for t in context])

        if any(w in clean_context for w in ['project', 'kaam', 'naukri', 'career', 'business']):
            return f"{category}_PROF"
        if any(w in clean_context for w in ['ghar', 'family', 'maa', 'papa', 'wife', 'husband']):
            return f"{category}_PERS"
        if any(w in clean_context for w in ['paisa', 'money', 'budget', 'salary', 'cost', 'price']):
            return f"{category}_FIN"

        return category

    # ── Scoring Engines ───────────────────────────────

    def _structure_preservation_score(self, original: str, dissolved: str) -> float:
        """
        Score 0-1: How much grammatical/semantic structure survived?
        Higher = better preservation.
        """
        orig_tokens = self._tokenize(original)
        diss_tokens = self._tokenize(dissolved)

        # Action verb retention
        action_verbs = {'meeting', 'discuss', 'present', 'deliver', 'complete', 'build',
                       'create', 'develop', 'launch', 'execute', 'manage', 'lead',
                       'kiya', 'kari', 'kare', 'banaya', 'bheja', 'likha', 'submit',
                       'review', 'approve', 'reject', 'report', 'propose'}
        orig_actions = sum(1 for t in orig_tokens if self._clean_token(t) in action_verbs)
        diss_actions = sum(1 for t in diss_tokens if self._clean_token(t) in action_verbs)
        action_retention = diss_actions / max(orig_actions, 1)

        # Quantifier retention
        quantifiers = {'months', 'weeks', 'days', 'hours', 'percent', 'team',
                      'projects', 'tasks', 'mahine', 'din', 'ghante', 'log'}
        orig_quants = sum(1 for t in orig_tokens if self._clean_token(t) in quantifiers)
        diss_quants = sum(1 for t in diss_tokens if self._clean_token(t) in quantifiers)
        quant_retention = diss_quants / max(orig_quants, 1)

        # Sentence structure (length ratio)
        length_ratio = len(diss_tokens) / max(len(orig_tokens), 1)
        length_score = 1.0 - abs(1.0 - length_ratio) * 0.5

        # Topic coherence
        orig_topics = self._extract_topic_words(orig_tokens)
        diss_topics = self._extract_topic_words(diss_tokens)
        topic_overlap = len(orig_topics & diss_topics) / max(len(orig_topics), 1)

        # Weighted combination
        score = (action_retention * 0.35 + 
                quant_retention * 0.15 + 
                length_score * 0.20 + 
                topic_overlap * 0.30)

        return round(min(1.0, max(0.0, score)), 4)

    def _identity_removal_score(self, text: str, identity_map: Dict) -> float:
        """
        Score 0-1: How completely was identity removed?
        Higher = more completely removed.
        """
        tokens = self._tokenize(text)

        # Check for remaining pronouns
        pronouns = {'i', 'me', 'my', 'mine', 'myself', 'we', 'our', 'ours',
                   'main', 'mujhe', 'mera', 'meri', 'mere', 'hum', 'hamara',
                   'aap', 'apka', 'apki', 'tum', 'tumhara', 'mai', 'apna'}
        pronoun_count = sum(1 for t in tokens if self._clean_token(t) in pronouns)

        # Check for proxy identities that slipped through
        proxy_count = sum(1 for t in tokens if self._clean_token(t) in self.proxy_identities)

        # Check for name patterns
        name_pattern = re.compile(r'\b[A-Z][a-z]{2,15}\b')
        name_count = len(name_pattern.findall(text))

        # Check for PII
        pii_patterns = {
            'phone': r'\b(?:\+91|0)?[6-9]\d{9}\b',
            'email': r'\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Z|a-z]{2,}\b',
        }
        pii_count = sum(len(re.findall(p, text)) for p in pii_patterns.values())

        total_risk = pronoun_count + proxy_count + name_count + pii_count
        risk_ratio = total_risk / max(len(tokens), 1)

        return round(max(0.0, 1.0 - risk_ratio * 5), 4)

    def _extract_topic_words(self, tokens: List[str]) -> Set[str]:
        """Extract topic-indicating words."""
        topic_words = {
            'project', 'career', 'business', 'strategy', 'deadline', 'client',
            'team', 'meeting', 'budget', 'target', 'goal', 'product', 'service',
            'kaam', 'naukri', 'business', 'target', 'meeting', 'team',
            'emotion', 'feeling', 'relationship', 'family', 'health',
            'finance', 'money', 'investment', 'growth'
        }
        return set(self._clean_token(t) for t in tokens if self._clean_token(t) in topic_words)

    def _topic_distribution(self, text: str) -> Dict[str, float]:
        """Categorize text into topic buckets."""
        tokens = [self._clean_token(t) for t in self._tokenize(text)]

        topics = {
            'professional': {'project', 'career', 'business', 'strategy', 'deadline',
                            'client', 'meeting', 'team', 'lead', 'manage', 'kaam',
                            'naukri', 'office', 'company', 'boss', 'manager'},
            'personal_emotion': {'happy', 'sad', 'angry', 'worried', 'excited',
                                'khush', 'udaas', 'gussa', 'chinta', 'takleef',
                                'feel', 'think', 'believe', 'lagta', 'sochta'},
            'logistical': {'schedule', 'plan', 'timeline', 'process', 'system',
                          'step', 'phase', 'time', 'date', 'location'},
            'financial': {'budget', 'revenue', 'cost', 'price', 'money', 'salary',
                         'paisa', 'kharcha', 'investment', 'profit'},
            'trauma': {'bhag', 'bhagna', 'darr', 'dar', 'marna', 'maar',
                      'sex', 'chudai', 'hurt', 'pain', 'abuse', 'violence'},
            'relationship': {'gf', 'bf', 'pyaar', 'love', 'kiss', 'wife', 'husband',
                            'dost', 'yaar', 'friend', 'partner', 'family'},
        }

        scores = {}
        for topic, words in topics.items():
            score = sum(1 for t in tokens if t in words)
            scores[topic] = score

        total = sum(scores.values())
        if total > 0:
            scores = {k: round(v / total, 3) for k, v in scores.items()}
        else:
            scores = {k: 0.0 for k in topics}

        return scores

    def _behavioral_pattern(self, text: str) -> str:
        """Detect behavioral pattern from structural signal."""
        tokens = [self._clean_token(t) for t in self._tokenize(text)]

        patterns = {
            'CONFLICT_PROFESSIONAL': ['conflict', 'disagree', 'argue', 'dispute',
                                      'professional', 'work', 'colleague', 'boss'],
            'GROWTH_LEARNING': ['learn', 'improve', 'grow', 'skill', 'course',
                               'training', 'certificate', 'seekh', 'sikhna'],
            'LEADERSHIP_EXECUTION': ['lead', 'team', 'manage', 'decision',
                                    'responsibility', 'drive', 'leadership'],
            'CRISIS_MANAGEMENT': ['crisis', 'urgent', 'emergency', 'fix',
                                 'resolve', 'critical', 'problem', 'issue'],
            'STAKEHOLDER_NEGOTIATION': ['negotiate', 'client', 'stakeholder',
                                       'deal', 'contract', 'agreement'],
            'TRAUMA_NARRATIVE': ['bhag', 'bhagna', 'darr', 'dar', 'marna',
                                'maar', 'sex', 'bhalu', 'abuse', 'hurt'],
            'RELATIONSHIP_INTIMATE': ['gf', 'bf', 'pyaar', 'love', 'kiss',
                                     'wife', 'husband', 'dost', 'yaar'],
            'EXPLICIT_CONTENT': ['sex', 'chudai', 'kiss', 'fuck', 'chod',
                                'explicit', 'adult'],
            'REFLECTIVE_SELF': ['think', 'feel', 'believe', 'lagta', 'sochta',
                               'samajhta', 'realize', 'understand'],
        }

        scores = {}
        for pattern, keywords in patterns.items():
            score = sum(1 for kw in keywords if kw in tokens)
            scores[pattern] = score

        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return 'GENERAL_UNSTRUCTURED'
        return best

    # ── Self-Training Loop ────────────────────────────

    def _learn_from_session(self, original: str, dissolved: str,
                            decisions: List[ZeroDecision], structure_score: float):
        """
        The heart of ZERO: every session teaches the system.
        """
        orig_tokens = [self._clean_token(t) for t in self._tokenize(original)]
        diss_tokens = [self._clean_token(t) for t in self._tokenize(dissolved)]

        removed = set(orig_tokens) - set(diss_tokens)
        kept = set(diss_tokens)

        # 1. Update decision memory
        for dec in decisions:
            key = f"{self._clean_token(dec.original)}|{dec.strategy}"
            if key in self.decision_memory:
                self.decision_memory[key]["count"] += 1
                old_score = self.decision_memory[key]["avg_structure_score"]
                old_count = self.decision_memory[key]["count"]
                self.decision_memory[key]["avg_structure_score"] = (
                    (old_score * (old_count - 1) + structure_score) / old_count
                )
                self.decision_memory[key]["last_used"] = time.time()
            else:
                self.decision_memory[key] = {
                    "count": 1,
                    "avg_structure_score": structure_score,
                    "replacement": dec.replacement,
                    "category": dec.category,
                    "last_used": time.time(),
                }

        # 2. Pattern discovery — find proxy identities
        for kept_token in kept:
            if len(kept_token) < self.config["min_token_length"]:
                continue

            for removed_token in removed:
                if len(removed_token) < self.config["min_token_length"]:
                    continue

                # Record correlation
                self.correlation_map[kept_token][removed_token] =                     self.correlation_map[kept_token].get(removed_token, 0) + 1

                # Check if this should become a proxy identity
                count = self.correlation_map[kept_token][removed_token]
                if count >= self.config["proxy_discovery_threshold"]:
                    if kept_token not in self.proxy_identities:
                        self.proxy_identities[kept_token] = {
                            "linked_to": removed_token,
                            "confidence": min(0.95, 0.6 + 0.07 * count),
                            "discovered_at": time.time(),
                            "correlation_count": count,
                        }
                        self.session_stats["new_patterns"] += 1
                    else:
                        # Boost existing proxy
                        old_conf = self.proxy_identities[kept_token]["confidence"]
                        self.proxy_identities[kept_token]["confidence"] = min(
                            0.99, old_conf + 0.01
                        )
                        self.proxy_identities[kept_token]["correlation_count"] = count

        # 3. Learn replacement effectiveness
        for dec in decisions:
            context_key = ' '.join([
                self._clean_token(t) 
                for t in self._tokenize(original)
            ])
            if context_key not in self.replacement_memory:
                self.replacement_memory[context_key] = []

            # Check if this replacement already exists
            existing = [r for r in self.replacement_memory[context_key]
                       if r.get('replacement') == dec.replacement]

            if existing:
                existing[0]["score"] = (
                    existing[0]["score"] * 0.9 + structure_score * 0.1
                )
                existing[0]["uses"] = existing[0].get("uses", 0) + 1
            else:
                self.replacement_memory[context_key].append({
                    "replacement": dec.replacement,
                    "score": structure_score,
                    "confidence": dec.confidence,
                    "uses": 1,
                    "first_used": time.time(),
                })

    def _build_evolution(self) -> ZeroEvolution:
        """Build current evolution snapshot."""
        total_decisions = sum(d.get('count', 0) for d in self.decision_memory.values())
        total_processed = self.session_stats["processed"] + total_decisions

        avg_conf = (self.session_stats["confidence_sum"] / 
                   max(self.session_stats["decisions"], 1))
        avg_struct = (self.session_stats["structure_sum"] / 
                     max(self.session_stats["processed"], 1))

        # Learning velocity: new patterns per 100 processed
        velocity = (self.session_stats["new_patterns"] / 
                   max(self.session_stats["processed"], 1) * 100)

        # Memory size estimate
        memory_size = 0
        try:
            memory_size = os.path.getsize(self.memory_path) / 1024 if os.path.exists(self.memory_path) else 0
        except:
            pass

        return ZeroEvolution(
            total_processed=total_processed,
            total_decisions=total_decisions,
            avg_confidence=round(avg_conf, 3),
            avg_structure_score=round(avg_struct, 3),
            proxy_identities_found=len(self.proxy_identities),
            new_patterns_this_session=self.session_stats["new_patterns"],
            learning_velocity=round(velocity, 2),
            memory_size_kb=round(memory_size, 2)
        )

    # ── Public API ────────────────────────────────────

    def get_stats(self) -> Dict:
        """Get current learning statistics."""
        return {
            "decision_memory_size": len(self.decision_memory),
            "correlation_entries": sum(len(v) for v in self.correlation_map.values()),
            "proxy_identities": len(self.proxy_identities),
            "replacement_contexts": len(self.replacement_memory),
            "embeddings_stored": len(self.structural_embeddings),
            "session_processed": self.session_stats["processed"],
            "session_decisions": self.session_stats["decisions"],
            "session_new_patterns": self.session_stats["new_patterns"],
        }

    def reset_session(self):
        """Reset session counters (not memory)."""
        self.session_stats = {
            "processed": 0,
            "decisions": 0,
            "new_patterns": 0,
            "confidence_sum": 0.0,
            "structure_sum": 0.0,
        }

    def export_model(self) -> Dict:
        """Export learned model for sharing/backup."""
        return {
            "proxy_identities": self.proxy_identities,
            "decision_memory": self.decision_memory,
            "replacements": self.replacement_memory,
            "version": "zero-1.0",
            "exported_at": time.time(),
            "stats": self.get_stats()
        }

    def import_model(self, model_data: Dict):
        """Import learned model from another ZERO instance."""
        self.proxy_identities.update(model_data.get("proxy_identities", {}))
        self.decision_memory.update(model_data.get("decision_memory", {}))
        self.replacement_memory.update(model_data.get("replacements", {}))
        self.save()


# ══════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════

def create_zero_mind(memory_path: str = "zero_mind.json") -> ZeroMind:
    """Factory function to create ZERO Mind instance."""
    return ZeroMind(memory_path)


# ══════════════════════════════════════════════════════
#  CLI DEMO
# ══════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys

    print("=" * 70)
    print("  ZERO Mind — Self-Training Identity Dissolution Network")
    print("  v1.0 · J.B.S. Mandloi · Apache 2.0")
    print("=" * 70)

    zero = create_zero_mind()

    if len(sys.argv) > 1 and sys.argv[1] == '--stats':
        print("\n  Current Learning Stats:")
        for k, v in zero.get_stats().items():
            print(f"    {k}: {v}")
        sys.exit(0)

    # Demo
    demo_text = "Main aaj bahut udaas hoon. Mera boss ne mujhe daanta. Mujhe lagta hai main fail ho gaya."
    demo_identity = [
        {"token": "Main", "category": "pronoun", "position": 0},
        {"token": "mera", "category": "pronoun", "position": 4},
        {"token": "mujhe", "category": "pronoun", "position": 6},
        {"token": "main", "category": "pronoun", "position": 11},
        {"token": "boss", "category": "name", "position": 5},
    ]

    print(f"\n  Input: {demo_text}")
    print(f"  Identity tokens: {len(demo_identity)}")
    print("\n  Dissolving...\n")

    result = zero.dissolve(demo_text, demo_identity)

    print(f"  Dissolved: {result.dissolved_text}")
    print(f"  Structure Score: {result.structure_score}")
    print(f"  Identity Score: {result.identity_score}")
    print(f"  Pattern: {result.behavioral_pattern}")
    print(f"  Decisions: {len(result.decisions)}")
    print(f"\n  Evolution:")
    print(f"    Total Processed: {result.evolution.total_processed}")
    print(f"    Proxy Identities: {result.evolution.proxy_identities_found}")
    print(f"    Learning Velocity: {result.evolution.learning_velocity}")
    print(f"    Memory Size: {result.evolution.memory_size_kb} KB")

    zero.save()
    print("\n  Memory saved.")
