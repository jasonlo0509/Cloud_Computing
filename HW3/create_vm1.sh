sudo qemu-system-x86_64 --enable-kvm -drive format=raw,file=controller.img,if=virtio \
			-m 4096 -net tap,ifname=tap0,script=no,downscript=no \
			-net nic,model=virtio,vlan=0,macaddr=ae:ae:00:00:00:50 -vnc :0 
