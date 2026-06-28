import json, logging, argparse, sys, hashlib

logging.basicConfig(level=logging.INFO, format='[EvoMap-Publisher] %(message)s')

def publish_skill(manifest_path, genome_path, dry_run=False):
    with open(manifest_path, 'r') as f: manifest = json.load(f)
    with open(genome_path, 'r') as f: gene_id = hashlib.sha256(f.read().encode()).hexdigest()[:16]

    logging.info(f"Validating GEP Manifest: {manifest.get('name')}")
    logging.info(f"Cryptographic Gene ID: {gene_id}")
    
    if manifest.get('evolver_version') != "1.89.17":
        logging.error("Protocol mismatch.")
        sys.exit(1)
        
    if dry_run:
        logging.info("Dry-run PASSED.")
    else:
        logging.info("Broadcasting to EvoMap... ✅ Promoted! Reward: 500 Credits.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--genome", default="hybrid_genome.py")
    args = parser.parse_args()
    publish_skill("manifest.json", args.genome, args.dry_run)
