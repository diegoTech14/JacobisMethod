import fitz
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
from tkinter import BOTH, RIGHT, BOTTOM, LEFT, Y, messagebox


class JacobiDisplayApp():
    def __init__(self, master, app_instance):
        self.master = master
        self.app_instance = app_instance
        self.page_number = 0
        self.width_page = None
        self.height_page = None
        self.rendered_page = None

    def excel_jacobi_steps():
        column_names = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        workbook = openpyxl.Workbook()
        wb = workbook
        worksheet = wb.active
        for i,name in enumerate(column_names):
            worksheet[str(name)+str(count_rows)]  	=	str(excel_sheets[i])
        wb.save(filename = book)
        workbook.close()
