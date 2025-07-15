from pathlib import Path
from typing import List
from PyPDF2 import PdfMerger

class PDFOperations:
    def __init__(self):
        self.files: List[Path] = []

    # --- CRUD işlemleri ---
    def add_files(self, paths: List[str]) -> None:
        self.files.extend(Path(p) for p in paths)

    def remove_index(self, index: int) -> None:
        if 0 <= index < len(self.files):
            self.files.pop(index)

    def move_up(self, index: int) -> None:
        if index > 0:
            self.files[index], self.files[index - 1] = self.files[index - 1], self.files[index]

    def move_down(self, index: int) -> None:
        if index < len(self.files) - 1:
            self.files[index], self.files[index + 1] = self.files[index + 1], self.files[index]

    # --- PDF birleştirme ---
    def merge(self, output_path: str) -> None:
        if not self.files:
            raise ValueError("Hiç PDF seçilmedi.")
        merger = PdfMerger()
        for pdf in self.files:
            merger.append(str(pdf))
        merger.write(output_path)
        merger.close()

    # --- Yardımcılar ---
    def basenames(self) -> List[str]:
        return [f.name for f in self.files]

    def count(self) -> int:
        return len(self.files)