import logging
import ipaddress

from pathlib import Path
from typing import List, Dict
from collections import defaultdict


class CidrCounter:
    def __init__(self, base_folder: str):
        self.__base_folder = base_folder
        self.__logger = logging.getLogger(self.__class__.__name__)

    def count(self, country_codes: List[str]) -> Dict[str, Dict[str, int]]:
        total = defaultdict(int)

        for country_code in country_codes:
            for ip_version in ["ipv4", "ipv6"]:
                cidr_file = (
                    Path(self.__base_folder)
                    / ip_version
                    / f"{country_code.lower()}.cidr"
                )

                if not Path.exists(cidr_file):
                    continue

                with open(cidr_file, "r") as f:
                    cidr_blocks = [
                        line.strip() for line in f.readlines() if line.strip()
                    ]

                for cidr in cidr_blocks:
                    count = ipaddress.ip_network(cidr).num_addresses
                    total[country_code] += count

        if not total:
            joined_countries = ",".join(country_codes)
            self.__logger.error(f"Error: CIDR files not found for {joined_countries}.")
            self.__logger.error("You can pull it with: `cidre pull --merge`")
            return {}

        return dict(sorted(total.items(), key=lambda item: -item[1]))
