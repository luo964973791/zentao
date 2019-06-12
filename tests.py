#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''这是安装docker的脚本，基于centos7.0,python2/3'''
import os,sys
docker_path = '/etc/docker/'
daemon_json = "cat >>/etc/docker/daemon.json<<EOF"
aliyuncs = '''
{
  "registry-mirrors": ["https://t5e5alvb.mirror.aliyuncs.com"]
}
EOF
'''
def install_docker():
    # 判断用户是否为root
    if os.getuid() != 0:
        print(u"\033[1;35m当前用户不是root用户，请以root用户执行脚本。\033[1;m")
        sys.exit(0)
    else:
        print(u"\033[1;32m开始安装docker所需依赖包。\033[1;m")
    gcc = os.system('yum install -y yum-utils device-mapper-persistent-data lvm2 && yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo && yum -y install docker-ce && yum makecache fast')
    if gcc != 0:
        print(u"\033[1;35m安装依赖包失败。\033[1;m")
        sys.exit(1)
    else:
        print(u"\033[1;32m准备创建docker主目录,并清除yum缓存。\033[1;m")
    docker = os.system('mkdir -p ' + docker_path)
    if docker != 0:
        print(u"\033[1;35m创建目录失败。\033[1;m")
        sys.exit(2)
    else:
        os.system('echo 1 > /proc/sys/net/ipv4/ip_forward && yum clean all && rm -rf /var/cache/yum/*')
        print(u"\033[1;32m装备添加阿里云加速器\033[1;m")
    insert_aliyun = os.system(daemon_json + aliyuncs)
    if insert_aliyun != 0:
        print(u"\033[1;35m添加阿里云docker加速器失败\033[1;m")
        sys.exit(3)
    else:
        print(u"\033[1;32m添加阿里云docker加速器成功，准备启动docker\033[1;m")
    start_docker = os.system('systemctl daemon-reload && systemctl restart docker && systemctl enable docker')
    if start_docker != 0:
        print(u"\033[1;35m启动docker失败。\033[1;m")
        sys.exit(4)
    else:
        print(u"\033[1;32m启动docker成功，并开始下载centos mysql tomcat php redis nginx httpd镜像\033[1;m")
    images = os.system('docker pull centos && docker pull mysql && docker pull tomcat && docker pull php && docker pull redis && docker pull nginx && docker pull httpd')
    if images != 0:
        print(u"\033[1;35m下载centos mysql tomcat php redis nginx httpd失败，请更换国内镜像，或者检查网络\033[1;m")
        sys.exit(5)
    else:
        print(u"\033[1;32m下载centos mysql tomcat php redis nginx httpd镜像成功，开始你的表演。\033[1;m")
if __name__ == "__main__":
    install_docker()
