import keyboard


class Walking:
    hot_ket: str = "w"

    @classmethod
    def start(cls):
        keyboard.press(cls.hot_ket)

    @classmethod
    def stop(cls):
        keyboard.release(cls.hot_ket)
