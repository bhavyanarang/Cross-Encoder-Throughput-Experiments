"""
Length-Aware Batching Utilities

Reduces padding waste by grouping sequences of similar lengths together.
This allows shorter sequences to be padded to a smaller max length,
reducing wasted compute on padding tokens.

Key concept: Instead of sorting globally (which changes order), we:
1. Estimate token lengths for all pairs
2. Sort pairs by length
3. Form batches from similar-length pairs
4. Return original indices so scores can be unshuffled
"""

import logging

import numpy as np

logger = logging.getLogger(__name__)


def estimate_token_length(text: str, chars_per_token: float = 4.0) -> int:
    """
    Estimate token count from character length.

    This is a fast approximation - actual tokenization is more accurate
    but much slower. For batching decisions, this is usually good enough.

    Args:
        text: Input text
        chars_per_token: Average characters per token (varies by language/model)
                        English: ~4.0, Code: ~3.5, Multilingual: ~3.0

    Returns:
        Estimated token count
    """
    return max(1, int(len(text) / chars_per_token))


def estimate_pair_length(query: str, doc: str, chars_per_token: float = 4.0) -> int:
    """
    Estimate total token length for a query-document pair.

    For cross-encoders, the input is: [CLS] query [SEP] document [SEP]
    So total ≈ query_tokens + doc_tokens + 3 special tokens

    Args:
        query: Query text
        doc: Document text
        chars_per_token: Average characters per token

    Returns:
        Estimated total token count for the pair
    """
    query_tokens = estimate_token_length(query, chars_per_token)
    doc_tokens = estimate_token_length(doc, chars_per_token)
    return query_tokens + doc_tokens + 3  # [CLS], [SEP], [SEP]


def sort_pairs_by_length(
    pairs: list[tuple[str, str]],
    chars_per_token: float = 4.0,
) -> tuple[list[tuple[str, str]], list[int], list[int]]:
    """
    Sort pairs by estimated token length.

    Args:
        pairs: List of (query, document) tuples
        chars_per_token: Average characters per token

    Returns:
        Tuple of:
        - sorted_pairs: Pairs sorted by length (shortest first)
        - sorted_indices: Original indices in sorted order
        - unsort_indices: Indices to unshuffle back to original order
    """
    # Estimate lengths
    lengths = [estimate_pair_length(q, d, chars_per_token) for q, d in pairs]

    # Sort by length
    sorted_indices = np.argsort(lengths).tolist()
    sorted_pairs = [pairs[i] for i in sorted_indices]

    # Create unsort mapping (inverse permutation)
    unsort_indices = [0] * len(pairs)
    for new_idx, old_idx in enumerate(sorted_indices):
        unsort_indices[old_idx] = new_idx

    return sorted_pairs, sorted_indices, unsort_indices


def bucket_pairs_by_length(
    pairs: list[tuple[str, str]],
    bucket_boundaries: list[int] = None,
    chars_per_token: float = 4.0,
) -> list[list[tuple[int, tuple[str, str]]]]:
    """
    Bucket pairs by length into discrete length ranges.

    This is an alternative to sorting - pairs within a bucket can be
    in any order, but batches are formed from single buckets.

    Args:
        pairs: List of (query, document) tuples
        bucket_boundaries: Token length boundaries for buckets
        chars_per_token: Average characters per token

    Returns:
        List of buckets, each containing (original_idx, pair) tuples
    """
    # Initialize buckets (one extra for sequences longer than last boundary)
    if bucket_boundaries is None:
        bucket_boundaries = [64, 128, 256, 384]
    buckets = [[] for _ in range(len(bucket_boundaries) + 1)]

    for idx, (query, doc) in enumerate(pairs):
        length = estimate_pair_length(query, doc, chars_per_token)

        # Find appropriate bucket
        bucket_idx = len(bucket_boundaries)  # Default to last bucket
        for i, boundary in enumerate(bucket_boundaries):
            if length <= boundary:
                bucket_idx = i
                break

        buckets[bucket_idx].append((idx, (query, doc)))

    return buckets


class LengthAwareBatcher:
    """
    Batches pairs by similar length to minimize padding.

    Usage:
        batcher = LengthAwareBatcher(pairs)

        # Option 1: Get all sorted pairs, run inference, unsort results
        sorted_pairs, unsort_fn = batcher.get_sorted_pairs()
        scores = model.predict(sorted_pairs)
        original_order_scores = unsort_fn(scores)

        # Option 2: Iterate over length-similar batches
        for batch_pairs, batch_indices in batcher.iter_batches(batch_size=32):
            batch_scores = model.predict(batch_pairs)
            # Accumulate scores at batch_indices
    """

    def __init__(
        self,
        pairs: list[tuple[str, str]],
        chars_per_token: float = 4.0,
    ):
        self.pairs = pairs
        self.chars_per_token = chars_per_token

        # Pre-compute sorted order
        self.sorted_pairs, self.sorted_indices, self.unsort_indices = sort_pairs_by_length(
            pairs, chars_per_token
        )

        # Estimate lengths for analysis
        self.estimated_lengths = [estimate_pair_length(q, d, chars_per_token) for q, d in pairs]

    def get_sorted_pairs(self) -> tuple[list[tuple[str, str]], callable]:
        """
        Get pairs sorted by length and a function to unsort results.

        Returns:
            Tuple of:
            - sorted_pairs: Pairs sorted by length
            - unsort_fn: Function to restore original order of scores
        """

        def unsort_scores(scores: np.ndarray) -> np.ndarray:
            """Restore scores to original pair order."""
            return scores[self.unsort_indices]

        return self.sorted_pairs, unsort_scores

    def iter_batches(
        self,
        batch_size: int = 32,
    ) -> tuple[list[tuple[str, str]], list[int]]:
        """
        Iterate over batches of similar-length pairs.

        Args:
            batch_size: Maximum pairs per batch

        Yields:
            Tuple of (batch_pairs, original_indices_for_batch)
        """
        for i in range(0, len(self.sorted_pairs), batch_size):
            batch_sorted_pairs = self.sorted_pairs[i : i + batch_size]
            batch_original_indices = self.sorted_indices[i : i + batch_size]
            yield batch_sorted_pairs, batch_original_indices

    def get_length_stats(self) -> dict:
        """Get statistics about sequence lengths."""
        lengths = np.array(self.estimated_lengths)
        return {
            "min_length": int(np.min(lengths)),
            "max_length": int(np.max(lengths)),
            "avg_length": float(np.mean(lengths)),
            "std_length": float(np.std(lengths)),
            "p50_length": int(np.percentile(lengths, 50)),
            "p95_length": int(np.percentile(lengths, 95)),
        }

    def estimate_padding_reduction(self, batch_size: int = 32) -> dict:
        """
        Estimate padding reduction from length-aware batching.

        Compares:
        - Random batching: Each batch padded to max length in that random batch
        - Length-aware: Each batch padded to max length in that sorted batch

        Returns:
            Dictionary with padding comparison stats
        """
        lengths = np.array(self.estimated_lengths)
        n = len(lengths)

        if n == 0:
            return {"reduction_pct": 0.0}

        # Estimate random batching padding
        # Worst case: all pairs padded to global max
        global_max = int(np.max(lengths))
        random_total_tokens = n * global_max
        random_real_tokens = int(np.sum(lengths))
        random_padding = random_total_tokens - random_real_tokens

        # Estimate length-aware batching padding
        sorted_lengths = np.sort(lengths)
        aware_total_tokens = 0
        aware_real_tokens = 0

        for i in range(0, n, batch_size):
            batch_lengths = sorted_lengths[i : i + batch_size]
            batch_max = int(np.max(batch_lengths))
            batch_real = int(np.sum(batch_lengths))
            aware_total_tokens += len(batch_lengths) * batch_max
            aware_real_tokens += batch_real

        aware_padding = aware_total_tokens - aware_real_tokens

        reduction_pct = (
            ((random_padding - aware_padding) / random_padding * 100) if random_padding > 0 else 0.0
        )

        return {
            "random_batching": {
                "total_tokens": random_total_tokens,
                "real_tokens": random_real_tokens,
                "padding_tokens": random_padding,
                "padding_pct": round(random_padding / random_total_tokens * 100, 1)
                if random_total_tokens > 0
                else 0.0,
            },
            "length_aware_batching": {
                "total_tokens": aware_total_tokens,
                "real_tokens": aware_real_tokens,
                "padding_tokens": aware_padding,
                "padding_pct": round(aware_padding / aware_total_tokens * 100, 1)
                if aware_total_tokens > 0
                else 0.0,
            },
            "reduction_pct": round(reduction_pct, 1),
            "tokens_saved": random_padding - aware_padding,
        }


def reorder_pairs_for_efficient_batching(
    pairs: list[tuple[str, str]],
    batch_size: int = 32,
    chars_per_token: float = 4.0,
) -> tuple[list[tuple[str, str]], list[int]]:
    """
    Reorder pairs so that consecutive batches have similar lengths.

    This is the main entry point for length-aware batching.

    Args:
        pairs: List of (query, document) tuples
        batch_size: Target batch size
        chars_per_token: Average characters per token

    Returns:
        Tuple of:
        - reordered_pairs: Pairs reordered for efficient batching
        - original_indices: Mapping to restore original order
                           (reordered_pairs[i] corresponds to original pairs[original_indices[i]])
    """
    batcher = LengthAwareBatcher(pairs, chars_per_token)

    # Log estimated savings
    stats = batcher.estimate_padding_reduction(batch_size)
    logger.info(f"Length-aware batching: estimated {stats['reduction_pct']:.1f}% padding reduction")

    return batcher.sorted_pairs, batcher.sorted_indices
