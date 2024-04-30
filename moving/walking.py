import keyboard


class Walking:
    hot_ket: str = "w"

    @classmethod
    def start(cls):
        if not keyboard.is_pressed(cls.hot_ket):
            keyboard.press(cls.hot_ket)

    @classmethod
    def stop(cls):
        if keyboard.is_pressed(cls.hot_ket):
            keyboard.release(cls.hot_ket)
