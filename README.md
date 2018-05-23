### 一、系统定义

Zabbix Auto Api：开发并封装Zabbix Api，提升zabbix监控的自动化能力，提升运维人员的效率，可以将更多的时间用于自动化工具开发上来。

### 二、主要功能

封装zabbix api为私有云和CMDB提供监控创建、删除、分组、维护、责任人、自动屏幕等功能的RESTFUL接口。

### 三、代码结构

```
└── zauto
	├── common 通用模块
    	├── check_data.py 传参验证
        ├── config.py│ 配置（url、账户等配置）
        └── init.py
    ├── zauto.py 路由及启动
    └── zbxmod zabbix功能模块
    	├── init.py
        ├── zbx_add_host.py
        ├── zbx_add_maintenance.py
        ├── zbx_delete_host.py
        ├── zbx_delete_maintenance.py
        └── zbx_login.py
```



