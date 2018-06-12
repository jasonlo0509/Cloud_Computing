sudo qemu-system-x86_64 --enable-kvm -drive format=raw,file=compute2.img,if=virtio \
			-m 4096 -net tap,ifname=tap2,script=no,downscript=no \
			-net nic,model=virtio,vlan=0,macaddr=ae:ae:ae:ae:00:50 -vnc :2
