# About
MobaXterm的配置文件中，连接字串用%分割，很多意义不明，不同协议也有区别，所以只测试了写本脚本时涉及的ssh、telnet、ftp三种类型的常用参数。



## 版本

MobaXterm:	v20.0 Build 4286

XShell:	6 (Build 0095)

Python:	3.7

OS:	Windows 10



## 使用

python XShell2MobaXterm.py <XShell_Sessions_dir>



## 问题

使用MobaXterm连接锐捷交换机，软件版本为 S5700H_RGOS 11.4(1)B2P4，出现诡异现象，可以正常连上，执行命令，但只要切换了标签页，该连接就自动断开，提示

> Remote side unexpectedly closed network connection

测试了一下午，终于找到问题，该设备不支持SFTP，将 会话设置->高级SSH设置->SSH浏览器类型 设为 无，可正常工作。