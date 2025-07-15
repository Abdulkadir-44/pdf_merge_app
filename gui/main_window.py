import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.pdf_operations import PDFOperations
from pathlib import Path

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF Birleştirici")
        self.geometry("520x420")
        self.resizable(False, False)

        self.ops = PDFOperations()
        self.selected_index = 0

        # --- Arayüz elemanları (kısaltılmış) ---
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=15)

        ctk.CTkButton(self.btn_frame, text="PDF'leri Seç",
                      command=self.select_pdfs, width=100).grid(row=0, column=0, padx=5)
        ctk.CTkButton(self.btn_frame, text="▲", width=40, command=self.move_up).grid(row=0, column=1, padx=5)
        ctk.CTkButton(self.btn_frame, text="▼", width=40, command=self.move_down).grid(row=0, column=2, padx=5)
        ctk.CTkButton(self.btn_frame, text="Kaldır", width=60,
                      fg_color="red", command=self.remove_selected).grid(row=0, column=3, padx=5)

        self.listbox = ctk.CTkTextbox(self, width=480, height=220)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Button-1>", self.on_click)
        self.listbox.bind("<Up>", self.on_key_up)
        self.listbox.bind("<Down>", self.on_key_down)

        ctk.CTkButton(self, text="Birleştir ve Kaydet",
                      command=self.merge_pdfs, width=200, height=40,
                      fg_color="green").pack(pady=15)

        self.update_listbox()

    # --- GUI olayları ---
    def select_pdfs(self):
        files = filedialog.askopenfilenames(title="PDF'leri Seç",
                                            filetypes=[("PDF Dosyaları", "*.pdf")])
        self.ops.add_files(files)
        self.selected_index = self.ops.count() - 1
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete("0.0", "end")
        for idx, name in enumerate(self.ops.basenames()):
            tag = "selected" if idx == self.selected_index else "normal"
            self.listbox.insert("end", name + "\n", tag)
        self.listbox.tag_config("selected", background="#3b82f6", foreground="white")
        self.listbox.tag_config("normal", background="", foreground="white")

    def on_click(self, event):
        index = int(self.listbox.index(f"@{event.x},{event.y}").split(".")[0]) - 1
        if 0 <= index < self.ops.count():
            self.selected_index = index
            self.update_listbox()

    def on_key_up(self, _):
        if self.selected_index > 0:
            self.selected_index -= 1
            self.update_listbox()

    def on_key_down(self, _):
        if self.selected_index < self.ops.count() - 1:
            self.selected_index += 1
            self.update_listbox()

    def move_up(self):
        self.ops.move_up(self.selected_index)
        self.selected_index = max(0, self.selected_index - 1)
        self.update_listbox()

    def move_down(self):
        self.ops.move_down(self.selected_index)
        self.selected_index = min(self.ops.count() - 1, self.selected_index + 1)
        self.update_listbox()

    def remove_selected(self):
        self.ops.remove_index(self.selected_index)
        self.selected_index = max(0, min(self.selected_index, self.ops.count() - 1))
        self.update_listbox()

    def merge_pdfs(self):
        if self.ops.count() == 0:
            messagebox.showwarning("Uyarı", "Hiç PDF seçilmedi!")
            return
        save_path = filedialog.asksaveasfilename(
            title="Kaydet",
            defaultextension=".pdf",
            filetypes=[("PDF Dosyası", "*.pdf")])
        if not save_path:
            return
        try:
            self.ops.merge(save_path)
            messagebox.showinfo("Başarılı", f"PDF'ler kaydedildi:\n{Path(save_path).name}")
        except Exception as e:
            messagebox.showerror("Hata", str(e))