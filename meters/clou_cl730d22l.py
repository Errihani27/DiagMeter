"""
Dictionnaire de décodage complet pour le compteur CLOU CL730D22L
Registres OBIS supportés :
  - 1-0.0.96.5.0.255 : État d'opération
  - 1-0.0.96.5.1.255 : État d'auto-diagnostic
  - 1-0.0.96.5.2.255 : État de qualité d'alimentation
  - 1-0.0.96.5.3.255 : Tamper Indicator Status (Fraude & Inversions)
"""

CLOU_CL730D22L_MAP = {
    "1-0.0.96.5.0.255": {
        "name": "État d'opération",
        "bits": {
            0: {
                "title": "Mode d'usine",
                "desc": "Compteur en mode configuration / usine (fabrication).",
                "severity": "INFO",
                "action": "Utilisé uniquement lors de la fabrication ou des tests en laboratoire."
            },
            3: {
                "title": "Ouverture de relais",
                "desc": "Le relais de coupure interne est actuellement ouvert (client coupé ou déconnecté).",
                "severity": "WARNING",
                "action": "Vérifier le solde/abonnement ou envoyer une commande de fermeture du relais."
            }
        }
    },
    "1-0.0.96.5.1.255": {
        "name": "État d'auto-diagnostic",
        "bits": {
            0: {
                "title": "Compteur non calibré",
                "desc": "La calibration métrologique du compteur n'est pas effectuée ou est corrompue.",
                "severity": "CRITICAL",
                "action": "Remplacer le compteur ou effectuer une recalibration en laboratoire."
            },
            1: {
                "title": "Erreur de mesure",
                "desc": "Anomalie détectée au niveau du circuit intégré de mesure.",
                "severity": "CRITICAL",
                "action": "Contrôler le bon fonctionnement général et prévoir le remplacement si l'erreur persiste."
            },
            2: {
                "title": "Erreur NVM (Mémoire non volatile)",
                "desc": "Défaut de lecture/écriture dans la mémoire Flash/EEPROM.",
                "severity": "CRITICAL",
                "action": "Redémarrer le compteur. Si le défaut persiste, remplacer l'appareil."
            },
            3: {
                "title": "Erreur RAM",
                "desc": "Défaut dans la mémoire vive de travail du microcontrôleur.",
                "severity": "CRITICAL",
                "action": "Effectuer un cycle de mise hors tension/sous tension."
            },
            4: {
                "title": "Batterie faible",
                "desc": "La tension de la pile/batterie interne de sauvegarde est basse.",
                "severity": "WARNING",
                "action": "Planifier le remplacement de la batterie pour éviter la perte d'horloge en cas de coupure."
            },
            5: {
                "title": "Réinitialisation des anomalies du compteur",
                "desc": "Un RAZ (Reset) des registres d'anomalies a été exécuté.",
                "severity": "INFO",
                "action": "Vérifier si une intervention de maintenance récente a eu lieu."
            },
            6: {
                "title": "Ouverture de capot",
                "desc": "Le capot principal du compteur a été ouvert.",
                "severity": "WARNING",
                "action": "Inspecter les scellés du capot principal pour exclure une tentative de fraude."
            },
            7: {
                "title": "Ouverture de cache-borne",
                "desc": "Le capot protégeant le bornier électrique a été retiré.",
                "severity": "WARNING",
                "action": "Vérifier les scellés du cache-borne et l'état des connexions."
            },
            9: {
                "title": "Perturbation de champ magnétique",
                "desc": "Détection d'un champ magnétique externe anormal (ex: aimant).",
                "severity": "CRITICAL",
                "action": "Vérifier la présence d'un aimant à proximité du coffret et contrôler l'historique d'index."
            },
            13: {
                "title": "Défaut de relais",
                "desc": "Dysfonctionnement mécanique ou électronique de l'organe de coupure.",
                "severity": "CRITICAL",
                "action": "Tester la commande manuelle du relais. Remplacer si l'actionneur est bloqué."
            },
            16: {
                "title": "Enlèvement de batterie remplaçable",
                "desc": "La batterie extractible a été retirée du logement.",
                "severity": "WARNING",
                "action": "Remettre une batterie neuve en place."
            },
            17: {
                "title": "Ouverture de couvercle de module",
                "desc": "Le capot du module de communication (PLC/GPRS/RF) est ouvert.",
                "severity": "WARNING",
                "action": "Vérifier la fixation du module de communication et ses scellés."
            },
            18: {
                "title": "Ajustement de neutre manquant non fini",
                "desc": "La procédure d'ajustement/compensation de neutre est incomplète.",
                "severity": "WARNING",
                "action": "Relancer la procédure de configuration de la mesure sur le neutre."
            },
            20: {
                "title": "Dépassement de charge normal",
                "desc": "La puissance appelée dépasse le seuil souscrit autorisé.",
                "severity": "WARNING",
                "action": "Vérifier la courbe de charge et ajuster la puissance souscrite au contrat si besoin."
            },
            21: {
                "title": "Dépassement de charge d'urgence",
                "desc": "La puissance appelée dépasse le seuil critique d'urgence défini.",
                "severity": "CRITICAL",
                "action": "Délester des charges immédiatement pour éviter le déclenchement du relais."
            }
        }
    },
    "1-0.0.96.5.2.255": {
        "name": "État de qualité d'alimentation",
        "bits": {
            0: {
                "title": "Haute tension sur toutes les phases",
                "desc": "Surtension globale sur les trois phases.",
                "severity": "CRITICAL",
                "action": "Mesurer la tension aux bornes et alerter l'exploitant du réseau HT/BT."
            },
            1: {
                "title": "Haute tension L1",
                "desc": "Surtension mesurée sur la phase 1.",
                "severity": "WARNING",
                "action": "Vérifier la tension entre L1 et Neutre."
            },
            2: {
                "title": "Haute tension L2",
                "desc": "Surtension mesurée sur la phase 2.",
                "severity": "WARNING",
                "action": "Vérifier la tension entre L2 et Neutre."
            },
            3: {
                "title": "Haute tension L3",
                "desc": "Surtension mesurée sur la phase 3.",
                "severity": "WARNING",
                "action": "Vérifier la tension entre L3 et Neutre."
            },
            4: {
                "title": "Sous-tension sur toutes les phases",
                "desc": "Baisse de tension généralisée sous le seuil minimal.",
                "severity": "CRITICAL",
                "action": "Contrôler la charge du départ et l'état du transformateur."
            },
            5: {
                "title": "Sous-tension L1",
                "desc": "Sous-tension mesurée sur la phase 1.",
                "severity": "WARNING",
                "action": "Mesurer la tension L1-N et vérifier l'équilibrage des charges."
            },
            6: {
                "title": "Sous-tension L2",
                "desc": "Sous-tension mesurée sur la phase 2.",
                "severity": "WARNING",
                "action": "Mesurer la tension L2-N et vérifier l'équilibrage des charges."
            },
            7: {
                "title": "Sous-tension L3",
                "desc": "Sous-tension mesurée sur la phase 3.",
                "severity": "WARNING",
                "action": "Mesurer la tension L3-N et vérifier l'équilibrage des charges."
            },
            8: {
                "title": "Perte de tension L1",
                "desc": "Absence totale de tension sur la phase 1.",
                "severity": "CRITICAL",
                "action": "Vérifier le fusible amont ou la continuité du câble L1."
            },
            9: {
                "title": "Perte de tension L2",
                "desc": "Absence totale de tension sur la phase 2.",
                "severity": "CRITICAL",
                "action": "Vérifier le fusible amont ou la continuité du câble L2."
            },
            10: {
                "title": "Perte de tension L3",
                "desc": "Absence totale de tension sur la phase 3.",
                "severity": "CRITICAL",
                "action": "Vérifier le fusible amont ou la continuité du câble L3."
            },
            11: {
                "title": "Perte de phase L1",
                "desc": "Disparition du signal de phase L1.",
                "severity": "CRITICAL",
                "action": "Inspecter les raccordements et le coupe-circuit de la phase 1."
            },
            12: {
                "title": "Perte de phase L2",
                "desc": "Disparition du signal de phase L2.",
                "severity": "CRITICAL",
                "action": "Inspecter les raccordements et le coupe-circuit de la phase 2."
            },
            13: {
                "title": "Perte de phase L3",
                "desc": "Disparition du signal de phase L3.",
                "severity": "CRITICAL",
                "action": "Inspecter les raccordements et le coupe-circuit de la phase 3."
            },
            14: {
                "title": "Défaut de fréquence",
                "desc": "Fréquence réseau hors de la plage tolérée (50 Hz ± delta).",
                "severity": "WARNING",
                "action": "Mesurer la fréquence réseau et vérifier s'il y a un groupe électrogène en service."
            },
            15: {
                "title": "Tension normale L1",
                "desc": "La tension de la phase 1 est dans sa plage nominale.",
                "severity": "INFO",
                "action": "Aucune action requise."
            },
            16: {
                "title": "Tension normale L2",
                "desc": "La tension de la phase 2 est dans sa plage nominale.",
                "severity": "INFO",
                "action": "Aucune action requise."
            },
            17: {
                "title": "Tension normale L3",
                "desc": "La tension de la phase 3 est dans sa plage nominale.",
                "severity": "INFO",
                "action": "Aucune action requise."
            },
            24: {
                "title": "Hors tension",
                "desc": "Le compteur est actuellement hors tension ou alimenté sur secours.",
                "severity": "CRITICAL",
                "action": "Vérifier l'alimentation principale du coffret."
            }
        }
    },
    "1-0.0.96.5.3.255": {
        "name": "Tamper Indicator Status (Fraudes / Inversions)",
        "bits": {
            0: {
                "title": "Ouverture de capot",
                "desc": "Événement de fraude : le capot principal a été ouvert.",
                "severity": "WARNING",
                "action": "Inspecter les scellés et dresser un constat d'intervention."
            },
            1: {
                "title": "Ouverture de cache-borne",
                "desc": "Événement de fraude : le cache-borne a été retiré.",
                "severity": "WARNING",
                "action": "Inspecter les scellés de bornier et vérifier la présence de shunts."
            },
            2: {
                "title": "Déséquilibre de courant",
                "desc": "Écart significatif entre les courants de phase ou entre phase et neutre.",
                "severity": "WARNING",
                "action": "Rechercher un piquage sauvage, une fuite à la terre ou un shunt de TC."
            },
            4: {
                "title": "Perturbation de champ magnétique",
                "desc": "Attempt de fraude par aimant puissant externe.",
                "severity": "CRITICAL",
                "action": "Contrôler l'environnement immédiat du compteur et vérifier l'intégrité de la mesure."
            },
            5: {
                "title": "Courant inverse sur toutes les phases",
                "desc": "Inversion du sens d'énergie sur l'ensemble des trois phases.",
                "severity": "CRITICAL",
                "action": "Vérifier le sens de câblage des trois Transformateurs de Courant (P1/P2 - S1/S2)."
            },
            6: {
                "title": "L1 Courant inverse",
                "desc": "Inversion du sens du courant sur la phase 1.",
                "severity": "CRITICAL",
                "action": "Inverser le sens de raccordement du TC ou des bornes d'entrée/sortie de la phase 1."
            },
            7: {
                "title": "L2 Courant inverse",
                "desc": "Inversion du sens du courant sur la phase 2.",
                "severity": "CRITICAL",
                "action": "Inverser le sens de raccordement du TC ou des bornes d'entrée/sortie de la phase 2."
            },
            8: {
                "title": "L3 Courant inverse",
                "desc": "Inversion du sens du courant sur la phase 3.",
                "severity": "CRITICAL",
                "action": "Inverser le sens de raccordement du TC ou des bornes d'entrée/sortie de la phase 3."
            },
            13: {
                "title": "Surintensité sur toutes les phases",
                "desc": "Courant mesuré dépassant la limite de sécurité sur les trois phases.",
                "severity": "CRITICAL",
                "action": "Contrôler immédiatement la charge totale de l'installation."
            },
            14: {
                "title": "L1 Surintensité",
                "desc": "Dépassement du seuil de courant sur la phase 1.",
                "severity": "WARNING",
                "action": "Mesurer le courant de la phase L1 à la pince ampèremétrique."
            },
            15: {
                "title": "L2 Surintensité",
                "desc": "Dépassement du seuil de courant sur la phase 2.",
                "severity": "WARNING",
                "action": "Mesurer le courant de la phase L2 à la pince ampèremétrique."
            },
            16: {
                "title": "L3 Surintensité",
                "desc": "Dépassement du seuil de courant sur la phase 3.",
                "severity": "WARNING",
                "action": "Mesurer le courant de la phase L3 à la pince ampèremétrique."
            },
            17: {
                "title": "Erreur de séquence de phase",
                "desc": "Ordre des phases incorrect (ex: L1-L3-L2 au lieu de L1-L2-L3).",
                "severity": "WARNING",
                "action": "Vérifier l'ordre de succession des phases à l'aide d'un ordre-mètre."
            },
            18: {
                "title": "Déséquilibre de tension",
                "desc": "Écart important entre les niveaux de tension des phases.",
                "severity": "WARNING",
                "action": "Contrôler les tensions simples et composées du réseau."
            },
            25: {
                "title": "Ouverture de couvercle de module",
                "desc": "Le capot du module de communication a été démonté.",
                "severity": "WARNING",
                "action": "Inspecter la fixation et le scellé du module amovible."
            },
            26: {
                "title": "Neutre manquant",
                "desc": "Absence de référence de neutre au niveau du bornier de mesure.",
                "severity": "CRITICAL",
                "action": "Vérifier immédiatement le raccordement du conducteur de neutre au compteur."
            }
        }
    }
}