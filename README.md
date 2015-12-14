# deployOS
一个自动化部署openstack的工具,支撑过现网20台服务器规模的openstack部署

##使用说明
1.确保所有部署的服务器开启ssh服务，并能用root远程登录

2.部署openstack前，需做好如下配置规划：
  a)控制节点，网络节点，计算节点的ip,主机名，网卡。建议contorller为1个网卡，network为>两个网卡，计算节点为1个网卡
  b)为降低运维复杂度，本部署工具把控制口和数据口设置为同一网卡
3.配置
  a)配置config.ini
    必须配置的选项为：CONTROLLER_NODE,NETWORK_NODE,COMPUTE_NODE,PAHT(local_dir为deployOS解压目录)
    多个计算节点，依次类推，其它使用默认即可
  b)配置fabric_env.py
    主要配置env.hosts,env.passwords,env.roledefs

4.部署
  在部署服务器上(和openstack区分开)，执行：
  a)apt-get install fabric
  b)./go.sh
  
5.FAQ
  1.部署的时间长短取决于网络状况，因为部署openstack需要从外网下载很多依赖包

  2.部署过程中有的步骤需要输入密码，需和config.ini里保持一致，建议统一为stack

  3.各位使用过程中，发现任何BUG或者建议，联系
    QQ:446369399
    e-mail: yanjianwei@fnic.cn
