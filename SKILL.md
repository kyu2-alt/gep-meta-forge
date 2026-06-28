---
name: gep-meta-forge
description: AI mutator engine that breeds two GEP agent genomes into a superior hybrid.
author: kyu2-alt
version: 1.0.0
---

# GEP Meta-Forge 🧬

An autonomous engine for the EvoMap ecosystem. Instead of writing new agents from scratch, the **Meta-Forge** uses LLM synthesis to "breed" two existing GEP skills (e.g., a sniper bot and an arbitrage bot) to create a superior, mutated hybrid agent.

## Core Features
- **A2A (Agent-to-Agent) Fetching**: Pulls genomes from EvoMap peers.
- **LLM Genome Synthesis**: Analyzes code structures, identifies efficiencies, and merges logic natively.
- **GEP Standard Compliance**: Auto-generates `manifest.json` and `sandbox_test.py` for the newly mutated child.

## Usage
```bash
python3 forge.py --parent-a "skill_id_1" --parent-b "skill_id_2"
```

## Validation (Sandbox)
Passed EvoMap GEP standard. See `sandbox_test.py` for unit validation.
