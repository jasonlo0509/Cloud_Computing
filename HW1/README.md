# HW1 
## Live Migration and Tap interface
## Steps for setup linux interface

1. Get main adapter name by ifconfig(i.e. eth0)
2. Add new bridge(br0) and add main adapter(eth0) as its interface
```bash
$ sudo brctl addbr br0 // Add a new network interface
$ sudo brctl show
    bridge name     bridge id               STP enabled     interfaces
    br0             8000.000000000000       no
$ sudo brctl addif br0 (Your hardware network adapter name)
```
3. Change /etc/network/interfaces
```bash 
# newly added 
auto eth0
iface eth0 inet manual
    dns-nameservers 8.8.8.8 8.8.4.4

auto br0
iface br0 inet static
    address (your ip)
    netmask (your netmask))
    gateway (your gateway)
    bridge_ports eth0
    bridge_fd 9
    bridge_hello 2
    bridge_maxage 12
    bridge_stp off

    auto br0:0
    iface br0:0 inet static
    address 10.1.1.254
    netmask 255.255.255.0
```
5. reboot! and type route to check your interface has been change to br0 (eth0->br0->internet)
6. ping 8.8.8.8 and www.google.com to ensure the network is available! Then follow the steps in assignment1.pdf(page9)

## Reference
1. [What is IPTABLE?](http://linux.vbird.org/linux_server/0250simple_firewall.php#netfilter)
2. [What is Live Migration?](http://blog.51cto.com/findman/260748)
3. [What is Virtio?](https://www.qnap.com/zh-tw/how-to/tutorial/article/%E5%A6%82%E4%BD%95%E5%9C%A8-virtualization-station-%E4%B8%AD%E8%A8%AD%E5%AE%9A%E5%8F%8A%E4%BD%BF%E7%94%A8-virtio-%E7%A1%AC%E7%A2%9F%E6%8E%A7%E5%88%B6%E4%BB%8B%E9%9D%A2)
4. [How to setup linux bridge interface](http://pominglee.blogspot.tw/2014/03/linux.html)
5. [KVM](http://www.lijyyh.com/2015/12/linux-kvm-set-up-linux-kvm.html)
6. [How to use sysbench](https://ssorc.tw/4882)
7. [How to use iperf](https://cms.35g.tw/coding/%E5%88%A9%E7%94%A8-iperf-%E6%B8%AC%E8%A9%A6%E7%B6%B2%E8%B7%AF%E6%95%88%E8%83%BD/)
8. [Add dns server](https://askubuntu.com/questions/465729/ping-unknown-host-google-com-in-ubuntu-server)
