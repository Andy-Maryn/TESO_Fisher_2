import multiprocessing

from UI.teso_fisher_ui import App

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = App()
    app.mainloop()
