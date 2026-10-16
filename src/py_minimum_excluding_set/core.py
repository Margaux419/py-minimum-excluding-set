"""Dynamic set that reports the smallest non-negative integer not present.

We keep two structures in sync:

* ``present`` – a set of the integers currently in the structure, so we can
  answer membership and removal in O(1).
* ``missing`` – a min-heap of candidate gaps discovered so far.

When we add an integer ``n`` we also offer ``n + 1`` as a *candidate* gap.
  The candidate is discarded if it turns out to be present, so we never
  need to remove arbitrary elements from the middle of the heap.
  Instead we lazily discard stale entries when they surface.  This trades a
  slightly larger heap for a simpler deletion story and O(1) amortized
  queries.

The smallest missing value is recalculated when a value is discarded, since
  removals can lower the answer.
"""

import heapq


class MinimumExcludingSet:
    """Maintain a dynamic set of non-negative integers and report the MEX.

    MEX = "minimum excluding" value: the smallest non-negative integer that
    is *not* currently in the set.  Starts at 0 for an empty set.

    Values must be non-negative integers.  Adding an already-present value is
    a no-op.  Adding ``n`` implicitly makes ``n + 1`` a candidate for the
    answer, but the candidate is only surfaced once every smaller value is
    accounted for.
    """

    def __init__(self):
        self._present = set()
        # Min-heap of *candidate* missing values. May contain stale entries
        # (values that later turned out to be present); we filter them lazily
        # in ``value``.
        self._candidates = [0]
        self._min_missing = 0

    def add(self, n):
        """Insert a non-negative integer into the set. Idempotent."""
        if n < 0:
            raise ValueError("only non-negative integers are supported")
        if n in self._present:
            return
        self._present.add(n)
        if n == self._min_missing:
            self._advance()
        else:
            heapq.heappush(self._candidates, n + 1)

    def _advance(self):
        """Move ``_min_missing`` past consecutive present values."""
        # Repeatedly increment while the value is present, then check the
        # candidate heap for anything larger that might already be missing.
        while self._min_missing in self._present:
            self._min_missing += 1
        while self._candidates and self._candidates[0] <= self._min_missing:
            heapq.heappop(self._candidates)

    def _recompute(self):
        """Recompute ``_min_missing`` from scratch, discarding stale heap."""
        self._min_missing = 0
        self._candidates = [0]
        self._advance()

    def discard(self, n):
        """Remove ``n`` if present. The MEX is recalculated.

        Because removals can lower the answer, we recompute ``_min_missing``
        from the current contents.
        """
        if n not in self._present:
            return
        self._present.discard(n)
        self._recompute()

    def value(self):
        """Return the current MEX in O(1) amortized time."""
        # ``_advance`` already keeps ``_min_missing`` correct after inserts
        # and discards, but we pop any stale candidates that equal the answer.
        while self._candidates and self._candidates[0] == self._min_missing:
            heapq.heappop(self._candidates)
            if self._min_missing in self._present:
                self._advance()
            else:
                break
        return self._min_missing

    def __len__(self):
        return len(self._present)

    def __contains__(self, n):
        return n in self._present

    def __repr__(self):
        return f"MinimumExcludingSet(value={self.value()}, size={len(self)})"
