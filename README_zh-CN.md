## 翻译协助来自 [MengWanYu](https://github.com/MengWanYu)

# 解锁Fastboot——OPPO MediaTek (通用版) 解锁Bootloader

本仓库中的脚本用于基于原厂preloader制作修改版，将其中的fastboot锁定标识修改为解锁状态。

## 通用说明

经实测发现，Realme设备在fastboot模式下刷入修改版preloader后，将无法通过物理按键进入相关模式。

本修改方法以类工程模式的方式加载大部分preloader，整个操作均通过preloader漏洞这一“小技巧”实现。仅当SBC（Secure Boot Check）为开启状态（SBC: True）且通过m_sec_boot启用时，才可对SBC状态进行操作，极少数特殊情况仍需进一步验证。

目前无法在无校验的情况下对RAW进行完整编辑，相关实现方法暂未攻克，因此本仓库方案无法帮助你绕过多款OPPO设备的LK校验。

## 操作步骤

1. 下载并安装Python 3.4+版本（mtkclient建议使用3.10-3.13版本）

2. 使用mtkclient（含图形界面）、GeekFlashTool或Penumbra，从你的OPPO设备中读取preloader（boot1）镜像文件

3. 将preloader备份文件放入preloader_path.py同目录下，并重命名为boot1.bin

4. 双击运行该Python脚本

5. 脚本运行完成后，修改后的preloader将保存在preloader_path文件夹中，文件名为boot1.bin

6. 使用兼容工具将生成的boot1刷入设备

7. 务必在开发者选项中开启OEM Unlock功能

8. 通过ADB执行「adb reboot bootloader」命令，进入解锁后的fastboot模式

9. 进入fastboot后，执行「fastboot flashing unlock」命令

10. 按下音量上键/下键确认解锁Bootloader，操作前请仔细查看设备屏幕的解锁提示文字

11. 完成以上步骤，即可结束Bootloader解锁的操作流程

## 补丁制作成功的日志示例

```Plain Text

Dev. Max_Goblin - 4pda
Mode: Default
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

俄罗斯4pda论坛的用户Max_Goblin提供了超详细的操作教程，包含Windows系统下mtkclient的完整安装、备份的创建与恢复、图形界面的详细使用，以及手动制作preloader补丁的方法，教程链接：[https://4pda.to/forum/index.php?showtopic=1059838&view=findpost&p=136154776](https://4pda.to/forum/index.php?showtopic=1059838&view=findpost&p=136154776)

## 设备支持情况

|机型|设备代码|SoC|SoC ID|支持状态|
|---|---|---|---|---|
|Oppo A9X|PCEM00 & PCET00.|Helio P70|MT6771|MTKClient: 完全支持|
|Oppo A15|CPH2185|Helio P35|MT6765|SBC开启，但补丁无效|
|Oppo A17|CPH2477|Helio G35|MT6765|MTKClient: 完全支持|
|Oppo A17K|CPH2471|Helio G35|MT6765|MTKClient: 完全支持|
|Oppo A18|CPH2591|Helio G85|MT6768/MT6769|DAA图形界面及命令行存在问题，已测试auth_sv5.auth|
|Oppo A35|PEFM00|Helio P35|MT6765|SBC未开启，暂不支持|
|Oppo A54 4G|CPH2239|Helio G35|MT6765|DAA图形界面及命令行存在问题，未测试auth_sv5.auth|
|Oppo A55 4G|CPH2325|Helio G35|MT6765|Mtkclient: 完全支持|
|Oppo A55 5G|CPHPEMM00 & PEMT00|Dimensity 700|MT6833|GeekFlashTool: 完全支持|
|Oppo A56 5G|PFVM110|Dimensity 700|MT6833|MTKClient: 完全支持|
|Oppo A58 4G|CPH2577|Helio G85|MT6768/MT6769|DAA图形界面及命令行存在问题，未测试auth_sv5.auth|
|Oppo A58x|PHJ110|Dimensity 700|MT6833|GeekFlashTool: 仅支持Android 12；[O+ Support Tool]: 完全支持|
|Oppo A73 5G|CPH2161|Dimensity 720|MT6853|MTKClient 图形界面支持；无图形界面运行需auth_sv5.auth|
|Oppo A93s|PFGM00|Dimensity 700|MT6833|MTKClient: 完全支持|
|OPPO F31 Pro 5G|CPH2763|Dimensity 7300|MT6878|[O+ Support Tool]: 支持；补丁无效，原因未知|
|Oppo K9 Pro|PEYM00|Dimensity 1200|MT6893|GeekFlashTool: 完全支持|
|Oppo Pad 2|OPD2201|Dimensity 9000|MT6983|GeekFlashTool: 完全支持|
|Oppo Reno 10 5g|CPH2531|Dimensity 7050|MT6877V|DAA图形界面及命令行存在问题，未测试auth_sv5.auth|
|Oppo Reno 11F 5g|CPH2603|Dimensity 7050|MT6877V|DAA图形界面及命令行存在问题，未测试auth_sv5.auth|
|Oppo Reno 3 5G|CPH2125|Dimensity 1000L|MT6885|MTKClient: 完全支持|
|Oppo Reno 4 Lite|CPH2125|Helio P95|MT6779|MTKClient: 完全支持|
|Oppo Reno 5 Lite|CPH2205|Helio P95|MT6779|MTKClient: 完全支持|
|Oppo Reno 5 Z|CPH2211|Dimensity 800U|MT6853|MTKClient + [DA](https://archive.diablosat.cc/firmwares/amt-dumps/Oppo_Realme_Oneplus_DA/DA_BR_MT6853.bin): 完全支持|
|Realme 12 Plus|RMX3867|Dimensity 7050|MT6877|MTKClient + [DA MT6877](https://archive.diablosat.cc/firmwares/amt-dumps/Oppo_Realme_Oneplus_DA/): 支持；补丁无法解锁fastboot，疑似因Android 15+，Android 14未测试，SBC状态未知|
|Realme GT Neo|RMX3031|Dimensity 1200|MT6893|GeekFlashTool: 完全支持|
|Realme V11 5G|RMX3121 & RMX3122|Dimensity 700|MT6833|GeekFlashTool: 完全支持|
#### 4pda论坛提供现成的preloader文件

#### DAA出现问题不代表无法解锁，尤其是未测试auth_sv5.auth的情况，可尝试mtkclient之外的其他工具

#### 若通过本补丁成功解锁任意OPPO设备的Bootloader，欢迎提交Issue反馈，注明解锁的新机型；建议同时提供原厂preloader、制作的补丁，说明设备的Android版本及读写preloader所用的工具。若解锁失败，也可进行反馈，也可通过Telegram与我联系。

## 协议说明

本项目基于AGPL-3.0协议授权，详细条款见[LICENSE](LICENSE)文件。

## 免责声明

本软件按**现状**提供，不承担任何明示或默示的担保责任。使用本工具即表示你认可以下条款：

- 修改preloader或刷入修改后的镜像文件，存在设备**永久损坏（变砖）**的高风险。

- 因使用、误用或无法使用本软件产生的任何后果，均由你自行承担全部责任。

- 本项目的维护者和贡献者，对由此产生的任何设备损坏、数据丢失、设备故障或法律问题，**不承担任何赔偿责任**。

- 本项目仅用于**教育和研究目的**，**禁止用于非法或未授权的用途**。
  
- 在 Android 15 及以上系统上应用此补丁不会解锁 fastboot，且总体上研究不足。仅在对自己的操作完全有把握时才进行。

- 通过 OTA 升级会覆盖你的 preloader（引导加载程序），但如果你按照本仓库的预期使用，通常只是导致 fastboot 被锁定，而不会让设备变砖。

- 你也可以自行更新 preloader 的 RAW 部分，这通常不会引起问题，但要小心，因为更新 RAW 可能会引入额外的锁定或修复。另外，从 Android 14 升级到 Android 15 可能会产生不可预料的后果。

请在充分理解所有风险和影响后再进行操作。

