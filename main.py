import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QFrame, QScrollArea,
    QListWidget, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from utils import detect_and_clean_format
from analyzer import StatusAnalyzer

# --- FEUILLE DE STYLE QSS (Thème Sombre Material) ---
STYLE_SHEET = """
QMainWindow {
    background-color: #1E1E2E;
}
QLabel {
    color: #E0E0E0;
    font-family: 'Segoe UI', sans-serif;
}
QFrame#TopBar {
    background-color: #11111B;
    border-bottom: 2px solid #313244;
}
QFrame#Card {
    background-color: #181825;
    border-radius: 8px;
    border: 1px solid #313244;
    padding: 12px;
}
QComboBox {
    background-color: #313244;
    color: #FFFFFF;
    border: 1px solid #45475A;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
}
QComboBox::drop-down {
    border: none;
}
QLineEdit {
    background-color: #313244;
    color: #FFFFFF;
    border: 1px solid #45475A;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
}
QPushButton {
    background-color: #89B4FA;
    color: #11111B;
    font-weight: bold;
    border-radius: 6px;
    padding: 9px 16px;
    font-size: 13px;
}
QPushButton:hover {
    background-color: #B4BEFE;
}
QPushButton#SecondaryButton {
    background-color: #45475A;
    color: #CDD6F4;
}
QPushButton#SecondaryButton:hover {
    background-color: #585B70;
}
QScrollArea {
    border: none;
    background-color: transparent;
}
"""

class StatusAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CLOU Status Analyzer Pro v1.0")
        self.resize(1100, 750)
        self.setStyleSheet(STYLE_SHEET)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. En-tête (Top Bar)
        top_bar = QFrame()
        top_bar.setObjectName("TopBar")
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(20, 15, 20, 15)
        
        app_title = QLabel("⚡ CLOU Status Analyzer Pro")
        app_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        top_bar_layout.addWidget(app_title)
        top_bar_layout.addStretch()
        
        subtitle = QLabel("Plateforme de Diagnostic pour Compteurs Intelligents")
        subtitle.setStyleSheet("color: #A6ADC8;")
        top_bar_layout.addWidget(subtitle)
        
        main_layout.addWidget(top_bar)

        # 2. Zone principale (Panneaux Gauche / Droit)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # --- PANNEAU GAUCHE : Sélections & Saisie ---
        left_panel = QVBoxLayout()
        left_panel.setSpacing(15)

        # Carte Sélecteurs (Compteur & Registre OBIS)
        select_card = QFrame()
        select_card.setObjectName("Card")
        select_layout = QVBoxLayout(select_card)

        select_layout.addWidget(QLabel("Modèle de Compteur :"))
        self.combo_meter = QComboBox()
        self.combo_meter.addItems(StatusAnalyzer.get_supported_meters())
        self.combo_meter.currentTextChanged.connect(self.on_meter_changed)
        select_layout.addWidget(self.combo_meter)

        select_layout.addWidget(QLabel("Registre OBIS :"))
        self.combo_obis = QComboBox()
        select_layout.addWidget(self.combo_obis)

        left_panel.addWidget(select_card)

        # Carte Saisie du Mot d'État
        input_card = QFrame()
        input_card.setObjectName("Card")
        input_layout = QVBoxLayout(input_card)

        input_layout.addWidget(QLabel("Mot d'état (HEX, BIN ou DEC) :"))
        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("Ex: 0x0019, 11001b, 25...")
        self.txt_input.returnPressed.connect(self.run_analysis)
        
        # 🔴 Connexion du signal pour passer le champ en ROUGE si >= 8 caractères
        self.txt_input.textChanged.connect(self.on_input_text_changed)
        
        input_layout.addWidget(self.txt_input)

        # Boutons d'action
        btn_layout = QHBoxLayout()
        btn_paste = QPushButton("Coller")
        btn_paste.setObjectName("SecondaryButton")
        btn_paste.clicked.connect(self.paste_input)
        
        btn_clear = QPushButton("Effacer")
        btn_clear.setObjectName("SecondaryButton")
        btn_clear.clicked.connect(self.clear_all)

        btn_analyze = QPushButton("Traduire / Analyser")
        btn_analyze.clicked.connect(self.run_analysis)

        btn_layout.addWidget(btn_paste)
        btn_layout.addWidget(btn_clear)
        btn_layout.addWidget(btn_analyze)
        input_layout.addLayout(btn_layout)

        left_panel.addWidget(input_card)

        # Carte Historique de session
        history_card = QFrame()
        history_card.setObjectName("Card")
        history_layout = QVBoxLayout(history_card)
        history_layout.addWidget(QLabel("Historique Récent"))
        
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("background: transparent; border: none; color: #CDD6F4;")
        self.history_list.itemClicked.connect(self.load_from_history)
        history_layout.addWidget(self.history_list)

        left_panel.addWidget(history_card)
        content_layout.addLayout(left_panel, stretch=1)

        # --- PANNEAU DROIT : Résultats & Diagnostic ---
        right_panel = QVBoxLayout()

        # Carte Résumé Global
        self.summary_card = QFrame()
        self.summary_card.setObjectName("Card")
        summary_layout = QVBoxLayout(self.summary_card)

        self.lbl_diagnostic = QLabel("Saisissez une valeur pour démarrer l'analyse.")
        self.lbl_diagnostic.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        summary_layout.addWidget(self.lbl_diagnostic)

        self.lbl_conversions = QLabel("HEX: - | BIN: - | DEC: -")
        self.lbl_conversions.setStyleSheet("color: #BAC2DE;")
        summary_layout.addWidget(self.lbl_conversions)

        right_panel.addWidget(self.summary_card)

        # Zone Scrollable pour l'affichage des cartes d'alarme
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.results_container)

        right_panel.addWidget(self.scroll_area, stretch=1)

        content_layout.addLayout(right_panel, stretch=2)
        main_layout.addLayout(content_layout)

        # Charger la liste OBIS du premier compteur au démarrage
        self.on_meter_changed(self.combo_meter.currentText())

    def on_input_text_changed(self, text: str):
        """
        Passe le champ de saisie en ROUGE si la longueur du texte est >= 8 caractères.
        """
        if len(text.strip()) >= 8:
            self.txt_input.setStyleSheet("""
                QLineEdit {
                    background-color: #2A1519;
                    color: #FF5555;
                    border: 2px solid #FF3333;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
        else:
            self.txt_input.setStyleSheet("""
                QLineEdit {
                    background-color: #313244;
                    color: #FFFFFF;
                    border: 1px solid #45475A;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-size: 14px;
                }
            """)

    def on_meter_changed(self, meter_name):
        self.combo_obis.clear()
        obis_dict = StatusAnalyzer.get_obis_registers(meter_name)
        for code, name in obis_dict.items():
            self.combo_obis.addItem(f"{code} - {name}", userData=code)

    def paste_input(self):
        clipboard = QApplication.clipboard()
        self.txt_input.setText(clipboard.text())

    def clear_all(self):
        self.txt_input.clear()
        self.lbl_diagnostic.setText("Saisissez une valeur pour démarrer l'analyse.")
        self.lbl_conversions.setText("HEX: - | BIN: - | DEC: -")
        self.clear_results()

    def clear_results(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def run_analysis(self):
        raw_text = self.txt_input.text()
        if not raw_text.strip():
            return

        try:
            val_int, detected_fmt = detect_and_clean_format(raw_text)
        except ValueError as e:
            QMessageBox.critical(self, "Erreur de format", str(e))
            return

        meter_model = self.combo_meter.currentText()
        obis_code = self.combo_obis.currentData()

        # Moteur d'analyse
        report = StatusAnalyzer.analyze(meter_model, obis_code, val_int)

        # Mise à jour du résumé supérieur
        self.update_summary(report, detected_fmt)

        # Affichage des cartes d'anomalies
        self.clear_results()
        if report["total_detected"] == 0:
            no_alarm = QLabel("✅ Aucune anomalie ni alarme détectée pour ce mot d'état.")
            no_alarm.setStyleSheet("color: #A6E3A1; font-size: 14px; padding: 20px;")
            self.results_layout.addWidget(no_alarm)
        else:
            for anomaly in report["anomalies"]:
                card = self.create_anomaly_card(anomaly)
                self.results_layout.addWidget(card)

        # Ajout à l'historique
        hist_item = f"[{report['hex_repr']}] {obis_code} - {report['total_detected']} alarme(s)"
        self.history_list.insertItem(0, hist_item)

    def update_summary(self, report, detected_fmt):
        sev = report["global_severity"]
        count = report["total_detected"]
        
        colors = {
            "OK": "#A6E3A1",
            "INFO": "#89B4FA",
            "WARNING": "#FAB387",
            "CRITICAL": "#F38BA8"
        }
        color = colors.get(sev, "#E0E0E0")

        msg = f"Diagnostic : {count} Anomalie(s) active(s) | Niveau global : {sev}"
        self.lbl_diagnostic.setText(msg)
        self.lbl_diagnostic.setStyleSheet(f"color: {color}; font-size: 14px; font-weight: bold;")
        
        conv_text = f"Format détecté : {detected_fmt}  |  HEX: {report['hex_repr']}  |  BIN: {report['bin_repr']}  |  DEC: {report['dec_repr']}"
        self.lbl_conversions.setText(conv_text)

    def create_anomaly_card(self, anomaly):
        card = QFrame()
        card.setObjectName("Card")
        
        border_colors = {"INFO": "#89B4FA", "WARNING": "#FAB387", "CRITICAL": "#F38BA8"}
        sev_color = border_colors.get(anomaly['severity'], "#45475A")
        card.setStyleSheet(f"QFrame#Card {{ border-left: 5px solid {sev_color}; }}")

        layout = QVBoxLayout(card)
        
        # Titre & Badge de gravité
        header = QHBoxLayout()
        title = QLabel(f"Bit {anomaly['bit']} : {anomaly['title']}")
        title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        
        badge = QLabel(f" {anomaly['severity']} ")
        badge.setStyleSheet(f"background-color: {sev_color}; color: #11111B; font-weight: bold; border-radius: 4px;")

        header.addWidget(title)
        header.addStretch()
        header.addWidget(badge)
        layout.addLayout(header)

        # Description de l'anomalie
        desc = QLabel(anomaly["desc"])
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #CDD6F4; margin-top: 4px;")
        layout.addWidget(desc)

        # Action / Recommandation terrain
        if "action" in anomaly:
            action = QLabel(f"💡 Recommandation : {anomaly['action']}")
            action.setWordWrap(True)
            action.setStyleSheet("color: #A6E3A1; font-size: 12px; margin-top: 6px;")
            layout.addWidget(action)

        return card

    def load_from_history(self, item):
        # Récupère la valeur HEX depuis l'historique
        hex_val = item.text().split("]")[0].replace("[", "")
        self.txt_input.setText(hex_val)
        self.run_analysis()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StatusAnalyzerApp()
    window.show()
    sys.exit(app.exec())