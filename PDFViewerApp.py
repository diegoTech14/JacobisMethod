import fitz
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
from tkinter import BOTH, RIGHT, BOTTOM, LEFT, Y, messagebox


class PDFViewerApp():
    def __init__(self, master, pdf_path, app_instance):
        self.master = master
        self.app_instance = app_instance
        self.page_number = 0
        self.width_page = None
        self.height_page = None
        self.rendered_page = None
        # CARGA EL DOCUMENTO PDF
        try:
            self.pdf_document = fitz.open(pdf_path)
        except FileNotFoundError as e:
            print("El archivo PDF no se encontró:", e)
        
        # CREA UN FRAME PARA LOS BOTONES
        self.button_frame = tk.Frame(master, background="white")
        self.button_frame.pack(side=BOTTOM, fill=BOTH)

        self.next_button = tk.Button(self.button_frame, text="\u2192", command=self.next_page,**self.app_instance.buttons_style)
        self.next_button.pack(side=RIGHT, ipadx=10)
        self.next_button.bind("<Enter>", lambda event: self.app_instance.in_cursor_btn(event, 1))
        self.next_button.bind("<Leave>", lambda event: self.app_instance.out_cursor_btn(event, 1))
        self.prev_button = tk.Button(self.button_frame, text="\u2190", command=self.prev_page,**self.app_instance.buttons_style)
        self.prev_button.pack(side=RIGHT, ipadx=10)
        self.prev_button.bind("<Enter>", lambda event: self.app_instance.in_cursor_btn(event, 1))
        self.prev_button.bind("<Leave>", lambda event: self.app_instance.out_cursor_btn(event, 1))

        self.menu_button = tk.Button(self.button_frame, text="\u2302 Volver al Menú Principal", command=self.go_to_menu,**self.app_instance.buttons_style)
        self.menu_button.pack(side=LEFT, ipadx=10)
        self.menu_button.bind("<Enter>", lambda event: self.app_instance.in_cursor_btn(event, 1))
        self.menu_button.bind("<Leave>", lambda event: self.app_instance.out_cursor_btn(event, 1))
        
        # CREA UN CANVAS PARA MOSTRAR EL PDF
        self.canvas = tk.Canvas(master, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=BOTH, expand=True)

        # CREA UN SCROLLBAR PARA EL CANVAS
        self.v_scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.canvas.yview)
        self.v_scrollbar.pack(side=RIGHT, fill=Y)
        
        # VINCULE EL SCROLLBAR AL CANVAS
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        # VINCULE EL EVENTO DE SCROLL DEL MOUSE AL CANVAS
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.load_pdf()
# ----------------------------------------------------------------------
    def next_page(self):
        self.page_number += 1
        self.load_pdf()   
# ----------------------------------------------------------------------
    def go_to_menu(self):
        self.app_instance.clear_widgets()
        self.app_instance.main_interface()
# ----------------------------------------------------------------------
    def prev_page(self):
        if self.page_number > 0:
            self.page_number -= 1
            self.load_pdf()
# ----------------------------------------------------------------------
    def load_pdf(self):
        # LIMPIA EL CANVAS
        self.canvas.delete("all")
        
        # VERIFICA QUE EL NÚMERO DE PÁGINA SEA VÁLIDO
        try:
            page = self.pdf_document.load_page(self.page_number)
        except ValueError:
            self.page_number -= 1
            page = self.pdf_document.load_page(self.page_number)
            messagebox.showinfo("Aviso", "Esta es la última página del documento")
               
        # CONVIERTE LA PÁGINA DEL PDF A UNA IMAGEN
        pix = page.get_pixmap()
        self.width_page = pix.width
        self.height_page = pix.height
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        # APLICA UN FILTRO DE SUAVIZADO A LA IMAGEN
        img_smoothed = img.filter(ImageFilter.DETAIL)
        self.rendered_page = ImageTk.PhotoImage(img_smoothed)

        # RENDERIZA LA IMAGEN EN EL CANVAS
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.rendered_page)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.master.geometry(f"{self.width_page}x580")
# ----------------------------------------------------------------------
    # MÉTODO PARA HACER SCROLL EN EL CANVAS
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")
