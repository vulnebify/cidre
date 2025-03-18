**CIDRe** is a CLI tool that fetches **daily updated IP allocations** from **Regional Internet Registries (RIRs)**, compiles them into country-based CIDR files, and allows easy **firewall management**.

🔹 **Supports AFRINIC, APNIC, ARIN, LACNIC, RIPE NCC**  
🔹 **Merges and optimizes CIDR blocks** for efficiency  
🔹 **Firewall integration** (UFW support)  
🔹 **IPv4 & IPv6 compatible**  

---

## ⚡ Quick start

### **1️⃣ Install CIDRE**

```bash
pip install cidre-cli
```

### **2️⃣ Pull & merge CIDR ranges**

```bash
cidre pull --merge
```

- Downloads the latest CIDR allocations from RIRs.
- Merges overlapping IP ranges for efficiency.

### **3️⃣ Block specific countries**

```bash
# UFW is better suited for small CIDR inputs
cidre deny ir kp --firewall ufw
```

- Blocks **Iran (IR), and North Korea (KP)** in UFW.
- Requires **ufw** installed (`sudo apt install ufw`).


```bash
# iptables is better suited for large CIDR inputs
cidre deny ru ir kp --firewall iptables
```

- Blocks **Russia (RU), Iran (IR), and North Korea (KP)** in iptables using ipset.
- Requires **ipset and iptables** installed (`sudo apt install ipset iptables`).

---

## 🚀 Features

- **Daily automatic CIDR updates**.
- **Compiles CIDR blocks per country** from RIR allocation data.
- **Merges overlapping IP ranges** for efficiency.
- **Allows easy firewall rules** for blocking or allowing entire countries.
- **Supports both IPv4 & IPv6**.

---

## 🛠️ Installation

### **1️⃣ Install via PyPI**

```bash
pip install cidre-cli
```

### **2️⃣ Alternative: clone the repository**

```bash
git clone https://github.com/vulnebify/cidre.git
cd cidre
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

---

## ⚡ Usage

### **1️⃣ Pull and compile CIDR ranges**

Fetches the latest IP allocation data from all RIRs and **compiles per-country CIDR blocks**:

```bash
cidre pull --merge
```

- `--merge`: Merges overlapping IP ranges for efficiency.
- `--proxy <proxy>`: Proxies connection to RIRs.
- `--cidr-store <path>`: Specifies CIDRs' custom storage directory. Default `./output/cidr/{ipv4|ipv6}/{country_code}.cidr`.

### **2️⃣ Action on countries**

Allow|deny|reject specific countries' CIDR blocks in **specified firewall**:

```bash
cidre allow|deny|reject ru ir kp
```

- `--firewall ufw|iptables`: Firewall to apply rules. Default `ufw`.
- `--cidr-store <path>`: Specifies CIDRs' custom storage directory. Default `./output/cidr/{ipv4|ipv6}/{country_code}.cidr`.

**⚠️ NOTE: iptables firewall DO NOT persist rules by default**

To ensure iptables and IPSet rules persist after a reboot, follow these steps:

```bash
# 1️⃣ Save rules based on the firewall method:
# - For iptables + IPSet:
sudo ipset save > /etc/ipset.rules
sudo iptables-save > /etc/iptables/rules.v4
sudo ip6tables-save > /etc/iptables/rules.v6

# 2️⃣ Restore firewall rules on boot:
# - For iptables + IPSet:
sudo bash -c 'echo "ipset restore < /etc/ipset.rules" >> /etc/rc.local'
sudo chmod +x /etc/rc.local

# 3️⃣ Reboot and verify:
sudo reboot
sudo ipset list
sudo iptables -L -v -n
```


---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙌 Inspired by

CIDRE was inspired by **[herrbischoff/country-ip-blocks](https://github.com/herrbischoff/country-ip-blocks)** and aims to provide an automated alternative with firewall integration.

---

## 🤝 Contributions

PRs are welcome! Feel free to **fork the repo** and submit pull requests.

---

## 📧 Contact

For any questions, open an issue or reach out via GitHub Discussions.

