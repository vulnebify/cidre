import logging
import subprocess
import shutil

from pathlib import Path
from typing import List


class UfwFirewall:
    def __init__(self, base_folder: str):
        self.__base_folder = base_folder
        self.__logger = logging.getLogger(self.__class__.__name__)

    def apply(self, action: str, country_codes: List[str]):
        if not shutil.which("ufw"):
            self.__logger.error("Error: UFW is not installed on this system.")
            self.__logger.error("You can install it with: `sudo apt install ufw`")
            return

        for country_code in country_codes:
            self.__apply_one(action, country_code)

    def __apply_one(self, action: str, country_code: str):

        for ip_version in ["ipv4", "ipv6"]:
            cidr_file = (
                Path(self.__base_folder) / ip_version / f"{country_code.lower()}.cidr"
            )

            if not Path.exists(cidr_file):
                self.__logger.error(
                    f"Error: CIDR file not found for {country_code.upper()} in {ip_version}."
                )
                self.__logger.error("You can pull it with: `cidre pull --merge`")
                return

            with open(cidr_file, "r") as f:
                cidr_blocks = [line.strip() for line in f.readlines() if line.strip()]

            if not cidr_blocks:
                self.__logger.error(
                    f"Error: No CIDR blocks found for {country_code.upper()} in {ip_version}."
                )
                return

            for cidr in cidr_blocks:
                rule = f"ufw {action} from {cidr}"
                self.__logger.info(f"Executing: {rule}")
                subprocess.run(rule, shell=True, check=True)
