### NetCut

Prerequistites :
- Run ARP Spoofer
    - `sudo -s PATH=$PATH python ARP_Spoofer/arp_spoofer.py`
    - `sudo sysctl -w net.ipv4.ip_forward=1`
- Run Packet Sniffer (optional)
    - `sudo -s PATH=$PATH python Packet_Sniffer/packet_sniffer.py`
- Run Net Cut
    - `sudo -s PATH=$PATH python Net_Cut/net_cut.py`

IPtables : 
- iptables -I FORWARD -j NFQUEUE --queue-num 0
- iptables flush 
- To test locally:
    - iptables -I OUTPUT -j NFQUEUE --queue-num 0
    - iptables -I INPUT -j NFQUEUE --queue-num 0

