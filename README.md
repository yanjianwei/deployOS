DeployOS
===================================================================

DeployOS v1.0一款支持在线部署openstack kilo版本的自动化部署工具脚本。该工具
支撑过现网几十台规模的openstack部署。采用的主要技术：Fabric+shell

## 主要版本历史

* 1.0: 2015-12-14
    * 新建deployOS项目;
    * 添加deployOS基本内容;

---
##使用说明
* 确保所有部署的服务器开启ssh服务，并能用root远程登录
* 部署openstack前，需做好如下配置规划:


> >a) 控制节点，网络节点，计算节点的ip,主机名，网卡。建议contorller为1个网卡，network为1个网卡，network为>两个网卡，计算节点为1个网卡
> 
> >b) 为降低运维复杂度，本部署工具把控制口和数据口设置为同一网卡

* 配置
> >a) 配置config.ini.必须配置的选项为:
> 
> >>CONTROLLER_NODE,NETWORK_NODE,COMPUTE_NODE,COMPUTE(local_dir为deployOS解压目录)
> 多个计算节点，依次类推，其它使用默认即可
> 
> >b)配置fabric_env.py:
> 
>>>主要配置env.hosts,env.passwords,env.roledefs

* 部署并运行
>>在部署服务器上(和openstack区分开)，执行：
>>>a)apt-get install fabric
>
>>>b)./go.sh

*注意
> a)部署的时间长短取决于网络状况，因为部署openstack需要从外网下载很多依赖包
>
> b)部署过程中有的步骤需要输入密码，需和config.ini里保持一致，建议统一为stack

  
---
## 参加步骤
* 在 GitHub 上 `fork` 到自己的仓库，如 `yanjianwei/deployOS.git`，然后 `clone` 到本地，并设置用户信息。

> $ git clone git@github.com:yanjianwei/deployOS.git
> 
> $ cd deployOS

> $ git config user.name "yourname"
> 
> $ git config user.email "your email"

* 修改代码后提交，并推送到自己的仓库。

> $ #do some change on the content
> 
> $ git commit -am "Fix issue #1: change helo to hello"
> 
> $ git push

* 在 GitHub 网站上提交 pull request。
* 定期使用项目仓库内容更新自己仓库内容。

> $ git remote add upstream https://github.com/yanjianwei/deployOS.git
> 
> $ git fetch upstream
> 
> $ git checkout master
> 
> $ git rebase upstream/master
> 
> $ git push -f origin master

* 欢迎各位网友提供更好的建议或者BUG，请联系QQ:446369399 e-mail:yanjianwei@fnic.cn




