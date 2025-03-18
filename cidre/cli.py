#!/usr/bin/env python3

import argparse
import logging

from . import rir_fetcher, cidr_store, countries, ufw_firewall, iptables_firewall

from typing import List
from enum import Enum


class Firewall(str, Enum):
    UFW = "ufw"
    IPTABLES = "iptables"


def country_code(value: str):
    value = value.upper()
    if value not in countries.ISO_3166_1_ALPHA_2_CODES:
        raise argparse.ArgumentTypeError(
            f"Invalid country code: {value}. Choose from {', '.join(countries.ISO_3166_1_ALPHA_2_CODES)}"
        )
    return value


def pull(merge: bool, proxy: str | None, store: str) -> bool:

    try:
        cidrs = rir_fetcher.RirFetcher(merge, proxy).fetch()

        cidr_store.FsCidrStore(store).save(cidrs)

        return True
    except:
        logger = logging.getLogger(__name__)
        logger.exception(
            "Yikes! Unhandled exception. Shame on us! File ticket: https://github.com/vulnebify/cidre/issues/new"
        )

        return False


def apply(firewall: Firewall, action: str, countries: List[str], store: str) -> bool:
    try:
        if firewall == Firewall.UFW:
            ufw = ufw_firewall.UfwFirewall(store)

            return ufw.apply(action, countries)

        if firewall == Firewall.IPTABLES:
            iptables = iptables_firewall.IpTablesFirewall(store)

            return iptables.apply(action, countries)
    except:
        logger = logging.getLogger(__name__)
        logger.exception(
            "Yikes! Unhandled exception. Shame on us! File ticket: https://github.com/vulnebify/cidre/issues/new"
        )

        return False


def main():
    print(
        r"""
  ____  ___  ____   ____   _____ 
 / ___||_ _||  _ \ |  _ \ | ____|
| |     | | | | | || |_) ||  _|  
| |___  | | | |_| ||  _ < | |___ 
 \____||___||____/ |_| \_\|_____|
        """
    )
    print(
        "Compile CIDRs from AFRINIC, APNIC, ARIN, LACNIC and RIPENCC. See more: https://github.com/vulnebify/cidre"
    )
    print("")

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command", required=True)

    pull_parser = subparsers.add_parser("pull", help="Pulls the CIDRs from RIRs")

    pull_parser.add_argument(
        "-m",
        "--merge",
        action="store_true",
        help="Merge CIDR blocks for efficiency",
    )
    pull_parser.add_argument(
        "-p",
        "--proxy",
        type=str,
        help="The proxy to make requests RIRs",
    )
    pull_parser.add_argument(
        "-cs",
        "--cidr-store",
        dest="cidr_store",
        type=str,
        default="../output/cidr",
        help="The path to store CIDRs. Default: '../output/cidr'.",
    )

    for action in ["allow", "deny", "reject"]:
        action_parser = subparsers.add_parser(
            action,
            help=f"Applies '{action}' action to country's CIDRs in firewall.",
        )

        action_parser.add_argument(
            "countries",
            nargs="+",
            type=country_code,
            help="The countries (ISO 3166-1 alpha-2 code).",
        )

        action_parser.add_argument(
            "-f",
            "--firewall",
            type=Firewall,
            choices=[Firewall.UFW, Firewall.IPTABLES],
            default=Firewall.UFW,
            help="The firewall for adding rules. Default: 'ufw'.",
        )

        action_parser.add_argument(
            "-cs",
            "--cidr-store",
            dest="cidr_store",
            type=str,
            default="../output/cidr",
            help="The path to store CIDRs. Default: '../output/cidr'.",
        )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    if args.command == "pull":
        print(
            f"💡 Pulling ranges from RIRs to compile CIDRs with {"enabled" if args.merge else "disabled"} merging...",
            end="\n\n",
        )
        success = pull(args.merge, args.proxy, args.cidr_store)
        print("")

        if success:
            print("Pulling complete ✅")
        else:
            print("Oh no! Pulling failed ❌")
    elif args.command in ["allow", "deny", "reject"]:
        print(
            f"💡 Applying '{args.command}' action to '{args.firewall.value}' firewall for {", ".join(args.countries)} countries...",
            end="\n\n",
        )
        success = apply(args.firewall, args.command, args.countries, args.cidr_store)
        print("")

        if success:
            print("Applying complete ✅")
        else:
            print("Oh no! Applying failed ❌")

    print("")


if __name__ == "__main__":
    main()
