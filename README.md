# CIDRE

**CIDRe** is a CLI tool that fetches **daily updated IP allocations** from **Regional Internet Registries (RIRs)**, compiles them into country-based CIDR files, and allows easy **firewall management**.

[![Compile CIDRs](https://github.com/vulnebify/cidre/actions/workflows/compile_cidrs.yml/badge.svg)](https://github.com/vulnebify/cidre/actions/workflows/compile_cidrs.yml)
[![Publish Release to PyPI](https://github.com/vulnebify/cidre/actions/workflows/pypi_release.yml/badge.svg)](https://github.com/vulnebify/cidre/actions/workflows/pypi_release.yml)

![demo](https://github.com/user-attachments/assets/ada4e504-90a3-442b-aa05-98a1e0b1da7e)

🔹 **Supports AFRINIC, APNIC, ARIN, LACNIC, RIPE NCC**    
🔹 Daily automatic CIDR updates **[in the repository](https://github.com/vulnebify/cidre/blob/main/output/cidr)**    
🔹 **Merges and optimizes CIDR blocks** for efficiency     
🔹 **Firewall integration** (UFW & iptables /w ipset support)   
🔹 **IPv4 & IPv6 compatible**     

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

### Install from PyPI

```bash
pip install cidre-cli
```

### Intall from GitHub

```bash
git clone https://github.com/vulnebify/cidre.git && cd cidre && python3 -m venv .venv && source .venv/bin/activate && pip install .
```

---

## Commands

### `cidr pull`

| Command           | Description                                         |
| ----------------- | --------------------------------------------------- |
| `cidre cidr pull` | Fetches the latest IP allocation data from all RIRs |

| Flag           | Description                                 | Default                           |
| -------------- | ------------------------------------------- | --------------------------------- |
| `--merge`      | Merges overlapping IP ranges for efficiency | `false`                           |
| `--proxy`      | Proxies connection to RIRs                  | *optinal*                         |
| `--cidr-store` | Specifies CIDRs' custom storage directory   | e.g. `./output/cidr/ipv4/us.cidr` |

### `cidr count`

| Command                  | Description                                                    |
| ------------------------ | -------------------------------------------------------------- |
| `cidre cidr count`       | Counts amount of IPs per country                               |
| `cidre cidr count US CN` | Counts amount of IPs by country code (ISO 3166-1 alpha-2 code) |

| Flag           | Description                               | Default                           |
| -------------- | ----------------------------------------- | --------------------------------- |
| `--cidr-store` | Specifies CIDRs' custom storage directory | e.g. `./output/cidr/ipv4/us.cidr` |

### `firewall allow|deny|reject`

| Command                 | Description                             |
| ----------------------- | --------------------------------------- |
| `cidre firewall allow`  | Apply allow rule to specified firewall  |
| `cidre firewall deny`   | Apply deny rule to specified firewall   |
| `cidre firewall reject` | Apply reject rule to specified firewall |

| Flag           | Description                                         | Default                           |
| -------------- | --------------------------------------------------- | --------------------------------- |
| `--firewall`   | Firewall to apply rules. Options: `ufw`, `iptables` | `ufw`                             |
| `--cidr-store` | Specifies CIDRs' custom storage directory           | e.g. `./output/cidr/ipv4/us.cidr` |

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

