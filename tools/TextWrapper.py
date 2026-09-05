import sys
from abc import ABC

import customtkinter


class TextWrapper(sys.stdout.__class__, ABC):
    text_field: customtkinter.CTkTextbox

    def __init__(self, text_field: customtkinter.CTkTextbox):
        self.text_field = text_field

    def write(self, text: str):
        self.text_field.insert(customtkinter.END, text)
        self.text_field.see('end')

    def flush(self):
        self.text_field.update()
