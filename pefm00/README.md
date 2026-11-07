# Oppo A35 (PEFM00 / MT6765) — full Fastboot via LK patch + CERT2 re-sign

**Status: tested on a retail PEFM00** (ColorOS 11 / Android 11,
`version-bootloader: oppo6765-3e02a00-20210728170313-2022101`).
`fastboot getvar all`, `fastboot boot` and the usual fastboot command set
work after this procedure.

This directory is for the A35, where the usual **preloader patch does not
work** (see the device table: "the patch did not open fastboot").  On this
model the fastboot gate is not in the preloader at all — it lives in LK, and
LK is protected by the Preloader's Secure Boot.

---

## 1. Why the preloader patch fails on PEFM00

There are three independent locks:

| Lock | Controls | Where |
|---|---|---|
| `seccfg` | Android verified boot state (orange) | SEJ-signed seccfg partition |
| OPPO fastboot auth | whether USB fastboot initialises at all | `opporeserve1 + 0x440C00`, RSA-PSS, bound to the device serial |
| SBC | Preloader verifying the `lk` image | OTP fuse (`SBC enabled: True`) |

`mtkclient da seccfg unlock` only flips the first one.  On the A35 the
`opporeserve1` authorisation record is **all zeroes** (the unit never went
through OPPO's "deep testing" channel), so `fastboot_init()` fails at
`FUN_588A77E0` before USB is brought up:

```
the serial is not match
fastboot_unlock_verify fail
```

and LK sleeps 2 s and reboots.

The preloader patch from this repository modifies the *preloader's* fastboot
flag, which the A35 LK ignores.  It cannot help here.

## 2. The two changes that are needed

### 2.1 LK: skip the fastboot authorisation call

```
VA 0x588A8ABE:  bl FUN_588A77E0      ->  movs r0, #0 ; nop
VA 0x588A8AC2:  cmp r0, #0
VA 0x588A8AC4:  beq.w 0x588A8ED6     ; "fastboot_unlock_verify ok"
```

`FUN_588A77E0` (VA `0x588A77E0`) reads the 4 KiB record at
`opporeserve1 + 0x440C00`, compares its serial field with the serial derived
from `get_devinfo_with_index(12/13)` and verifies an RSA-2048/PSS-SHA256
signature against a public key embedded in LK.  Replacing the four-byte BL
with `movs r0,#0 ; nop` makes the following `cmp`/`beq` take the success
branch.  The auth routine and its key are left untouched.

### 2.2 LK: re-sign `cert2` (SBC)

A modified `lk` image fails the Preloader's certificate check:

```
sbc_en = 1
[SBC] cert verify, part = lk, img = lk...ok    <- stock
[SBC] img auth fail                            <- modified, without re-sign
```

The `lk` partition is an MKIMG container:

```
lk (0x3c57a4) -> cert1 -> cert2 -> lk_main_dtb -> cert1 -> cert2
```

`cert2` contains, as DER objects:

* OID `2.16.886.2454.2.4` — BIT STRING, SHA-256 of the 0x200 image header;
* OID `2.16.886.2454.2.1` — BIT STRING, SHA-256 of the image data.

MTK's libsec picks the **first matching OID while walking the blob** instead
of restricting itself to the signed region (the logic flaw behind
CVE-2023-20696 and similar).  By prepending an extra set of these OIDs with
the *new* hashes before the original signed DER, the verifier compares the
recomputed hashes against the attacker-supplied values while the RSA
signature is still checked over the untouched original data.  The result is
a modified image that passes SBC without OPPO's private key.

This is implemented by [`pwnage24mtk`](https://github.com/kasnria001/pwnage24mtk)
(`sign_mtk_cert.py`).  Two layouts are supported; which one your libsec
accepts depends on its `bypass_mode`:

* `v6` — prepend a constructed `0xA0` block as a sibling before the DER;
* `legacy` — additionally wrap the original DER in a BIT STRING so an old
  parser that steps into objects still finds the `0x30 SEQUENCE`.

Try `v6` first, then `legacy`.

## 3. Requirements

* BROM access (mtkclient + a DAA-capable DA; on this device
  `Target config: 0xe5`, `DAA enabled: True`).
* A stock `lk` dump from **your** device (4 MiB).  The patch checks the
  header (`0x58881688`, `"lk"`) and the exact bytes at the patch site, and
  refuses to run on a different build.
* Python 3 + `capstone` (optional, for the disassembly check).
* `pwnage24mtk` cloned locally.

## 4. Procedure

```bash
# 0) back up everything that matters (BROM; one command per BROM session)
DA="/path/to/All in One Oppo & Realme.bin"
mtk --loader "$DA" r lk     lk-stock.bin
mtk --loader "$DA" r lk2    lk2-stock.bin
mtk --loader "$DA" r seccfg seccfg.bin
mtk --loader "$DA" r preloader preloader.bin --parttype boot1

# 1) build (patch + re-sign + truncate to 4 MiB)
git clone https://github.com/kasnria001/pwnage24mtk tools/pwnage24mtk
./build_lk.sh lk-stock.bin v6
#  -> lk-stock-v6-4m.bin

# 2) flash and reboot
mtk --loader "$DA" w lk lk-stock-v6-4m.bin
mtk --loader "$DA" reset
```

`mtk` leaves the device in DA state after each invocation; power-cycle and
re-enter BROM between commands (or use `mtk multi`).

If the device does not boot, or the Preloader logs
`[SBC] cert verify ... fail` / `Second Bootloader Load Failed`, restore the
stock image and try the other mode:

```bash
mtk --loader "$DA" w lk lk-stock.bin
mtk --loader "$DA" reset
mtk --loader "$DA" w lk lk-stock-v6-4m.bin   # or the legacy build
```

## 5. Verification

```
$ fastboot getvar all
(bootloader) serialno: NFDE8DBQSG5DTKWC
(bootloader) unlocked: yes
(bootloader) secure: no
(bootloader) kernel: lk
(bootloader) product: oppo6765
(bootloader) version-bootloader: oppo6765-3e02a00-20210728170313-2022101

$ fastboot boot output/boot-edk2-logo.img
Sending 'boot.img' (32768 KB)                      OKAY
Booting                                            OKAY
```

`fastboot oem device-info` returns `unknown command` — this LK does not
implement OEM commands; that is expected.

## 6. Important notes

* **Keep `lk-stock.bin` and the built image.** An OTA (or flashing the stock
  `lk`) restores the locked fastboot.  Re-apply the 4-byte patch + CERT2
  re-sign after every LK update.
* **Do not flash the stock `lk` and expect fastboot to stay open** — it will
  not.  Use the patched image.
* Do not write the preloader unless you have verified `SBC: 0`; on this
  device SBC is fused (`SBC enabled: True`), so a modified preloader will not
  boot.
* This is a vulnerability-based unlock, not an official one.  The OTP trust
  anchor is untouched, so the device remains "secure boot fused"; the method
  only abuses the parser.  Treat the device as fully compromised from a
  physical-access standpoint.
* If `fastboot flash` reports `failed to get download permission for
  partition '...'` there is a second, per-partition permission layer in LK;
  it can be patched and re-signed the same way.

## 7. Credits

* [`pwnage24mtk`](https://github.com/kasnria001/pwnage24mtk) — CERT2 hash
  override implementation and the CVE background (CVE-2023-20696,
  CVE-2025-20730).
* [`mtkclient`](https://github.com/bkerler/mtkclient) — BROM/DA access.
* Original preloader-patch project this repository is based on.

## 8. 中文摘要

A35（PEFM00）的 fastboot 不在 preloader 的锁里，而在 LK 的
`FUN_588A77E0`（读 `opporeserve1+0x440C00` 的 RSA-PSS 授权记录）。本机该记录
全 0，所以必失败。做法是：把 `fastboot_init` 里对它的调用改成返回 0（4 字节），
再用 CERT2 解析漏洞（`pwnage24mtk`）重签改过的 LK，绕过 Preloader 的 SBC。
已验证 `fastboot getvar all` / `fastboot boot` 可用。改过的 LK 必须重签，
否则 Preloader 会 `img auth fail`；OTA 覆盖 LK 后需重做。
