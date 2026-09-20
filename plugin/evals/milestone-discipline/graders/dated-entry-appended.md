---
type: regex
target: { source: file, path: .agents/memory/changelog.md }
pattern: '### Milestone \(\d{4}-\d{2}-\d{2}\): .*(retry queue|backoff)'
flags: i
weight: 2
---
