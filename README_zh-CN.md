# Fastboot 解锁工具 — Oppo 联发科（通用）Bootloader 解锁方案
本仓库中的脚本用于基于设备原厂预加载器（preloader）制作修改版镜像，将其中的 Fastboot 锁定标志位修改为解锁状态。

## 概述
该修改方案以类工程模式的思路，对预加载器主体进行处理。
全部功能基于一个预加载器漏洞利用技巧实现。仅当 **SBC（安全启动校验，Secure Boot Check）状态为开启（True）**，且通过 `m_sec_boot` 完成启用时，才可对 SBC 状态进行修改。存在少量例外情况，仍需进一步研究验证。

在不通过签名校验的情况下，无法对 RAW 数据进行完整编辑，目前我也未找到实现方法。
因此本方案**无法帮你绕过多数 Oppo 机型的 LK 校验**。

---

## 使用步骤
* 下载并安装 [Python](https://www.python.org/downloads) 3.4 及以上版本（MTKclient 推荐使用 3.10-3.13 版本）
* 使用 [mtkclient](https://github.com/bkerler/mtkclient)（含图形界面）、[GeekFlashTool](https://gitee.com/geekflashtool) 或 [Penumbra](https://github.com/shomykohai/penumbra)，从你的 Oppo 设备中读取预加载器（boot1）镜像备份
* 将预加载器备份放到与 `preloader_path.py` 同级的目录中，并重命名为 `boot1.bin`
* 双击运行该 Python 脚本
* 脚本运行完成后，修改完成的预加载器镜像将生成在 `preloader_path` 文件夹内，文件名为 `boot1.bin`
* 使用上述支持的工具，将生成的 `boot1.bin` 刷入设备
* 务必在设备开发者选项中开启 **OEM 解锁**
* 使用 ADB 命令进入已解锁的 Fastboot 模式：
  ```
  adb reboot bootloader
  ```
* 进入 Fastboot 模式后，执行 Bootloader 解锁命令：
  ```
  fastboot flashing unlock
  ```
* 按设备屏幕上的提示，通过音量上键或音量下键确认 Bootloader 解锁操作
* 恭喜你，终于完成了 Bootloader 解锁的全部流程

---

## 补丁生成成功的日志示例
```
Dev. Max_Goblin - 4pda
boot1.bin found state: successfully
Memory type: EMMC_BOOT
Flag block find state: successfully
lock state: 22 (lock)
Write range zeros: 0x800:0x2000
Jump offset code: 0x800 to 0x2000
--------------------
Change BRLYT offset
0x20d: 08 -> 20
0x21d: 08 -> 20
0x211: 08 -> 10
0x212: 08 -> 10
0x221: 08 -> 10
0x222: 08 -> 10
--------------------
Write flag block to: 0x1000
Fastboot lock state: 0x22 -> 00
Create new preloader to: С:\mtkclient\mtkclient_2.0.1\preloader_path\boot1.bin
Press Enter to close
```

## 补充说明
俄罗斯 4PDA 论坛用户 **Max_Goblin** 提供了超详细的[图文教程](https://4pda.to/forum/index.php?showtopic=1059838&view=findpost&p=136154776)，内容包括：Windows 系统下 mtkclient 的完整安装步骤、设备分区备份与恢复方法、图形界面详细使用指南，以及手动制作 preloader 补丁的完整教程。

---

## 支持设备列表
| 机型                | 设备代号             | 芯片平台           | SoC ID         | 支持状态                                                                 |
|---------------------|----------------------|--------------------|----------------|--------------------------------------------------------------------------|
| Oppo A9X            | PCEM00 & PCET00      | Helio P70          | MT6771         | MTKClient：完整支持                                                      |
| Oppo A15            | CPH2185              | Helio P35          | MT6765         | SBC 已启用，但补丁无效                                                   |
| Oppo A17            | CPH2477              | Helio G35          | MT6765         | MTKClient：完整支持                                                      |
| Oppo A17            | CPH2477              | Helio G35          | MT6765         | MTKClient：完整支持                                                      |
| Oppo A17K           | CPH2471              | Helio G35          | MT6765         | MTKClient：完整支持                                                      |
| Oppo A18            | CPH2591              | Helio G85          | MT6768/MT6769  | 图形界面与命令行存在 DAA 相关问题，已完成 auth_sv5.auth 适配测试       |
| Oppo A35            | PEFM00               | Helio P35          | MT6765         | SBC 未启用，不支持本方案                                                 |
| Oppo A54 4G         | CPH2239              | Helio G35          | MT6765         | 图形界面与命令行存在 DAA 相关问题，未完成 auth_sv5.auth 适配测试       |
| Oppo A55 4G         | CPH2325              | Helio G35          | MT6765         | MTKClient：完整支持                                                      |
| Oppo A55 5G         | CPHPEMM00 & PEMT00   | Dimensity 700      | MT6833         | GeekFlashTool：完整支持                                                  |
| Oppo A56 5G         | PFVM110              | Dimensity 700      | MT6833         | MTKClient：完整支持                                                      |
| Oppo A58 4G         | CPH2577              | Helio G85          | MT6768/MT6769  | 图形界面与命令行存在 DAA 相关问题，未完成 auth_sv5.auth 适配测试       |
| Oppo A58x           | PHJ110               | Dimensity 700      | MT6833         | GeekFlashTool：仅支持 Android 12；[O+ Support Tool]：完整支持          |
| Oppo A73 5G         | CPH2161              | Dimensity 720      | MT6853         | 支持图形界面操作；无图形界面操作需搭配 auth_sv5.auth 使用               |
| OPPO F31 Pro 5G     | CPH2763              | Dimensity 7300     | MT6878         | [O+ Support Tool]：支持；未知原因导致补丁无效                            |
| Oppo Pad 2          | OPD2201              | Dimensity 9000     | MT6983         | GeekFlashTool：完整支持                                                  |
| Oppo Reno 10 5g     | CPH2531              | Dimensity 7050     | MT6877V        | 图形界面与命令行存在 DAA 相关问题，未完成 auth_sv5.auth 适配测试       |
| Oppo Reno 11F 5g    | CPH2603              | Dimensity 7050     | MT6877V        | 图形界面与命令行存在 DAA 相关问题，未完成 auth_sv5.auth 适配测试       |
| Oppo Reno 4 Lite    | CPH2125              | Helio P95          | MT6779         | MTKClient：完整支持                                                      |
| Oppo Reno 5 Lite    | CPH2205              | Helio P95          | MT6779         | MTKClient：完整支持                                                      |

#### 4PDA 论坛已提供现成的预加载器修改镜像。
#### 出现 DAA 相关问题，不代表设备一定不支持解锁，尤其是未测试 auth_sv5.auth 的情况下。对于 Oppo 机型，通常只是难以找到可用的 DA 文件，仍建议尝试。
#### 如果你通过 mtkclient 和本补丁成功解锁了任意 Oppo 设备的 Bootloader，欢迎提交 Issue 告知适配成功的新机型，建议一并提供原厂预加载器和修改后的补丁文件。你也可以反馈本方案无效的机型情况，或通过 Telegram 联系我。

---

## 许可协议
本项目采用 **AGPL-3.0** 开源许可协议。详见 [LICENSE](LICENSE) 文件了解完整许可条款。