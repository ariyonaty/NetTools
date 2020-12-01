### Linux IP Forwarding
On the Linux attacker machine, after spoofing, targetted machine will send packets to it. 
By default, the kernel drops the packets instead of forwarding them to router.

To enable packet forwarding, run:
```bash
sysctl -w net.ipv4.ip_forward=1
```
To disable packet forwarding, run:
```bash
sysctl -w net.ipv4.ip_forward=1
```
To check status, run:
```bash
systl net.ipv4.ip_forward
```
