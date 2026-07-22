import re

def detect_and_clean_format(value_str: str):
    """
    Détecte le format de la valeur fournie (HEX, BIN, DEC) et retourne la valeur en int.
    Exemples acceptés : "0x0019", "19h", "0b11001", "11001b", "25", " 1001 "
    """
    clean_val = value_str.strip().lower()
    if not clean_val:
        raise ValueError("Le champ de saisie est vide.")

    # Format Hexadécimal (0x..., ...h)
    if clean_val.startswith("0x") or clean_val.endswith("h"):
        hex_str = clean_val.replace("0x", "").rstrip("h")
        return int(hex_str, 16), "HEX"
    
    # Format Binaire (0b..., ...b)
    if clean_val.startswith("0b") or clean_val.endswith("b"):
        bin_str = clean_val.replace("0b", "").rstrip("b")
        return int(bin_str, 2), "BIN"
    
    # Vérification si binaire pur (que des 0 et 1 d'au moins 4 bits)
    if set(clean_val).issubset({"0", "1"}) and len(clean_val) >= 4:
        return int(clean_val, 2), "BIN"

    # Essai en Hexadécimal si contient A-F
    if re.search(r'[a-f]', clean_val):
        return int(clean_val, 16), "HEX"

    # Par défaut : Décimal
    try:
        return int(clean_val, 10), "DEC"
    except ValueError:
        raise ValueError("Format numérique invalide (non reconnu comme HEX, BIN ou DEC).")