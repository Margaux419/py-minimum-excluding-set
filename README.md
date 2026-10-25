# py-minimum-excluding-set

A small, pure-Python data structure that maintains a dynamic set of non-negative integers and instantly reports the smallest value not present (the *MEX*, or minimum excluding value).

## Usage

```python
from py_minimum_excluding_set import MinimumExcludingSet

s = MinimumExcludingSet()
assert s.value() == 0

s.add(0)
s.add(1)
s.add(2)
assert s.value() == 3

s.add(5)          # a gap above the current answer; answer stays 3
assert s.value() == 3

s.discard(1)      # removal lowers the answer to the first gap
assert s.value() == 1
```

## Why this exists

The minimum excluding value shows up in game-theory positions (Sprague-Grundy), allocator slot booking, and protocol sequence numbering. A naive re-scan of the set on every query is O(n); this library keeps the answer current in O(1) amortized time per mutation by maintaining a candidate heap of gaps and exploiting the fact that the MEX only ever *increases* as contiguous values from zero are filled.

The trade-off: the candidate heap may hold stale entries (values that were offered as gaps but later turned out to be present). These are filtered lazily when they surface, so the heap can grow to the number of distinct insertions in the worst case, while queries stay cheap.

## Edge cases

- Only non-negative integers are supported. Passing a negative to `add` raises `ValueError`.
- Adding a value already present is a no-op (idempotent).
- Removing a value with `discard` can lower the reported MEX, since the answer is recomputed from the current contents.

## API

- `MinimumExcludingSet()` — construct an empty set, MEX = 0.
- `add(n)` — insert a non-negative integer.
- `discard(n)` — remove `n` if present; no-op otherwise.
- `value()` — return the current MEX.
- `len(s)` — number of elements currently stored.
- `n in s` — membership test.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

