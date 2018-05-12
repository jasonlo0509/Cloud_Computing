sudo qemu-system-x86_64 --enable-kvm -drive format=raw,file=ubuntu.img,if=virtio \
                        -m 2048 -net tap,ifname=tap1,script=no,downscript=no \
                        -net nic,model=virtio,vlan=0,macaddr=ae:ae:00:00:00:50 -vnc :1 \
                        -incoming tcp:0:4400
