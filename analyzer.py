import sys
from pathlib import Path

# Force Python à ajouter le dossier racine du projet dans ses chemins de recherche
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Import direct sans le point
from meters.clou_cl730d22l import CLOU_CL730D22L_MAP
METERS_DATABASE = {
    "CLOU CL730D22L": CLOU_CL730D22L_MAP
}

class StatusAnalyzer:
    @staticmethod
    def get_supported_meters():
        return list(METERS_DATABASE.keys())

    @staticmethod
    def get_obis_registers(meter_model: str):
        meter_map = METERS_DATABASE.get(meter_model, {})
        return {code: data["name"] for code, data in meter_map.items()}

    @staticmethod
    def analyze(meter_model: str, obis_code: str, raw_value: int):
        meter_map = METERS_DATABASE.get(meter_model, {})
        obis_data = meter_map.get(obis_code, {})
        
        bits_map = obis_data.get("bits", {})
        active_anomalies = []
        
        highest_severity = "INFO"
        severity_weight = {"INFO": 1, "WARNING": 2, "CRITICAL": 3}

        # Analyse bit par bit
        for bit_index in range(32): # Vérification jusqu'à 32 bits
            if (raw_value >> bit_index) & 1:
                if bit_index in bits_map:
                    anomaly = bits_map[bit_index].copy()
                    anomaly["bit"] = bit_index
                    active_anomalies.append(anomaly)
                    
                    # Mise à jour de la gravité globale
                    current_sev = anomaly.get("severity", "INFO")
                    if severity_weight.get(current_sev, 1) > severity_weight.get(highest_severity, 1):
                        highest_severity = current_sev
                else:
                    # Bit actif mais non documenté
                    active_anomalies.append({
                        "bit": bit_index,
                        "title": f"Bit {bit_index} Réservé / Inconnu",
                        "desc": "Ce bit est actif mais n'est pas défini dans la table d'interprétation.",
                        "severity": "INFO",
                        "action": "Consulter le manuel constructeur si le dysfonctionnement persiste."
                    })

        return {
            "total_detected": len(active_anomalies),
            "global_severity": highest_severity if active_anomalies else "OK",
            "anomalies": active_anomalies,
            "hex_repr": f"0x{raw_value:08X}",
            "bin_repr": f"0b{raw_value:032b}",
            "dec_repr": str(raw_value)
        }