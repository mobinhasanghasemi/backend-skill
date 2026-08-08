# RESEARCH PROTOCOL

The brain's **deep-learning discipline**. Before ANY substantial claim enters the knowledge base, it must pass through research. This file defines the workflow, the source hierarchy, contradiction handling, and the research quality gate.

---

## Why the protocol exists

> Knowledge without research is rumor wearing a lab coat.

A neuron must not contain claims that are:
- outdated (version drift)
- version-specific but stated as universal
- workload-specific but stated as general
- security-sensitive but unexamined
- community-myth (survives on repetition, not evidence)
- hallucinated by a previous AI session

---

## The Research Pipeline (mandatory for NEW substantial facts)

```text
Research
    │
    ▼
Source Discovery            (find the authority, not the echo)
    │
    ▼
Official Documentation      (vendor docs, specs, standards bodies)
    │
    ▼
Standards                   (RFC, ISO/IEC, OAS, CNCF...)
    │
    ▼
Security Guidance           (OWASP, NIST, CISA, vendor security pages)
    │
    ▼
Recent Changes              (release notes, changelog, deprecations)
    │
    ▼
Known Issues                (github issues, known limitations)
    │
    ▼
Performance Evidence        (benchmarks — labelled measured vs vendor claims)
    │
    ▼
Production Experience       (public postmortems, case studies)
    │
    ▼
Contradiction Detection     (do sources disagree?)
    │
    ▼
Synthesis
    │
    ▼
Neuron Generation
    │
    ▼
Review (quality gate below)
```

---

## Source Hierarchy (strongest first)

1. **Official standards** (RFC, ISO, OASIS, W3C, IETF)
2. **Official documentation** (Vendor: docs.djangoproject.com, postgresql.org, kubernetes.io)
3. **Official specifications** (OpenAPI, OpenTelemetry spec, SemVer)
4. **Academic research** (peer-reviewed on the topic)
5. **Established engineering orgs** (SRE books, AWS/Azure/GCP well-architected, Google SRE)
6. **Production case studies**
7. **Benchmarks** (labelled methodology)
8. **Community sources** (blogs, StackOverflow, Reddit) — LOWEST, must not override 1-3 without strong corroboration.

---

## Contradiction Detection

If two sources disagree:

- Identify the **entire disagreement** (versions? workloads? environments? security stance?)
- Prefer the higher-authority source **by default**
- If conflict is work-loadsensitive → state BOTH with the differentiator, don't pick a winner
- If conflict is security-related → take the **more conservative** reading
- Record the conflict in the neuron's Evidence section

---

## Version Awareness

Every technology neuron must record:

| Field | Example |
|---|---|
| Current version | Django 6.0.x (Dec 2025) |
| LTS | 5.2, ends April 2028 |
| Supported Python | 6.0: 3.12–3.14 |
| Breaking changes | removed `django.contrib.gis` in 6.0? (verify!) |
| Security advisories | check Django security release list |
| Migration guidance | from 4.2/5.2 → 6.0 |

The **version matrix** with global truth lives in `brain/version-awareness.md`. Neurons reference it rather than repeatedly cloning numbers.

---

## The Research Quality Gate

Before publishing/updating a substantial neuron, check all of the following:

```
[ ] current official documentation checked
[ ] relevant standard checked
[ ] security guidance checked
[ ] recent changes checked
[ ] deprecations checked
[ ] known limitations checked
[ ] performance claims validated (measured vs claimed separated)
[ ] conflicting recommendations investigated
[ ] version boundaries identified
[ ] evidence recorded in the neuron
[ ] Confidence assigned
```

If any is missing, the claim pending → mark `Verification Status: pending` and `Confidence: UNCERTAIN` rather than shipping it as fact.

---

## Research Tools of the trade

- Web searches for: `vendor docs <technology> version release`, `release notes <technology>`, `known issues <technology> <version>`, `<technology> deprecations`.
- Get 2026-era info on **version** + **breaking changes** + **security announcements** for every technology neuron before `Version Awareness`.
- For number-based claims (throughput/latency): prefer the vendor's own labelled-caveat benchmarks; ideal measured numbers require an environment, so mark `MEASURED` vs `REPORTED`.

---

## When this protocol is NOT required

- Lightweight directory references (links)
- Neurons whose claims are textbook-stable (MVCC, b-tree—verified long ago, low drift)
- ROOT routing rules (logic, not fact)

**Larger changes (new technology, practice-shift, version jumps) ALWAYS trigger the pipeline.**

---

## Anti-Patterns in research (Do not)

- ❌ Citing a blog that cites a blog that cites the vendor docs (echo)
- ❌ "It is 2026 and X is the best" without source
- ❌ Generalizing "we did X at our company" without the caveats
- ❌ Preserving "best practice" from a 2015 post in a 2026 system without re-verification