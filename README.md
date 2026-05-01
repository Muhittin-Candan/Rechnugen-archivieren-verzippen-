# Rechnugen-archivieren-verzippen-
Das Script liest die PDF Rechungen nach bestimmen Schlüsselwörtern aus und verzippt/archiviert diese dann 

# PDF Keyword Analyzer & Auto-Zipper

Dieses Python-Skript durchsucht automatisch alle PDF-Dateien in einem Verzeichnis nach bestimmten buchhalterischen Schlüsselwörtern. Es generiert einen übersichtlichen CSV-Bericht über die gefundenen Begriffe und verpackt alle relevanten PDF-Dateien (solche mit mindestens einem Treffer) vollautomatisch in ein ZIP-Archiv.

## 🚀 Funktionen

* **Textanalyse:** Extrahiert Text aus PDFs und sucht nach den Begriffen "Bezahlt von", "Trinkgeld", "Flughafengebühr" und "Balance".
* **CSV-Reporting:** Erstellt die Datei `pdf_analysis.csv`, in der für jede analysierte PDF dokumentiert ist, welche Schlüsselwörter (markiert mit 'x') gefunden wurden.
* **Smart Zipping:** Erstellt automatisch ein Archiv namens `pdf_sammlung.zip`[cite: 2]. Dieses Archiv enthält *nur* die PDFs, in denen mindestens eines der Schlüsselwörter vorkommt[cite: 2] – ideal, um relevante Rechnungen schnell zu filtern und weiterzuleiten.

## 📋 Voraussetzungen

Das Skript benötigt Python und die Bibliothek `PyPDF2` für die PDF-Verarbeitung[cite: 2]. Alle anderen verwendeten Module (`os`, `re`, `csv`, `zipfile`) sind in der Python-Standardbibliothek enthalten[cite: 2].
