import os
import logging

from pathlib import Path

from typing import Dict, Set


class FsCidrStore:
    def __init__(self, base_folder: str):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__base_path = Path(base_folder)

    def save(self, cidrs: Dict[str, Dict[str, Set]]):
        self.__logger.info(
            f"Saving CIDRs into {self.__base_path}/* path.",
            extra={"base_path": {self.__base_path}},
        )
        for cc, networks in sorted(cidrs.items()):
            for ip_version in ["ipv4", "ipv6"]:
                directory = self.__base_path / ip_version
                os.makedirs(directory, exist_ok=True)
                filename = f"{directory}/{cc.lower()}.cidr"
                with open(filename, "w") as f:
                    for network in networks[ip_version]:
                        f.write(f"{network}\n")
                        self.__logger.debug(
                            f"Data saved to {filename}", extra={"filename": filename}
                        )
