# Unlock Fastboot — Oppo MediaTek (Universal) to Unlock Bootloader
The script in this repository is designed to create a modified *preloader* based on the factory one, 
in which the fastboot lock flag is changed to unlocked.

---

## Instructions
* Download and install [Python](https://www.python.org/downloads) 3.4+ version (for MTKclient 3.10-3.13)
* Use [mtkclient](https://github.com/bkerler/mtkclient) and gui, or [GeekFlashTool](https://gitee.com/geekflashtool), or [Penumbra](https://github.com/shomykohai/penumbra) to read the preloader (boot1) dump from you Oppo
* Place the preloader backup in the same folder as preloader_path.py, making sure to name it boot1.bin
* Then double-click on the Python script.
* After the script finishes running, the finished preloader will be located in the preloader_path folder under the name boot1.bin
* Write the resulting boot1 to the device, use the supported tool
* Be sure to enable OEM Unlock in the developer settings
* Use adb and the [ adb reboot bootloader ] command to get into unlocked fastboot
* Then, after entering fastboot, use the [ fastboot flashing unlock ] command
* Confirm bootloader unlocking by pressing the Volume Up or Volume Down key. For clarity, read the text on the device screen after the unlock request
* Rejoice at the end of the bootloader unlocking ordeal...
---
## Example of a log of a successful patch creation
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
## Additionally
On the Russian 4pda forum, user Max_Goblin provides very detailed [instructions](https://4pda.to/forum/index.php?showtopic=1059838&view=findpost&p=136154776), including detailed installation of mtkclient for Windows, creating and restoring backups, a detailed description of using the graphical interface, and instructions for manually creating a patch for the preloader.

---
## Information about supported devices
| Model              | Device code    | SoC                | SoC ID            | Status                                                        |
|--------------------|----------------|--------------------|-------------------|---------------------------------------------------------------|
| Oppo A9X           | PCEM00 & PCET00| Helio P70          | MT6771            | MTKClient: Full support                                       |
| Oppo A15           | CPH2185        | Helio P35          | MT6765            | SBC enabled, but patch doesn't work                           |
| Oppo A17           | CPH2477        | Helio G35          | MT6765            | MTKClient: Full support                                       |
| Oppo A17           | CPH2477        | Helio G35          | MT6765            | MTKClient: Full support                                       |
| Oppo A17K          | CPH2471        | Helio G35          | MT6765            | MTKClient: Full support                                       |
| Oppo A18           | CPH2591        | Helio G85          | MT6768/MT6769     | Problems DAA GUI and cmd, auth_sv5.auth tested                |
| Oppo A35           | PEFM00         | Helio P35          | MT6765            | SBC is not enabled, not supported                             |
| Oppo A54 4G        | CPH2239        | Helio G35          | MT6765            | Problems DAA GUI and cmd, auth_sv5.auth not tested            |
| Oppo A55 4G        | CPH2325        | Helio G35          | MT6765            | Mtkclient: Full support                                       |
| Oppo A55 5G        | CPHPEMM00 & PEMT00| Dimensity 700 | MT6833           | GeekFlashTool: Full support                                   |
| Oppo A56 5G        | PFVM110        | Dimensity 700      | MT6833            | MTKClient: Full support                                       |
| Oppo A58 4G        | CPH2577        | Helio G85          | MT6768/MT6769     | Problems DAA gui and cmd, auth_sv5.auth not tested            |
| Oppo A58x          | PHJ110         | Dimensity 700      | MT6833            | Problems DAA gui and cmd, auth_sv5.auth tested                |
| Oppo A73 5G        | CPH2161        | Dimensity 720      | MT6853            | GUI support, to work without GUI, auth_sv5.auth is required.  |
| Oppo Pad 2         | OPD2201        | Dimensity 9000     | MT6983            | GeekFlashTool: Full support                                   |
| Oppo Reno 10 5g    | CPH2531        | Dimensity 7050     | MT6877V           | Problems DAA gui and cmd, auth_sv5.auth not tested            |
| Oppo Reno 11F 5g   | CPH2603        | Dimensity 7050     | MT6877V           | Problems DAA gui and cmd, auth_sv5.auth not tested            |
| Oppo Reno 4 Lite   | CPH2125        | Helio P95          | MT6779            | MTKClient: Full support                                       |
| Oppo Reno 5 Lite   | CPH2205        | Helio P95          | MT6779            | MTKClient: Full support                                       |
#### Ready-made preloaders are available on 4pda.
#### Problems with DAA don't necessarily mean unlocking isn't supported, especially if auth_sv5.auth hasn't been tested. For Oppo, it's usually simply impossible to find a valid DA, but I recommend trying.
#### If you've unlocked the bootloader of any Oppo device using mtkclient and this patch, please create an issue and let me know which new Oppo device this method worked for, preferably providing the stock preloader and the patched one. Alternatively, you can report that this method didn't work. You can also contact me on Telegram.
---
## This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.
