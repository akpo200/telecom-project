import json
import os
from datetime import datetime

LEADS_FILE = "lead_sniper/leads_db.json"

def save_leads(new_leads):
    """Sauvegarde les nouveaux leads en évitant les doublons."""
    if not os.path.exists(LEADS_FILE):
        existing_leads = []
    else:
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            try:
                existing_leads = json.load(f)
            except:
                existing_leads = []

    # On utilise le téléphone comme identifiant unique
    existing_tels = {l.get("telephone") for l in existing_leads if l.get("telephone")}
    
    added_count = 0
    for lead in new_leads:
        if lead.get("telephone") not in existing_tels:
            lead["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            existing_leads.append(lead)
            added_count += 1
            existing_tels.add(lead.get("telephone"))

    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_leads, f, indent=4, ensure_ascii=False)
    
    return added_count

def get_all_leads():
    """Récupère tous les leads stockés."""
    if not os.path.exists(LEADS_FILE):
        return []
    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []
