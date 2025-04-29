from .cidrs.rir_fetcher import RirFetcher
from .cidrs.cidr_counter import CidrCounter

# Backward compatibility
from .cidrs import rir_fetcher, cidr_store, cidr_counter
from .firewalls import ufw_firewall, iptables_firewall
