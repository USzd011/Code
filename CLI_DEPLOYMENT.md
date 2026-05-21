# 🦞 大厂 CLI 工具部署报告

## 📅 部署时间
2026-05-09 02:40 (Asia/Shanghai)

## ✅ 已安装的 CLI 工具

### 1. 腾讯云 CLI (tccli)
- **版本**: 3.1.88.1
- **状态**: ✅ 已安装并配置
- **API 配置**:
  - SecretId: `[REDACTED]`
  - SecretKey: `[REDACTED]`
  - Region: `ap-guangzhou`
- **测试结果**: ✅ API 调用成功

### 2. AWS CLI
- **版本**: 1.45.6
- **状态**: ✅ 已安装
- **Python**: 3.12.3
- **配置**: ⏳ 需要配置 AWS 凭证

### 3. 阿里云 CLI (aliyuncli)
- **版本**: 2.1.5
- **状态**: ✅ 已安装
- **配置**: ⏳ 需要配置阿里云凭证

---

## ⏳ 需要手动安装的 CLI

### 4. Google Cloud SDK
- **安装地址**: https://cloud.google.com/sdk/docs/install
- **状态**: ⏳ 需要手动安装

### 5. 华为云 CLI
- **安装地址**: https://support.huaweicloud.com/cli/index.html
- **状态**: ⏳ 需要手动安装

### 6. 百度云 CLI
- **状态**: ⏳ 需要手动安装

### 7. 企业微信 CLI
- **状态**: ⏳ 需要手动配置

### 8. 字节跳动 CLI
- **状态**: ⏳ 需要手动配置

---

## 📋 使用方法

### 腾讯云 CLI
```bash
# 查看云服务器列表
tccli cvm DescribeInstances

# 查看地域列表
tccli cvm DescribeRegions

# 创建云服务器
tccli cvm RunInstances --InstanceType S5.SMALL1 --ImageId img-xxx
```

### AWS CLI
```bash
# 配置凭证
aws configure

# 查看 S3 存储桶
aws s3 ls

# 查看 EC2 实例
aws ec2 describe-instances
```

### 阿里云 CLI
```bash
# 配置凭证
aliyuncli configure

# 查看 ECS 实例
aliyuncli ecs DescribeInstances
```

---

## 🔧 配置文件位置

- **腾讯云**: `~/.tccli/default.credential`
- **AWS**: `~/.aws/credentials`
- **阿里云**: `~/.aliyuncli/credentials`

---

## 🚀 下一步计划

1. ✅ 腾讯云 CLI 已配置
2. ⏳ 配置 AWS CLI 凭证
3. ⏳ 配置阿里云 CLI 凭证
4. ⏳ 安装 Google Cloud SDK
5. ⏳ 安装华为云 CLI
6. ⏳ 配置企业微信 CLI

---

_部署完成时间：2026-05-09 02:40 (Asia/Shanghai)_
_状态：部分完成_
