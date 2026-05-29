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
        location_markers = {'mein', 'pe', 'par', 'se', 'tak', 'in', 'at', 'from', '
