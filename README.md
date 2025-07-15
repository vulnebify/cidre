# CIDRE

**CIDRe** is a CLI tool that fetches **daily updated IP allocations** from **Regional Internet Registries (RIRs)**, compiles them into country-based CIDR files, and allows easy **firewall management**. Daily automatic CIDR updates **[in the repository](https://github.com/vulnebify/cidre/blob/main/output/cidr).**

[![Compile CIDRs](https://github.com/vulnebify/cidre/actions/workflows/compile_cidrs.yml/badge.svg)](https://github.com/vulnebify/cidre/actions/workflows/compile_cidrs.yml)
[![Publish Release to PyPI](https://github.com/vulnebify/cidre/actions/workflows/pypi_release.yml/badge.svg)](https://github.com/vulnebify/cidre/actions/workflows/pypi_release.yml)

[![asciicast](https://asciinema.org/a/727926.svg)](https://asciinema.org/a/727926)

---

## Quick start

### **Install CIDRE**

```bash
pip install cidre-cli
```

### **Pull & merge CIDR ranges**

```bash
cidre cidr pull --merge
```

- Downloads the latest CIDR allocations from RIRs.
- Merges overlapping IP ranges for efficiency.

### **Block specific countries**

```bash
# UFW is better suited for small CIDR inputs
cidre firewall deny ir kp --firewall ufw
```

- Blocks **Iran (IR), and North Korea (KP)** in UFW.
- Requires **ufw** installed (`sudo apt install ufw`).


```bash
# iptables is better suited for large CIDR inputs
cidre firewall deny ru ir kp --firewall iptables
```

- Blocks **Russia (RU), Iran (IR), and North Korea (KP)** in iptables using ipset.
- Requires **ipset and iptables** installed (`sudo apt install ipset iptables`).

---

## Installation

### From PyPI

```bash
pip install cidre-cli
```

### From GitHub

```bash
git clone https://github.com/vulnebify/cidre.git && cd cidre && python3 -m venv .venv && source .venv/bin/activate && pip install .
```

---

## Commands

### `cidr pull`

| Command                             | Description                                                         |
| ----------------------------------- | ------------------------------------------------------------------- |
| `cidre cidr pull`                   | Fetches the latest IP allocation data from all RIRs                 |
| `cidre cidr pull --merge`           | Merges overlapping IP ranges for efficiency. Optional.              |
| `cidre cidr pull --proxy PROXY`     | Proxies connection to RIRs. Optional.                               |
| `cidre cidr pull --cidr-store PATH` | Specifies CIDRs' custom storage directory. Default: `./output/cidr` |

### `cidr count`

| Command                  | Description                                                    |
| ------------------------ | -------------------------------------------------------------- |
| `cidre cidr count`       | Counts amount of IPs per country                               |
| `cidre cidr count US CN` | Counts amount of IPs by country code (ISO 3166-1 alpha-2 code) |
| `cidre cidr count --cidr-store PATH`       | Specifies CIDRs' custom storage directory. Default: `./output/cidr`    |

### `firewall allow|deny|reject`

| Command                                   | Description                                                         |
| ----------------------------------------- | ------------------------------------------------------------------- |
| `cidre firewall allow`                    | Apply allow rule to specified firewall                              |
| `cidre firewall deny`                     | Apply deny rule to specified firewall                               |
| `cidre firewall reject`                   | Apply reject rule to specified firewall                             |
| `cidre firewall reject --firewall ufw`    | Firewall to apply rules. Options: `ufw`, `iptables`. Default: `ufw` |
| `cidre firewall reject --cidr-store PATH` | Specifies CIDRs' custom storage directory. Default: `./output/cidr`          |

**⚠️ NOTE: iptables firewall DO NOT persist rules by default**

To ensure iptables and IPSet rules persist after a reboot, follow these steps:

```bash
# Save rules based on the firewall method:
# - For iptables + IPSet:
sudo ipset save > /etc/ipset.rules
sudo iptables-save > /etc/iptables/rules.v4
sudo ip6tables-save > /etc/iptables/rules.v6

# Restore firewall rules on boot:
# - For iptables + IPSet:
sudo bash -c 'echo "ipset restore < /etc/ipset.rules" >> /etc/rc.local'
sudo chmod +x /etc/rc.local

# Reboot and verify:
sudo reboot
sudo ipset list
sudo iptables -L -v -n
```

---

## License

This project is licensed under the **MIT License**.

---

## Inspired by

CIDRE was inspired by **[herrbischoff/country-ip-blocks](https://github.com/herrbischoff/country-ip-blocks)** and aims to provide an automated alternative with firewall integration.

---

## Contributions

PRs are welcome! Feel free to **fork the repo** and submit pull requests.

---

## Contact

For any questions, open an issue or reach out via GitHub Discussions.

