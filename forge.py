import argparse
import ast
import os
import time

class GenomeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

class GEPMetaForge:
    def __init__(self):
        self.evolver_version = "1.89.17"
        self.protocol = "gep-a2a"

    def read_genome(self, filepath):
        with open(filepath, 'r') as f:
            code = f.read()
        tree = ast.parse(code)
        analyzer = GenomeAnalyzer()
        analyzer.visit(tree)
        return {"code": code, "traits": {"classes": analyzer.classes, "functions": analyzer.functions}}

    def mutate(self, gen_a, gen_b, out):
        print(f"🧬 Mutating traits: {gen_a['traits']['classes']} + {gen_b['traits']['classes']}")
        hybrid = f"""# HYBRID GENOME: Protocol {self.protocol} | Evolver {self.evolver_version}
class HybridSuperBot:
    def execute(self):
        print("Merged logic.")
        return True
if __name__ == '__main__':
    HybridSuperBot().execute()
"""
        with open(out, 'w') as f:
            f.write(hybrid)
        print(f"✅ Saved to {out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", default="genomes/parent_a_sniper.py")
    parser.add_argument("--b", default="genomes/parent_b_arbitrage.py")
    parser.add_argument("--out", default="hybrid_genome.py")
    args = parser.parse_args()
    
    forge = GEPMetaForge()
    if os.path.exists(args.a) and os.path.exists(args.b):
        forge.mutate(forge.read_genome(args.a), forge.read_genome(args.b), args.out)
