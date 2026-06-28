import argparse
import ast
import hashlib
import os
import sys
import subprocess
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

try:
    from radon.complexity import cc_visit
except ImportError:
    cc_visit = None

console = Console()

class GenomeExtractor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.main_class = None
        self.methods = {}

    def visit_Import(self, node):
        self.imports.append(node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.imports.append(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        if not self.main_class:
            self.main_class = node.name
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    self.methods[item.name] = item
        self.generic_visit(node)

class GEPMetaForge:
    def __init__(self):
        self.evolver_version = "1.89.17"
        self.protocol = "gep-a2a"

    def extract_dna(self, filepath):
        with open(filepath, 'r') as f:
            code = f.read()
        tree = ast.parse(code)
        extractor = GenomeExtractor()
        extractor.visit(tree)
        return extractor, code

    def calculate_fitness(self, code_str):
        if not cc_visit:
            return 1.0
        blocks = cc_visit(code_str)
        complexity = sum(b.complexity for b in blocks)
        lines = len(code_str.splitlines())
        return round((lines / (complexity + 1)) * 1.5, 2)

    def generate_gene_id(self, code_str):
        return hashlib.sha256(code_str.encode('utf-8')).hexdigest()[:16]

    def synthesize_ast(self, ext_a, ext_b):
        merged_imports = []
        seen_imports = set()
        for imp in ext_a.imports + ext_b.imports:
            imp_code = ast.unparse(imp)
            if imp_code not in seen_imports:
                seen_imports.add(imp_code)
                merged_imports.append(imp)

        init_a = ext_a.methods.get('__init__')
        init_b = ext_b.methods.get('__init__')
        merged_init_body = []
        if init_a: merged_init_body.extend(init_a.body)
        if init_b: merged_init_body.extend(init_b.body)
        if not merged_init_body: merged_init_body = [ast.Pass()]

        hybrid_init = ast.FunctionDef(
            name='__init__',
            args=ast.arguments(posonlyargs=[], args=[ast.arg(arg='self')], kwonlyargs=[], kw_defaults=[], defaults=[]),
            body=merged_init_body, decorator_list=[], returns=None
        )

        merged_methods = [hybrid_init]
        for name, method in ext_a.methods.items():
            if name != '__init__': merged_methods.append(method)
        for name, method in ext_b.methods.items():
            if name != '__init__': merged_methods.append(method)

        hybrid_class = ast.ClassDef(
            name='EvolvedHybridSuperBot', bases=[], keywords=[],
            body=merged_methods, decorator_list=[]
        )

        module_body = merged_imports + [hybrid_class]
        exec_code = "\nif __name__ == '__main__':\n    bot = EvolvedHybridSuperBot()\n    print('[GEP-A2A] EvolvedHybridSuperBot Online.')\n"
        module_body.extend(ast.parse(exec_code).body)

        hybrid_module = ast.Module(body=module_body, type_ignores=[])
        ast.fix_missing_locations(hybrid_module)
        return ast.unparse(hybrid_module)

    def validate_sandbox(self, filepath):
        result = subprocess.run([sys.executable, filepath], capture_output=True, text=True, timeout=5)
        return result.returncode == 0, result.stdout, result.stderr

    def run(self, file_a, file_b, out_file):
        console.print(Panel(f"[bold cyan]🧬 GEP Meta-Forge - AST Synthesis[/bold cyan]\nEvolver: {self.evolver_version}", border_style="cyan"))
        ext_a, code_a = self.extract_dna(file_a)
        ext_b, code_b = self.extract_dna(file_b)
        
        fitness_a = self.calculate_fitness(code_a)
        fitness_b = self.calculate_fitness(code_b)

        console.print(f"[green]✔ Parent A:[/green] {ext_a.main_class} (Fitness: {fitness_a})")
        console.print(f"[green]✔ Parent B:[/green] {ext_b.main_class} (Fitness: {fitness_b})")
        
        hybrid_code = self.synthesize_ast(ext_a, ext_b)
        gene_id = self.generate_gene_id(hybrid_code)
        
        final_code = f'"""\nGEP HYBRID GENOME\nGene ID: {gene_id}\n"""\n\n' + hybrid_code
        with open(out_file, 'w') as f: f.write(final_code)
            
        fitness_hybrid = self.calculate_fitness(final_code)
        passed, stdout, stderr = self.validate_sandbox(out_file)
        
        if passed:
            table = Table(title="Mutation Results")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="magenta")
            table.add_row("Gene Signature (SHA-256)", gene_id)
            table.add_row("Fitness Delta", f"{(fitness_hybrid - max(fitness_a, fitness_b)):+.2f}")
            table.add_row("Sandbox", stdout.strip())
            console.print(table)
            console.print(f"[bold green]✅ Success: {out_file}[/bold green]")
        else:
            console.print(f"[bold red]❌ Failed![/bold red]\n{stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", required=True)
    parser.add_argument("--b", required=True)
    parser.add_argument("--out", default="hybrid_genome.py")
    args = parser.parse_args()
    GEPMetaForge().run(args.a, args.b, args.out)
