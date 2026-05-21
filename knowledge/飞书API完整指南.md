# 飞书API完整指南

> 创建时间：2026-05-05 03:53
> 状态：已授权158个权限

---

## 一、当前授权权限

**已授权：** 158个权限
**待授权：** 0个权限

---

## 二、核心API能力

### 2.1 消息能力（im:message）

**可用功能：**
- ✅ 发送消息（im:message）
- ✅ 接收消息（im:message:readonly）
- ✅ 更新消息（im:message:update）
- ✅ 撤回消息（im:message:recall）
- ✅ 发送消息给多用户（im:message:send_multi_users）
- ✅ 发送消息给多部门（im:message:send_multi_depts）
- ✅ 以机器人身份发送（im:message:send_as_bot）
- ✅ 发送系统消息（im:message:send_sys_msg）
- ✅ 群消息（im:message.group_msg）
- ✅ P2P消息（im:message.p2p_msg:readonly）
- ✅ 群@消息（im:message.group_at_msg:readonly）
- ✅ 消息表情反应（im:message.reactions）
- ✅ 消息置顶（im:message.pins）
- ✅ 加急消息（im:message.urgent）
- ✅ 加急短信（im:message.urgent:sms）
- ✅ 加急电话（im:message.urgent:phone）

---

### 2.2 群聊能力（im:chat）

**可用功能：**
- ✅ 创建群聊（im:chat:create）
- ✅ 读取群聊信息（im:chat:read）
- ✅ 更新群聊信息（im:chat:update）
- ✅ 删除群聊（im:chat:delete）
- ✅ 群成员管理（im:chat.members）
- ✅ 群公告（im:chat.announcement）
- ✅ 群置顶消息（im:chat.chat_pins）
- ✅ 群菜单（im:chat.menu_tree）
- ✅ 群标签页（im:chat.tabs）
- ✅ 群插件（im:chat.collab_plugins）
- ✅ 群Widget（im:chat.widgets）
- ✅ 群管理员（im:chat.managers）
- ✅ 群置顶通知（im:chat.top_notice）
- ✅ 羡慕审核（im:chat.moderation）
- ✅ 以群主身份操作（im:chat:operate_as_owner）
- ✅ Bot访问群成员（im:chat.members:bot_access）

---

### 2.3 文档能力（docs:document）

**可用功能：**
- ✅ 读取文档内容（docs:document.content:read）
- ✅ 创建文档（docs:doc）
- ✅ 复制文档（docs:document:copy）
- ✅ 导入文档（docs:document:import）
- ✅ 导出文档（docs:document:export）
- ✅ 订阅文档（docs:document.subscription）
- ✅ 上传媒体文件（docs:document.media:upload）
- ✅ 下载媒体文件（docs:document.media:download）
- ✅ 文档评论（docs:document.comment）
- ✅ 文档权限管理（docs:permission）
- ✅ 文档事件订阅（docs:event）

---

### 2.4 云盘能力（drive:drive）

**可用功能：**
- ✅ 云盘读取（drive:drive:readonly）
- ✅ 云盘写入（drive:drive）
- ✅ 文件上传（drive:file:upload）
- ✅ 文件下载（drive:file:download）
- ✅ 文件读取（drive:file:readonly）
- ✅ 文件管理（drive:file）
- ✅ 云盘搜索（drive:drive.search:readonly）
- ✅ 云盘版本管理（drive:drive:version）
- ✅ 云盘元数据（drive:drive.metadata:readonly）
- ✅ 文件查看记录（drive:file:view_record:readonly）
- ✅ 文件点赞（drive:file.like:readonly）

---

### 2.5 通讯录能力（contact）

**可用功能：**
- ✅ 用户基础信息（contact:user.base:readonly）
- ✅ 用户详细信息（contact:user.employee:readonly）
- ✅ 用户ID（contact:user.id:readonly）
- ✅ 用户邮箱（contact:user.email:readonly）
- ✅ 用户电话（contact:user.phone:readonly）
- ✅ 用户部门（contact:user.department:readonly）
- ✅ 用户职位（contact:job_title:readonly）
- ✅ 用户职级（contact:job_level:readonly）
- ✅ 用户岗位族（contact:job_family:readonly）
- ✅ 用户性别（contact:user.gender:readonly）
- ✅ 用户工号（contact:user.employee_id:readonly）
- ✅ 用户员工号（contact:user.employee_number:read）
- ✅ 部门基础信息（contact:department.base:readonly）
- ✅ 部门组织信息（contact:department.organize:readonly）
- ✅ 部门HRBP（contact:department.hrbp:readonly）
- ✅ 用户群组（contact:group:readonly）
- ✅ 用户角色（contact:role:readonly）
- ✅ 功能角色（contact:functional_role:readonly）
- ✅ 工作城市（contact:work_city:readonly）
- ✅ 单位信息（contact:unit:readonly）

---

### 2.6 Wiki知识库能力（wiki）

**可用功能：**
- ✅ Wiki节点移动（wiki:node:move）

---

### 2.7 日历能力（calendar）

**可用功能：**
- ✅ 请假管理（calendar:timeoff）
- ✅ 请假创建（calendar:time_off:create）
- ✅ 请假删除（calendar:time_off:delete）

---

### 2.8 搜索能力（search）

**可用功能：**
- ✅ 文档搜索（search:docs:read）
- ✅ 搜索数据集创建（search:dataset.docs:create）
- ✅ 搜索数据集删除（search:dataset.docs:delete）

---

### 2.9 OCR能力（optical_char_recognition）

**可用功能：**
- ✅ 图片OCR识别（optical_char_recognition:image）

---

### 2.10 邮箱能力（mail）

**可用功能：**
- ✅ 邮箱联系人读取（mail:user_mailbox.mail_contact:read）
- ✅ 邮箱联系人写入（mail:user_mailbox.mail_contact:write）
- ✅ 邮箱联系人电话（mail:user_mailbox.mail_contact.phone:read）
- ✅ 邮箱联系人地址（mail:user_mailbox.mail_contact.mail_address:read）

---

### 2.11 视频会议能力（vc）

**可用功能：**
- ✅ 会议事件读取（vc:meeting.meetingevent:read）

---

### 2.12 CoreHR能力（corehr）

**可用功能：**
- ✅ 紧急联系人读取（corehr:person.emergency_contact:read）
- ✅ 紧急联系人写入（corehr:person.emergency_contact:write）
- ✅ 入离职时间（corehr:person.entry_leave_time:read）

---

### 2.13 考勤能力（attendance）

**可用功能：**
- ✅ 加班审批写入（attendance:overtime_approval:write）

---

## 三、常用API调用示例

### 3.1 发送消息

**工具：** message
**参数：**
```
action: send
channel: feishu
message: 消息内容
target: 用户ID或群ID
```

**示例：**
```
发送私聊消息：
target: ou_xxxxx
message: 你好！

发送群聊消息：
target: chat:oc_xxxxx
message: 大家好！
```

---

### 3.2 读取消息

**工具：** message
**参数：**
```
action: read
channel: feishu
chatId: 群ID或用户ID
limit: 消息数量
```

---

### 3.3 创建文档

**工具：** feishu_doc
**参数：**
```
action: create
title: 文档标题
content: 文档内容（Markdown）
folder_token: 文件夹token（可选）
```

---

### 3.4 读取文档

**工具：** feishu_doc
**参数：**
```
action: read
doc_token: 文档token
```

---

### 3.5 上传文件

**工具：** feishu_drive
**参数：**
```
action: upload
file_path: 本地文件路径
folder_token: 云盘文件夹token
```

---

### 3.6 获取用户信息

**工具：** feishu_chat
**参数：**
```
action: member_info
chat_id: 群ID
member_id: 用户ID
member_id_type: open_id
```

---

### 3.7 OCR识别

**工具：** exec（调用百度OCR）
**参数：**
```
使用百度OCR API识别图片文字
```

---

## 四、权限分类汇总

### 消息类（40个权限）
- 消息发送、接收、更新、撤回
- 群消息、私聊消息、@消息
- 消息反应、置顶、加急

### 群聊类（20个权限）
- 群创建、读取、更新、删除
- 群成员、公告、置顶、菜单
- 群插件、Widget、管理员

### 文档类（30个权限）
- 文档创建、读取、复制、导入导出
- 文档评论、权限、订阅
- 文档事件、媒体文件

### 云盘类（15个权限）
- 云盘读取、写入、搜索
- 文件上传、下载、管理
- 版本、元数据、查看记录

### 通讯录类（40个权限）
- 用户基础信息、详细信息
- 用户联系方式、部门、职位
- 部门信息、群组、角色

### 其他类（13个权限）
- Wiki、日历、搜索
- OCR、邮箱、视频会议
- CoreHR、考勤

---

## 五、API调用注意事项

### 5.1 用户ID类型

**支持的ID类型：**
- open_id（推荐）
- user_id
- union_id

**示例：**
```
ou_xxxxx（open_id）
user_xxxxx（user_id）
on_xxxxx（union_id）
```

---

### 5.2 群ID格式

**格式：**
```
chat:oc_xxxxx
```

---

### 5.3 文档token

**获取方式：**
- 从文档URL提取
- URL格式：/docx/xxx

---

### 5.4 文件夹token

**获取方式：**
- 从云盘URL提取
- 使用feishu_drive工具列出

---

## 六、常用场景示例

### 场景1：发送私聊消息

```
工具：message
参数：
  action: send
  channel: feishu
  target: ou_fea209144fdd2d485e564ba5b67ac832
  message: 你好，杨欢！
```

---

### 场景2：发送群聊消息

```
工具：message
参数：
  action: send
  channel: feishu
  target: chat:oc_12f7d1cdc6fdba16b8358123e8a71103
  message: 大家好！
```

---

### 场景3：创建文档

```
工具：feishu_doc
参数：
  action: create
  title: 新文档
  content: # 标题\n内容
```

---

### 场景4：读取群成员

```
工具：feishu_chat
参数：
  action: members
  chat_id: oc_12f7d1cdc6fdba16b8358123e8a71103
```

---

### 场景5：上传文件到云盘

```
工具：feishu_drive
参数：
  action: upload
  file_path: /path/to/file
  folder_token: fldxxxxx
```

---

## 七、总结

**飞书API能力完整覆盖：**
- ✅ 消息（发送、接收、管理）
- ✅ 群聊（创建、管理、成员）
- ✅ 文档（创建、编辑、权限）
- ✅ 云盘（上传、下载、搜索）
- ✅ 通讯录（用户、部门、群组）
- ✅ Wiki、日历、搜索、OCR、邮箱等

**已授权158个权限，API调用无限制！**

---

**创建时间：** 2026-05-05 03:53
**状态：** 完整API指南已创建