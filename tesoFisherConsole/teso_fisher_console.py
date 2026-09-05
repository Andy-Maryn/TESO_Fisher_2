import argparse
import logging
import time
from typing import Any

import keyboard
import pyWinCoreAudio

logger = logging.getLogger('teso_fisher_console.py')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)

DEVICE_NAME = "Динамики (Realtek(R) Audio)"
MIN_PEAK_VOLUME = 0.45


def parser() -> argparse.Namespace:
    pars = argparse.ArgumentParser(description='TESO-fisher')
    pars.add_argument('--device_name', type=str, default=None,
                      help='device name (default: "Динамики (Realtek(R) Audio)")')
    pars.add_argument('--device_id', type=str, default=None,
                      help='device id (default: "Динамики (Realtek(R) Audio)")')
    pars.add_argument('--min_peak_volume', type=float, default=None,
                      help='min peak volume (default: 0; min: 0; max: 99)')
    pars.add_argument('--log', type=bool, nargs='?', default=False,
                      help='write logs in file "logs.txt" (default: do not write')
    if pars.parse_args().log is not False:
        logging.basicConfig(level=logging.INFO, filename="logs.txt", filemode="w")
        logger.info(f"Start writing logs")
    return pars.parse_args()


def get_args(args: argparse.Namespace) -> tuple[Any, Any]:
    if args.device_id is not None:
        dev = get_device_by_id(args.device_id)
    elif args.device_name is not None:
        dev = get_device_by_name(args.device_name)
    else:
        dev = get_device_by_name(DEVICE_NAME)

    if type(args.min_peak_volume) in [int, float]:
        if 0 < args.min_peak_volume < 99 and type(args.min_peak_volume) in [int, float]:
            min_pv = args.min_peak_volume / 100
        else:
            min_pv = MIN_PEAK_VOLUME
    else:
        min_pv = MIN_PEAK_VOLUME
    return dev, min_pv


def get_list_of_devices() -> list:
    logger.info(f"----------------------------------")
    logger.info(f"List of devices:")
    device_list = []
    for n, d in enumerate(pyWinCoreAudio.AudioDevices):
        for rep in d.render_endpoints:
            if rep.form_factor in ["Headphones", "Speakers"]:
                logger.info(f"render endpoint {n}, id({rep.id}): {rep.name} is a {rep.form_factor}")
                device_list.append(rep.name)
    return device_list


def get_device_by_name(name: str) -> Any:
    for n, d in enumerate(pyWinCoreAudio.AudioDevices):
        for rep in d.render_endpoints:
            if rep.name == name:
                return rep
    logger.error(f"wrong name: {name}")
    exit()


def get_device_by_id(dev_id: Any) -> Any:
    for n, d in enumerate(pyWinCoreAudio.AudioDevices):
        for rep in d.render_endpoints:
            if dev_id in rep.id:
                return rep
    logger.error(f"wrong id: {dev_id}")
    exit()


def get_peak_value(dev: Any) -> float:
    return dev.volume.peak_meter.peak_value


def action() -> None:
    keyboard.send("e")
    time.sleep(1)
    keyboard.send("e")


def loop(dev: Any, min_pv: float):
    while True:
        if get_peak_value(dev) >= min_pv:
            logger.info(f"fish: {get_peak_value(dev)}")
            action()


if __name__ == "__main__":
    pars = parser()
    get_list_of_devices()
    device, min_peak_volume = get_args(pars)

    logger.info(f"----------------------------------")
    logger.info(f"chosen device: {device.name}")
    logger.info(f"min peak volume: {min_peak_volume}")
    logger.info(f"----------------------------------")

    logger.info(f"Start fishing")
    loop(device, min_peak_volume)
