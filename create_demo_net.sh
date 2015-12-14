source demo-openrc.sh
nova keypair-add demo-key
nova keypair-list
neutron net-create demo-net
neutron subnet-create demo-net 192.168.1.0/24 \
  --name demo-subnet --gateway 192.168.1.1
neutron router-create demo-router
neutron router-interface-add demo-router demo-subnet
neutron router-gateway-set demo-router ext-net
neutron net-list

# nova --debug boot --flavor m1.tiny --image cirros-0.3.4-x86_64 --nic net-id=b2173633-4349-4777-ae59-07c18097b2ca \
#  --security-group default --key-name demo-key demo-4
