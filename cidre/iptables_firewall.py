import logging
import shutil
import subprocess
from pathlib import Path
from typing import List


class IpTablesFirewall:
    def __init__(self, base_folder: str):
        self.__base_folder = base_folder
        self.__logger = logging.getLogger(self.__class__.__name__)

    def apply(self, action: str, country_codes: List[str]) -> bool:
        if not shutil.which("ipset") or not shutil.which("iptables"):
            self.__logger.error(
                "Error: ipset or iptables is not installed on this system."
            )
            self.__logger.error(
                "You can install them with: `sudo apt install ipset iptables`"
            )
            return False

        for country_code in country_codes:
            self.__apply_one(action, country_code.lower())

        return True

    def __apply_one(self, action: str, country_code: str):
        for ip_version in ["ipv4", "ipv6"]:
            cidr_file = Path(self.__base_folder) / ip_version / f"{country_code}.cidr"

            if not cidr_file.exists():
                self.__logger.error(
                    f"CIDR file not found for {country_code.upper()} in {ip_version}."
                )
                self.__logger.error("You can pull it with: `cidre pull --merge`")
                return

            with open(cidr_file, "r") as f:
                cidr_blocks = [line.strip() for line in f.readlines() if line.strip()]

            if not cidr_blocks:
                self.__logger.error(
                    f"No CIDR blocks found for {country_code.upper()} in {ip_version}."
                )
                return

            set_name = f"cidre_{country_code}_blocklist_{ip_version}"

            self.__create_ipset(set_name, ip_version)
            self.__add_to_ipset(set_name, cidr_blocks)
            self.__apply_iptables(set_name, action, ip_version)

    def __create_ipset(self, set_name: str, ip_version: str):
        self.__logger.info(f"🛠 Creating IPSet {set_name} (if not exists)...")

        if ip_version == "ipv4":
            subprocess.run(
                ["ipset", "create", set_name, "hash:net", "-exist"], check=True
            )
        elif ip_version == "ipv6":
            subprocess.run(
                ["ipset", "create", set_name, "hash:net", "family", "inet6", "-exist"],
                check=True,
            )

    def __add_to_ipset(self, set_name: str, cidr_blocks: List[str]):
        self.__logger.info(f"IPSet ({set_name}): Adding {len(cidr_blocks)} CIDRs...")

        for cidr in cidr_blocks:
            subprocess.run(["ipset", "add", set_name, cidr, "-exist"], check=True)

            self.__logger.debug(f"IPSet ({set_name}): Added {cidr}")

    def __apply_iptables(self, set_name: str, action: str, ip_version: str):
        iptables_action = {
            "deny": "DROP",
            "reject": "REJECT",
            "allow": "ACCEPT",
        }.get(action)

        self.__logger.info(
            f"Applying iptables rule: {action.upper()} for {set_name}..."
        )
        subprocess.run(
            [
                "iptables" if ip_version == "ipv4" else "ip6tables",
                "-I",
                "INPUT",
                "-m",
                "set",
                "--match-set",
                set_name,
                "src",
                "-j",
                iptables_action,
            ],
            check=True,
        )
