## [中文版🇨🇳](README_zh-CN.md)

# Unlock Fastboot — Oppo MediaTek (Universal) to Unlock Bootloader
The script in this repository is designed to create a modified *preloader* based on the factory one, 
in which the fastboot lock flag is changed to unlocked.

## General information
* It has been discovered that on Realme devices, after flashing the modified preloader into fastboot, it is now impossible to log in using the buttons, but it is still possible to enter fastboot for example with the `adb reboot bootloader` command
* Android 10 and 15+ do not support this patch. Android 9 may also not support it, but only one device has been tested so far. This is not processor-dependent.
* It is impossible to fully edit RAW without verification, I don't know how to implement it. That is why this repository will not help you bypass LK verification on many Oppo & Realme

---

## Instructions
As an alternative to using a Python script, you can use this website: [PLOnline](https://lf-repo.github.io/PLOnline/) ([open source](https://github.com/LF-Repo/PLOnline)); or compiled exe [PLPatcher](https://github.com/LF-Repo/PLPatcher/releases/tag/1.0.1).

**It's important to understand that these projects aren't directly related to me, I don't monitor their relevance, and I don't contribute to their development. They were probably mostly created using Vibe Code, but that's better than .exe files that steal your personal data...**


* Download and install [Python](https://www.python.org/downloads) 3.4+ version (for MTKclient 3.10-3.13)
* Use [mtkclient](https://github.com/bkerler/mtkclient) and gui, or [GeekFlashTool](https://gitee.com/geekflashtool), or [Penumbra](https://github.com/shomykohai/penumbra) to read the preloader (boot1) dump from you Oppo. If your active slot is B, you must apply the patch to boot2. If slots A/B are missing, you must still apply the patch to boot1.
* Place the preloader backup in the same folder as preloader_path.py, making sure to name it boot1.bin, then double-click on the Python script. Or use cmd and CLI: `path_preloader.py [input file]`
* After the script finishes running, the finished preloader will be located in the preloader_path folder under the name boot1.bin
* Write the resulting preloader to the device, use the supported tool
* Be sure to enable OEM Unlock in the developer settings
* Use adb and the `adb reboot bootloader` command to get into unlocked fastboot
* Then, after entering fastboot, use the `fastboot flashing unlock` command
* Confirm bootloader unlocking by pressing the Volume Up or Volume Down key. For clarity, read the text on the device screen after the unlock request
* Rejoice at the end of the bootloader unlocking ordeal...
---
## Example of a log of a successful patch creation
```
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
---
## Information about supported devices
[You can see the list of tested devices here](https://github.com/Shocked-Cat/oppo-mtk-fastboot-unlock/blob/main/support_list.md)

- Issues with DAA do not necessarily mean that unlocking is not supported, especially if auth_sv5.auth has not been tested. You can try different programs besides mtkclient

- The auth_sv5.auth file can usually be easily extracted from official OFP or OZIP update files using oppo_decrypt

- If you have unlocked the bootloader of any Oppo device with this patch, please create a problem and let us know which new Oppo device this method worked for, preferably providing a standard preloader and patch, as well as mention the Android version, and what software you used to read and write the preloader. Alternatively, you can report that this method did not work. You can also contact me via Telegram.

## Disclaimer

This software is provided **"as is"** without any warranty of any kind, express or implied. By using this tool, you acknowledge that:
* Changing the preloader or flashing the altered images carries a **high risk of permanent damage to the device** ("brick").
* You are solely responsible for any consequences resulting from the use, misuse, or inability to use this software.
* The maintainers and contributors of this project are **not liable for any damage**, data loss, device malfunction, or legal issues that may arise.
* This project is intended for **educational and research purposes only**. It is **not intended for illegal or unauthorized use**.
* Upgrading via OTA will overwrite your preloader, but if you've used this repository as intended, you'll only have fastboot blocked, without turning your device into a brick.
* You can also update the RAW part of the preloader yourself, and this should not cause problems, but be careful, as updating the RAW may add additional locks or fixes. And also updating from Android 14 to Android 15 can entail an unpredictable result.

Proceed only if you fully understand the risks and implications.

---
## This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.
---
