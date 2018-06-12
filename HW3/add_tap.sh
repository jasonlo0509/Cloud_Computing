#!/usr/bin/env bash

sudo openvpn --mktun --dev tap0 --user `id -un`
sudo ifconfig tap0 promisc up
sudo brctl addif br0 tap0
sudo openvpn --mktun --dev tap1 --user `id -un`
sudo ifconfig tap1 promisc up
sudo brctl addif br0 tap1

sudo openvpn --mktun --dev tap2 --user `id -un`
sudo ifconfig tap2 promisc up
sudo brctl addif br0 tap2
