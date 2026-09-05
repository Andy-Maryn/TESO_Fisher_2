# UI

**Директория:** `UI/`

## Назначение

GUI для управления текущим аудио-based рыболовным процессом. Интерфейс написан на `customtkinter` поверх Tkinter.

Основной файл: `UI/teso_fisher_ui.py`.

## Структура

- `App` — главное окно приложения.
- `ComboBoxFrame` — выбор аудиоустройства.
- `SliderFrame` — настройка sensitivity/threshold.
- `ButtonFrame` — запуск и остановка Fisher.
- `Toplevel` — дополнительное маленькое окно с кнопками START/STOP.
- `LabelFrame` — textbox для логов.
- `Fisher` — `multiprocessing.Process`, выполняющий audio detection loop.

## Запуск

Обычный entry point — `teso_fisher_main.py`, который создаёт `App` и запускает `mainloop()`.

```text
python teso_fisher_main.py
```

Также `UI/teso_fisher_ui.py` можно запускать напрямую.

## Жизненный цикл START

`ButtonFrame.press_button_start()`:

1. останавливает предыдущий Fisher, если он существует;
2. получает выбранное аудиоустройство через `ComboBoxFrame.get_device()`;
3. берёт значение slider и делит его на `100`;
4. создаёт `Fisher(args=(queue, min_pv, device.name), daemon=True)`;
5. запускает процесс;
6. запускает daemon-thread для отображения значений peak в логах;
7. переключает состояния кнопок.

## Жизненный цикл STOP

`press_button_stop()` проходит по `Fisher.instances`, вызывает `terminate()`, удаляет процесс из списка и переключает
UI.

### Что важно помнить

- Остановка процесса принудительная, graceful shutdown нет.
- Поток, читающий `peak_value`, не получает отдельного сигнала завершения.
- `Fisher.instances` — class-level список.
- Значение slider хранится как число 0..100, но в Fisher передаётся как 0..1.
- Интерфейс отображает «fish: <peak>», хотя значение фактически является peak level аудио, а не распознанной рыбой.

## `SliderFrame`

Начальное значение: `45.000`.

Диапазон: `0..100`.

Изменить значение можно как slider'ом, так и вручную через Entry. Enter вызывает `set_slider()` и ограничивает значение
диапазоном.

## `ComboBoxFrame`

Получает список render endpoints через `get_list_of_devices()`. Устройство `DEVICE_NAME` принудительно перемещается в
начало списка.

## Дополнительное окно

`Toplevel` создаётся кнопкой `->`. Оно содержит отдельный `ButtonFrame`, но использует parent главного окна для
устройства и threshold.

## Зависимости

`customtkinter`, `tkinter`, `threading`, `multiprocessing` и функции из `tesoFisherConsole.teso_fisher_console`.
