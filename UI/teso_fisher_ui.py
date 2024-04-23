import logging
import threading
import tkinter
from multiprocessing import Process, Queue

import customtkinter

from tesoFisherConsole.teso_fisher_console import get_list_of_devices, get_peak_value, action, get_device_by_name, \
    DEVICE_NAME

peak_value = Queue(maxsize=0)

logger_teso_fisher_ui = logging.getLogger('teso_fisher_ui.py')
logger_teso_fisher_ui.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger_teso_fisher_ui.addHandler(ch)

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
    """
    create CTk window like you do with the Tk window
    """

    def __init__(self):
        super().__init__()

        # window title
        self.toplevel_window = None
        self.title("TESO Fisher UI.exe")

        # static window size
        self.width = 665
        self.height = 500
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        # static window level
        # self.wm_attributes('-topmost', 1)
        # self.after_idle(self.attributes, '-topmost', True)

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)

        # create logs
        self.label_frame = LabelFrame(master=self)
        self.label_frame.grid(row=3, column=0, padx=(20, 20), sticky="nsew")

        # create ComboBoxFrame frame
        self.combo_box_frame = ComboBoxFrame(master=self)
        self.combo_box_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create slider and progressbar frame
        self.slider_progressbar_frame = SliderFrame(master=self)
        self.slider_progressbar_frame.grid(row=1, column=0, padx=(20, 20), sticky="nsew")

        # create buttons
        self.buttons_frame = ButtonFrame(master=self)
        self.buttons_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # top level
        self.button_new_app = customtkinter.CTkButton(master=self.buttons_frame, text="->", fg_color="transparent",
                                                      border_width=2, text_color=("gray10", "#DCE4EE"), width=50,
                                                      command=self.button_new_app_press)
        self.button_new_app.grid(row=0, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def button_new_app_press(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Toplevel()  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


class ComboBoxFrame(customtkinter.CTkFrame):
    """
    Frame for list of devices
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_columnconfigure(1, weight=1)

        # text_box for frames
        self.label = customtkinter.CTkLabel(master=self, text="List of devices:")
        self.label.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="w")

        values = get_list_of_devices()
        values.remove(DEVICE_NAME)
        values.insert(0, DEVICE_NAME)

        self.combobox = customtkinter.CTkComboBox(master=self, values=values, width=500)
        self.combobox.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    def get_device(self):
        return get_device_by_name(self.combobox.get())


class SliderFrame(customtkinter.CTkFrame):
    VALUE = 45.000

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_columnconfigure(1, weight=1)

        # text_box for frames
        self.text_var = tkinter.StringVar(value=str(self.VALUE))
        self.slider_var = tkinter.DoubleVar(value=self.VALUE)
        self.label = customtkinter.CTkEntry(master=self, textvariable=self.text_var)
        self.label.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="w")
        self.label.focus_set()
        self.label.bind(['<Return>'], command=self.set_slider)

        self.slider = customtkinter.CTkSlider(self, orientation="horizontal", from_=0, to=100, command=self.set_label,
                                              variable=self.slider_var, width=400)
        self.slider.grid(row=0, column=1, rowspan=5, pady=(10, 10), sticky="ns")

    def set_label(self, event):
        self.text_var.set(str(float('%.3f' % event)))

    def set_slider(self, event):
        try:
            value = float(self.text_var.get())
            if value < 0:
                self.slider_var.set(0)
                self.text_var.set('0.00')
            elif value > 100:
                self.slider_var.set(100)
                self.text_var.set('100.00')
            else:
                self.slider_var.set(value)
        except ValueError:
            self.text_var.set(str(self.slider_var.get()))


class ButtonFrame(customtkinter.CTkFrame):
    BUTTON_ON = "blue"
    BUTTON_OFF = "transparent"

    __button_instances = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__class__.__button_instances.append(self)

        self.parent = self.master
        self.min_pv = None
        self.device = None
        self.get_peak_value_process = threading.Thread()
        self.state_get_peak_value_process = False

        self.grid_columnconfigure((0, 1), weight=1)

        self.button_start = customtkinter.CTkButton(master=self, text="START", fg_color="transparent", border_width=2,
                                                    text_color=("gray10", "#DCE4EE"), command=self.press_button_start)
        if Fisher.instances:
            self.button_start.configure(fg_color=self.BUTTON_ON)
        self.button_start.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.button_stop = customtkinter.CTkButton(master=self, text="STOP", fg_color="transparent", border_width=2,
                                                   text_color=("gray10", "#DCE4EE"), command=self.press_button_stop, )
        if not Fisher.instances:
            self.button_stop.configure(fg_color=self.BUTTON_ON)
        self.button_stop.grid(row=0, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def __del__(self):
        self.__class__.__button_instances.remove(self)

    def press_button_start(self):
        if Fisher.instances:
            self.press_button_stop()

        LabelFrame.write("Start:")
        self.device = self.parent.combo_box_frame.get_device()
        self.min_pv = float(self.parent.slider_progressbar_frame.text_var.get()) / 100

        LabelFrame.write(f"device - {self.device.name}\n"
              f"sensitive - {self.min_pv}")

        self.fishing = Fisher(args=(peak_value, self.min_pv, self.device.name), daemon=True)
        self.fishing.start()
        self.get_peak_value_process = threading.Thread(target=self.__get_peak_value, daemon=True)
        self.state_get_peak_value_process = True
        self.get_peak_value_process.start()
        self.switch_button(self.BUTTON_ON)

    def __get_peak_value(self):
        while self.state_get_peak_value_process:
            try:
                LabelFrame.write(f"fish: {peak_value.get()}")
            except:
                pass

    def press_button_stop(self):
        if Fisher.instances:
            for process in Fisher.instances:
                while process.is_alive():
                    process.terminate()
                Fisher.instances.remove(process)
                self.switch_button(self.BUTTON_OFF)
            LabelFrame.write(f"Stop\n")

    def switch_button(self, state):
        for inst in self.__class__.__button_instances:
            if state is self.BUTTON_ON:
                inst.button_start.configure(fg_color=self.BUTTON_ON)
                inst.button_stop.configure(fg_color=self.BUTTON_OFF)
            elif state is self.BUTTON_OFF:
                inst.button_start.configure(fg_color=self.BUTTON_OFF)
                inst.button_stop.configure(fg_color=self.BUTTON_ON)
            else:
                LabelFrame.write("ERROR")


class Toplevel(customtkinter.CTkToplevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title("TESO Fisher UI")

        # static window size
        self.width = 360
        self.height = 65
        self.minsize(self.width, self.height)
        self.maxsize(self.width, self.height)

        self.protocol('WM_DELETE_WINDOW', self.on_close)

        self.wm_attributes('-topmost', 1)
        self.after_idle(self.attributes, '-topmost', True)

        self.buttons_frame = ButtonFrame(master=self)
        self.buttons_frame.grid(row=2, column=0, sticky="nsew")

        self.buttons_frame.parent = self.master

    def on_close(self):
        self.destroy()
        self.buttons_frame.__del__()


class LabelFrame(customtkinter.CTkFrame):
    __instance = None

    @classmethod
    def get_instance(cls):
        return cls.__instance

    def __init__(self, master, **kwargs):
        if not LabelFrame.__instance:
            super().__init__(master, **kwargs)
            self.grid_columnconfigure(0, weight=1)

            self.text_box = customtkinter.CTkTextbox(master=self)
            self.text_box.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
            self.__class__.__instance = self

            # sys.stdout = TextWrapper(self.text_box)
            # sys.stdin = TextWrapper(self.text_box)
    @classmethod
    def write(cls, text: str):
        text_box = cls.__instance.text_box
        text_box.insert(customtkinter.END, text + '\n')
        text_box.see('end')


class Fisher(Process):
    instances = []

    def __init__(self, **kwargs):
        super().__init__(target=self.loop, **kwargs)
        self.__class__.instances.append(self)

    @staticmethod
    def loop(q, min_pv, dev_name):
        while True:
            val = get_peak_value(get_device_by_name(dev_name))
            if val >= min_pv:
                q.put(val)
                action()


if __name__ == "__main__":
    app = App()
    app.mainloop()
