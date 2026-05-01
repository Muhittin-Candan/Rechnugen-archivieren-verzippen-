import os
import re
import csv
import zipfile
import PyPDF2

def extract_text_from_pdf(pdf_path):
    """Extrahiert Text aus einer PDF-Datei."""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"Fehler beim Lesen von {pdf_path}: {e}")
    return text

def analyze_pdf_content(text):
    """Analysiert den Text auf die gesuchten Schlüsselwörter."""
    # Konvertiere zu Kleinbuchstaben für case-insensitive Suche
    text_lower = text.lower()
    
    # Definiere die Suchmuster
    patterns = {
        'Bezahlt von': r'bezahlt von',
        'Trinkgeld': r'trinkgeld',
        'Flughafengebühr': r'flughafengebühr',
        'Balance': r'balance'
    }
    
    results = {}
    for key, pattern in patterns.items():
        # Suche nach dem Pattern (case-insensitive)
        if re.search(pattern, text_lower):
            results[key] = 'x'
        else:
            results[key] = ''
    
    return results

def create_zip_with_pdfs(pdf_files, zip_name='pdf_sammlung.zip'):
    """Erstellt ein ZIP-Archiv mit ausgewählten PDF-Dateien."""
    if not pdf_files:
        print("Keine PDF-Dateien zum Verpacken gefunden.")
        return None
    
    try:
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf_file in pdf_files:
                if os.path.exists(pdf_file):
                    zipf.write(pdf_file, os.path.basename(pdf_file))
                    print(f"Hinzugefügt: {pdf_file}")
                else:
                    print(f"Warnung: Datei nicht gefunden: {pdf_file}")
        
        print(f"\nZIP-Archiv '{zip_name}' wurde erfolgreich erstellt.")
        print(f"Enthaltene Dateien: {len(pdf_files)}")
        return zip_name
    except Exception as e:
        print(f"Fehler beim Erstellen des ZIP-Archivs: {e}")
        return None

def main():
    # Verzeichnis mit PDF-Dateien (aktuelles Verzeichnis)
    pdf_directory = '.'
    
    # Liste für die Ergebnisse
    csv_data = []
    
    # Liste für PDF-Dateien, die verpackt werden sollen
    pdf_files_to_zip = []
    
    # Header für CSV
    header = ['PDF Name', 'Bezahlt von', 'Trinkgeld', 'Flughafengebühr', 'Balance']
    csv_data.append(header)
    
    # Durchsuche alle PDF-Dateien im Verzeichnis
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("Keine PDF-Dateien im aktuellen Verzeichnis gefunden.")
        return
    
    for filename in pdf_files:
        # Dateiname ohne .pdf-Endung
        pdf_name = os.path.splitext(filename)[0]
        
        # Vollständiger Pfad zur PDF-Datei
        pdf_path = os.path.join(pdf_directory, filename)
        
        # Text aus PDF extrahieren
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            # Analyse des Textes
            results = analyze_pdf_content(text)
            
            # Prüfe, ob mindestens ein Schlüsselwort gefunden wurde
            has_keyword = any(value == 'x' for value in results.values())
            
            # Nur wenn ein Schlüsselwort gefunden wurde, zur ZIP-Liste hinzufügen
            if has_keyword:
                pdf_files_to_zip.append(pdf_path)
                print(f"PDF enthält Schlüsselwort: {filename}")
            
            # Erstelle eine Zeile für die CSV-Datei
            row = [
                pdf_name,
                results.get('Bezahlt von', ''),
                results.get('Trinkgeld', ''),
                results.get('Flughafengebühr', ''),
                results.get('Balance', '')
            ]
            csv_data.append(row)
        else:
            # Wenn kein Text extrahiert werden konnte
            row = [pdf_name, '', '', '', '']
            csv_data.append(row)
            print(f"Kein Text extrahiert aus: {filename}")
    
    # CSV-Datei schreiben
    output_csv = 'pdf_analysis.csv'
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
    
    print(f"\nCSV-Datei '{output_csv}' wurde erfolgreich erstellt.")
    print(f"Es wurden {len(pdf_files)} PDF-Dateien analysiert.")
    
    # ZIP-Archiv erstellen (nur mit PDFs, die Schlüsselwörter enthalten)
    print("\n" + "="*50)
    print("Erstelle ZIP-Archiv mit PDFs, die Schlüsselwörter enthalten...")
    print("="*50)
    
    if pdf_files_to_zip:
        zip_file_name = 'pdf_sammlung.zip'
        create_zip_with_pdfs(pdf_files_to_zip, zip_file_name)
        
        # Optional: ZIP-Archiv-Info anzeigen
        if os.path.exists(zip_file_name):
            zip_size = os.path.getsize(zip_file_name) / 1024  # Größe in KB
            print(f"\nZIP-Archiv Größe: {zip_size:.2f} KB")
    else:
        print("Keine PDF-Dateien mit Schlüsselwörtern gefunden. ZIP-Archiv wird nicht erstellt.")

if __name__ == "__main__":
    main()