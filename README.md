
# i茅台预约工具----GitHub Actions版

<p align="center">
  <a href="https://hits.seeyoufarm.com">
     <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2F397179459%2FiMaoTai-reserve&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false"/>
  </a>
  <a href="https://github.com/397179459/iMaoTai-reserve">
    <img src="https://img.shields.io/github/stars/397179459/iMaoTai-reserve" alt="GitHub Stars">
  </a>
  <a href="https://github.com/397179459/iMaoTai-reserve">
    <img src="https://img.shields.io/github/forks/397179459/iMaoTai-reserve" alt="GitHub Forks">
  </a>
  <a href="https://github.com/397179459/iMaoTai-reserve/issues">
    <img src="https://img.shields.io/github/issues-closed-raw/397179459/iMaoTai-reserve" alt="GitHub Closed Issues">
  </a>
  <a href="https://github.com/397179459/iMaoTai-reserve">
    <img alt="GitHub commit activity (branch)" src="https://img.shields.io/github/commit-activity/y/397179459/iMaoTai-reserve">
  </a>
  <a href="https://github.com/397179459/iMaoTai-reserve">
    <img src="https://img.shields.io/github/last-commit/397179459/iMaoTai-reserve" alt="GitHub Last Commit">
  </a>
</p>


### 功能：
- [x] 集成Github Actions
- [x] 多账号配置
- [x] 账号有效期管控
- [x] 手机号加密保存
- [x] 自动获取app版本
- [x] 微信消息推送

### 原理：
```shell
1、登录获取验证码
2、输入验证码获取TOKEN
3、获取当日SESSION ID
4、根据配置文件预约CONFIG文件中，所在城市的i茅台商品
```

# 使用方法
## Overview
1. 需要先在本地运行登录脚本，配置好登录信息和抢购信息。
2. 配置 Github Actions 环境变量如下（环境名称以及解释）
   - `PUSHPLUS_KEY`：推送信息的 key
   - `PRIVATE_AES_KEY`：自定义私钥（吧）
   - `CREDENTIALS_BASE64`: credential.base64这个文件的内容，即原项目中`./myConfig/credentials`文件内容经过 base64 编码后得到的字符串。

## 具体使用步骤：
### 本地 run 的部分
如果不需要添加手机号，则login.py只需要跑一次，因为每添加一个手机号，都会写入一次本地文件。
1. 安装依赖
```shell
pip3 install --no-cache-dir -r requirements.txt
```
2. 修改config.py，按照你的需求修改相关配置，这里很重要，建议每个配置项都详细阅读。（注意不要泄露自己的 TOKEN 哈！）
3. 再去配置环境变量 `GAODE_KEY`,再运行`login.py`。高德 API Token用于根据预约位置寻找最近的茅台专卖店。
4. 按提示输入 预约位置、手机号、验证码 等，生成的token等。很长时间不再需要登录。支持多账号，支持加密。
```shell
python3 login.py
# 都填写完之后可以去./myConfig/credentials中查看明文的配置信息
```

### 需要 Github 上配置的部分
**请确保本地运行部分已执行，`./myConfig/credentials.base64`已经生成**

1. 配置github secrets，共 3 项
   - `PUSHPLUS_KEY`：推送信息的 key，去 [PushPlus官网](https://www.pushplus.plus/) 申请一个，分分钟搞定
   - `PRIVATE_AES_KEY`：自定义私钥（吧），随便写个喜欢的字符串
   - `CREDENTIALS_BASE64`: `./myConfig/credentials.base64`这个文件的内容


## 特别感谢
技术思路：https://blog.csdn.net/weixin_47481826/article/details/128893239

初版代码：https://github.com/tianyagogogo/imaotai




