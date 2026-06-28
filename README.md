# GEP Meta-Forge 🧬
![EvoMap GEP Validation](https://github.com/kyu2-alt/gep-meta-forge/actions/workflows/evomap_gep_test.yml/badge.svg)

> **AI Mutator Engine for the EvoMap Ecosystem.**
> Autonomously fetches two agent skills, analyzes their genomes via Python AST, and synthesizes a highly optimized hybrid agent.

## Core Features
1. **True AST Extraction**: Parses Python source code, breaking it down into `imports`, `classes`, and `functions`.
2. **Deterministic and LLM Stitching**: Deduplicates imports and synthesizes logic. Use `--llm` to trigger semantic merging via OpenAI.
3. **Automated Sandbox Validation**: The generated hybrid genome is immediately tested in an isolated subprocess to ensure syntax viability.
4. **GEP Standard Compliance**: Injects EvoMap A2A protocols and `evolver_version` tracking automatically.
5. **CI/CD Pipeline**: GitHub Actions auto-validates genomes against EvoMap Sandbox rules on every push.

## Installation
```bash
git clone git@github.com:kyu2-alt/gep-meta-forge.git
cd gep-meta-forge
pip install -r requirements.txt
```

## Usage
The engine takes two parent genomes and mutates them into a hybrid child agent:
```bash
python3 forge.py --a genomes/parent_a_sniper.py --b genomes/parent_b_arbitrage.py --out hybrid.py
```

### Publishing to EvoMap
Validate and broadcast your mutated agent to the network:
```bash
python3 publish.py --dry-run
python3 publish.py
```
