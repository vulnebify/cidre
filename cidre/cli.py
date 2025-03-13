#!/usr/bin/env python3

import argparse
import logging

from . import rir_fetcher, cidr_store, firewall, countries

from typing import List


def country_code(value: str):
    value = value.upper()
    if value not in countries.ISO_3166_1_ALPHA_2_CODES:
        raise argparse.ArgumentTypeError(
            f"Invalid country code: {value}. Choose from {', '.join(countries.ISO_3166_1_ALPHA_2_CODES)}"
        )
    return value


def pull(merge: bool, proxy: str | None, store: str):
    cidrs = rir_fetcher.RirFetcher(merge, proxy).fetch()

    cidr_store.FsCidrStore(store).save(cidrs)


def apply(action: str, countries: List[str], store: str):
    ufw = firewall.UfwFirewall(store)

    ufw.apply(action, countries)


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
        "-s",
        "--store",
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
            choices=["ufw"],
            default="ufw",
            help="The firewall for adding rules.",
        )

        action_parser.add_argument(
            "-s",
            "--store",
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
        pull(args.merge, args.proxy, args.store)
        print("")
        print("Pulling complete ✅")
    elif args.command in ["allow", "deny", "reject"]:
        print(
            f"💡 Applying '{args.command}' action to '{args.firewall}' firewall for {", ".join(args.countries)} countries...",
            end="\n\n",
        )
        apply(args.command, args.countries, args.store)
        print("")
        print("Applying complete ✅")

    print("")


if __name__ == "__main__":
    main()
