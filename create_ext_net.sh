source admin-openrc.sh
neutron net-create ext-net --shared --router:external  \
--provider:physical_network external --provider:network_type flat

#neutron subnet-create ext-net 172.171.0.0/20 --name ext-subnet \
#  --allocation-pool start=172.171.4.161,end=172.171.4.179 \
#  --disable-dhcp  --dns-nameserver 114.114.114.114 --gateway 172.171.0.1
