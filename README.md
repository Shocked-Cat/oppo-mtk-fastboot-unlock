# Unlock Fastboot — Oppo MediaTek (Universal) to Unlock Bootloader
The script in this repository is designed to create a modified *preloader* based on the factory one, 
in which the fastboot lock flag is changed to unlocked.

---

## Instructions
* Download and install [Python](https://www.python.org/downloads) 3.4+ version
* Use [mtkclient](https://github.com/bkerler/mtkclient) and gui to read the preloader (boot1) dump from you Oppo
* Place the preloader backup in the same folder as preloader_path.py, making sure to name it boot1.bin
* Then double-click on the Python script.
* After the script finishes running, the finished preloader will be located in the preloader_path folder under the name boot1.bin
* Writing the resulting preloader to the device, use the same mtkclient and gui
* Be sure to enable OEM Unlock in the developer settings
* Use adb and the adb reboot bootloader command to get into unlocked fastboot
* Then, after entering fastboot, use the fastboot flashing unlock command
* Confirm bootloader unlocking by pressing the Volume Up or Volume Down key. For clarity, read the text on the device screen after the unlock request
* Rejoice at the end of the bootloader unlocking ordeal...
---
## Example of a log of a successful patch creation
```
Dev. Max_Goblin - 4pda
boot1.bin found state: successfully
Flag block find state: successfully
lock state: 22 (lock)
Write range zeros: 0x800:0x2000
Jupm offset code: 0x800 to 0x2000
0x20d: 08 -> 10
0x21d: 08 -> 10
0x211: 08 -> 20
0x212: 04 -> 20
0x221: 08 -> 20
0x222: 04 -> 20
Write flag block to: 0x1000
Fastboot lock state: 0x22 -> 00
Create new preloader to: С:\mtkclient\mtkclient_2.0.1\preloader_path\boot1.bin
Press Enter to close
```
## Additionally
On the Russian 4pda forum, user Max_Goblin provides very detailed [instructions](https://4pda.to/forum/index.php?showtopic=1059838&view=findpost&p=136154776), including detailed installation of mtkclient for Windows, creating and restoring backups, a detailed description of using the graphical interface, and instructions for manually creating a patch for the preloader.

---

## This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.
