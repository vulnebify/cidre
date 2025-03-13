import logging

import requests
import ipaddress
import netaddr
import collections

from typing import Dict, List, Set

RIRS = {
    "afrinic": "https://ftp.afrinic.net/pub/stats/afrinic/delegated-afrinic-extended-latest",
    "apnic": "https://ftp.apnic.net/pub/stats/apnic/delegated-apnic-extended-latest",
    "arin": "https://ftp.arin.net/pub/stats/arin/delegated-arin-extended-latest",
    "lacnic": "https://ftp.lacnic.net/pub/stats/lacnic/delegated-lacnic-extended-latest",
    "ripencc": "https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest",
}


class RirFetcher:
    def __init__(self, merge: bool, proxy: str | None):
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__merge = merge
        self.__proxy = proxy

    def fetch(self):
        data = self.__fetch()

        cidrs = self.__convert_to_cidrs(data)

        if not self.__merge:
            return cidrs

        merged = self.__merge_cidrs(cidrs)

        return merged

    def __fetch(self) -> Dict[str, List[str]]:
        sources = RIRS

        data = {}
        for registry, url in sources.items():
            try:
                self.__logger.info(
                    f"Pulling IP ranges from {registry}.", extra={"registry": registry}
                )
                response = requests.get(
                    url,
                    timeout=30,
                    proxies=({"http": self.__proxy} if self.__proxy else None),
                )
                response.raise_for_status()
                data[registry] = response.text.splitlines()
            except requests.RequestException as e:
                self.__logger.exception(
                    f"Error pulling {registry} data.", extra={"registry": registry}
                )

        return data

    def __convert_to_cidrs(
        self, data: Dict[str, List[str]]
    ) -> Dict[str, Dict[str, Set]]:

        self.__logger.info("Compliling pulled IP ranges into CIDRs.")

        country_cidrs = collections.defaultdict(lambda: {"ipv4": set(), "ipv6": set()})

        for _, lines in data.items():
            for line in lines:
                parts = line.split("|")
                if len(parts) < 7:
                    continue

                _registry, cc, ip_version, start_ip, value, _date, status = parts[:7]

                if status != "allocated" and status != "assigned":
                    continue

                try:
                    count = int(value)
                    start_ip_obj = ipaddress.ip_address(start_ip)
                    end_ip_obj = ipaddress.ip_address(int(start_ip_obj) + count - 1)

                    cidr_blocks = netaddr.iprange_to_cidrs(
                        str(start_ip_obj),
                        str(end_ip_obj),
                    )

                    if ip_version == "ipv4":
                        country_cidrs[cc]["ipv4"].update(cidr_blocks)
                    elif ip_version == "ipv6":
                        country_cidrs[cc]["ipv6"].update(cidr_blocks)
                except ValueError:
                    continue

        return country_cidrs

    def __merge_cidrs(
        self, cidrs: Dict[str, Dict[str, Set]]
    ) -> Dict[str, Dict[str, Set]]:
        self.__logger.info("Merging compiled CIDRs.")

        merged_cidrs = {}

        for cc, networks in cidrs.items():
            merged_cidrs[cc] = {
                "ipv4": sorted(netaddr.IPSet(networks["ipv4"]).iter_cidrs()),
                "ipv6": sorted(netaddr.IPSet(networks["ipv6"]).iter_cidrs()),
            }

        return merged_cidrs
