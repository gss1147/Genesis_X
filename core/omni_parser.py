import os
import pandas as pd
import logging
import warnings
import json
from bs4 import BeautifulSoup

# Suppress heavy library warnings
warnings.filterwarnings("ignore")

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniParser")

class OmniParser:
    def __init__(self):
        # Docling for advanced document layout analysis (Lazy load to save startup RAM)
        self.doc_converter = None

    def _get_docling(self):
        if self.doc_converter is None:
            try:
                from docling.document_converter import DocumentConverter
                self.doc_converter = DocumentConverter()
            except ImportError:
                logger.warning("Docling not found. PDF support limited.")
        return self.doc_converter

    def parse_file(self, file_path: str) -> str:
        """
        Ingests media and returns a dense semantic text block.
        """
        ext = os.path.splitext(file_path).[1]lower()
        logger.info(f"Ingesting {file_path} as {ext}")

        try:
            # --- Document Formats ---
            if ext in ['.pdf', '.docx', '.md', '.rtf']:
                return self._parse_doc(file_path)
            
            # --- Structured / Tabular Data ---
            elif ext in ['.csv', '.tsv']:
                return self._parse_csv(file_path)
            elif ext in ['.xlsx', '.xls', '.ods']:
                return self._parse_excel(file_path)
            
            # --- Code & Config ---
            elif ext in ['.json', '.xml', '.yaml', '.sql', '.toml', '.py', '.js', '.c', '.cpp', '.h']:
                return self._parse_code(file_path)

            # --- Web / Markup ---
            elif ext in ['.html', '.htm']:
                return self._parse_html(file_path)

            # --- Audio (Spectral Metadata) ---
            elif ext in ['.mp3', '.wav', '.flac', '.ogg', '.m4a']:
                return self._parse_audio_meta(file_path)
            
            # --- Text/Log ---
            elif ext in ['.txt', '.log', '.ini']:
                 with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            else:
                return f""

        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
            return f"[Omni-Parser Error] Could not parse file: {str(e)}"

    def _parse_doc(self, path):
        converter = self._get_docling()
        if converter and path.endswith('.pdf'):
            try:
                result = converter.convert(path)
                return result.document.export_to_markdown()
            except Exception as e:
                logger.error(f"Docling failed: {e}")
                
        # Fallback
        try:
            with open(path, 'rb') as f:
                import pypdf
                reader = pypdf.PdfReader(f)
                return "\n".join([page.extract_text() for page in reader.pages])
        except:
             with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()

    def _parse_csv(self, path):
        try:
            df = pd.read_csv(path)
            text_rep = f"Dataset Schema: {list(df.columns)}\n"
            text_rep += f"Shape: {df.shape}\nData Sample:\n"
            text_rep += df.head(10).to_markdown(index=False)
            return text_rep
        except:
            return "Error reading CSV"

    def _parse_excel(self, path):
        xls = pd.ExcelFile(path)
        text_rep = f"Spreadsheet Report ({len(xls.sheet_names)} sheets):\n"
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet)
            text_rep += f"\n--- Sheet: {sheet} ---\n"
            text_rep += df.head(5).to_markdown(index=False)
        return text_rep

    def _parse_html(self, path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')
            # Extract dense text, remove scripts/styles
            for script in soup(["script", "style"]):
                script.extract()
            return soup.get_text(separator='\n')

    def _parse_code(self, path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return f"File: {os.path.basename(path)}\n```\n{content}\n```"

    def _parse_audio_meta(self, path):
        # Lightweight Audio Analysis (No GPU)
        import librosa
        import numpy as np
        y, sr = librosa.load(path, duration=30)
        tempo, _ = librosa.feature.rhythm.tempo(y=y, sr=sr)
        duration = librosa.get_duration(y=y, sr=sr)
        rms = np.mean(librosa.feature.rms(y=y))
        return f"Audio Analysis:\nFilename: {os.path.basename(path)}\nDuration: {duration:.2f}s\nBPM: {tempo}\nEnergy/Volume: {rms:.4f}\n(Content requires GPU for full transcription)"
