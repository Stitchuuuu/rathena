import yaml
import re
import argparse

def load_items(filepath):
    """Charge le fichier YAML et retourne la liste des items."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    # Le fichier a généralement une clé racine "Body"
    if isinstance(data, dict) and 'Body' in data:
        return data['Body']
    return data

def filter_items(items, job=None, script_pattern=None, job_must_be_true=True):
    """
    Filtre les items selon:
    - job: nom du job à chercher dans Jobs (ex: "Merchant")
    - script_pattern: regex/texte à chercher dans le champ Script (ex: "bMatkRate")
    - job_must_be_true: si True, vérifie que Jobs[job] == True
    """
    results = []

    for item in items:
        if item is None:
            continue

        # --- Filtre par Job ---
        if job:
            jobs = item.get('Jobs', {})
            job_value = jobs.get(job, False)
            if job_must_be_true and job_value is not True:
                continue
            if not job_must_be_true and job_value is not False:
                continue

        # --- Filtre par Script (texte brut ou regex) ---
        if script_pattern:
            script = item.get('Script', '')
            if script is None:
                script = ''
            if not re.search(script_pattern, script, re.IGNORECASE):
                continue

        results.append(item)

    return results

def print_results(items):
    """Affiche les résultats de façon lisible."""
    if not items:
        print("Aucun item trouvé.")
        return

    print(f"\n{len(items)} item(s) trouvé(s) :\n" + "-"*50)
    for item in items:
        print(f"ID: {item.get('Id')}")
        print(f"AegisName: {item.get('AegisName')}")
        print(f"Name: {item.get('Name')}")
        print(f"Type: {item.get('Type')} / SubType: {item.get('SubType', '-')}")
        jobs_true = [j for j, v in item.get('Jobs', {}).items() if v is True]
        print(f"Jobs: {', '.join(jobs_true) if jobs_true else 'Aucun'}")
        if item.get('Script'):
            print(f"Script:\n{item.get('Script').strip()}")
        print("-"*50)

def main():
    parser = argparse.ArgumentParser(description="Filtre les items RO par Jobs et Script")
    parser.add_argument("file", help="Chemin vers item_db_equip.yml")
    parser.add_argument("--job", help="Job requis (ex: Merchant, Swordman, Mage...)")
    parser.add_argument("--script", help="Texte ou regex à chercher dans Script (ex: bMatkRate)")
    parser.add_argument("--job-false", action="store_true",
                         help="Cherche les items où Job = false au lieu de true")

    args = parser.parse_args()

    items = load_items(args.file)
    filtered = filter_items(
        items,
        job=args.job,
        script_pattern=args.script,
        job_must_be_true=not args.job_false
    )
    print_results(filtered)

if __name__ == "__main__":
    main()
