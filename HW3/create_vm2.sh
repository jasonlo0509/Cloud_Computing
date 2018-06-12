sudo qemu-system-x86_64 --enable-kvm -drive format=raw,file=compute1.img,if=virtio \
			-m 4200 -net tap,ifname=tap1,script=no,downscript=no \
			-net nic,model=virtio,vlan=0,macaddr=ae:ae:ae:00:00:50 -vnc :1 
