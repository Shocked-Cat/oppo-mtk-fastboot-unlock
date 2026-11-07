#!/usr/bin/env python3
"""Bypass the OPPO fastboot authorisation check in the Oppo A35 (PEFM00) LK.

Background
----------
On the A35 (MT6765, ColorOS 11) `fastboot_init()` calls a vendor routine
before it brings up USB:

    VA 0x588A8ABE:  bl FUN_588A77E0
    VA 0x588A8AC2:  cmp r0, #0
    VA 0x588A8AC4:  beq.w 0x588A8ED6        ; "fastboot_unlock_verify ok"

FUN_588A77E0 (VA 0x588A77E0) reads a 4 KiB record from
`opporeserve1 + 0x440C00`, compares the stored serial with one derived from
`get_devinfo_with_index(12/13)`, and verifies an RSA-2048/PSS (SHA-256)
signature with a key embedded in LK.  A device that never went through
OPPO's authorised unlock channel has an all-zero record, so the call returns
-1, LK prints "the serial is not match" / "fastboot_unlock_verify fail",
sleeps 2 s and reboots.  USB fastboot is never initialised.

The seccfg "unlock" (lock_state 3 / orange) does NOT affect this check: it
only controls Android verified boot.

This script replaces the 4-byte BL with `movs r0,#0 ; nop`.  The following
CMP/BEQ then takes the success branch, so fastboot initialises normally.
The auth routine itself is left untouched.

LOCK NOTE
---------
A modified LK must still pass the Preloader's SBC certificate check
("sbc_en = 1" / "[SBC] cert verify, part = lk").  Always re-sign the image
with the CERT2 hash-override technique (see ./README.md) before flashing.

Usage
-----
    python3 patch_lk_fastboot.py stock-lk.bin [-o out.bin] [--entry]

--entry patches the prologue of FUN_588A77E0 (movs r0,#0 ; bx lr) instead
of the call site; use it only if a future build gains more call sites.
"""
import argparse
import hashlib
import struct
import sys

try:
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
except ImportError:  # capstone is optional, only used for verification
    Cs = None

# Stock OPPO A35 PEFM00 LK (oppo6765-3e02a00-20210728170313-2022101)
LOAD_ADDR = 0x58881688
AUTH_VA = 0x588A77E0            # FUN_588A77E0 - vendor fastboot auth
CALLSITE_VA = 0x588A8ABE        # bl FUN_588A77E0 inside fastboot_init
CALLSITE_ORIG = bytes.fromhex("fef78ffe")
PATCH_CALLSITE = bytes.fromhex("002000bf")   # movs r0,#0 ; nop
PATCH_ENTRY = bytes.fromhex("00207047")      # movs r0,#0 ; bx lr
ENTRY_ORIG = bytes.fromhex("2de9f04f")       # push.w {r4-r11, lr}


def va_to_off(va: int) -> int:
    return 0x200 + (va - LOAD_ADDR)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("lk", help="stock lk partition dump (4 MiB)")
    ap.add_argument("-o", "--out", help="output file")
    ap.add_argument("--entry", action="store_true",
                    help="patch FUN_588A77E0 prologue instead of the call site")
    args = ap.parse_args()

    data = bytearray(open(args.lk, "rb").read())
    if len(data) < 0x400:
        sys.exit("not an LK image (too small)")

    load = struct.unpack_from("<I", data, 0)[0]
    body_len = struct.unpack_from("<I", data, 4)[0]
    magic = bytes(data[8:12])
    print(f"file    : {args.lk} ({len(data)} bytes, sha256 {sha256(data)[:16]})")
    print(f"header  : load={load:#x} size={body_len:#x} magic={magic!r}")
    if load != LOAD_ADDR or magic[:2] != b"lk":
        sys.exit(f"!! unexpected LK header (expected load={LOAD_ADDR:#x}, "
                 f"magic 'lk')")

    if args.entry:
        off, orig, patch = va_to_off(AUTH_VA), ENTRY_ORIG, PATCH_ENTRY
        what = "FUN_588A77E0 prologue"
    else:
        off, orig, patch = va_to_off(CALLSITE_VA), CALLSITE_ORIG, PATCH_CALLSITE
        what = "fastboot_init call site"

    cur = bytes(data[off:off + 4])
    print(f"target  : {what} @ VA {LOAD_ADDR + off - 0x200:#x} "
          f"(file +{off:#x})")
    print(f"bytes   : {cur.hex()} -> {patch.hex()}")
    if cur != orig:
        sys.exit("!! unexpected bytes at patch site; refusing to patch "
                 "(dump your own lk and re-check offsets)")

    if Cs and not args.entry:
        md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
        ins = next(md.disasm(bytes(data[off:off + 4]),
                             LOAD_ADDR + off - 0x200), None)
        if ins:
            print(f"decoded : {ins.mnemonic} {ins.op_str}")
            if f"{AUTH_VA:#x}" not in ins.op_str:
                sys.exit("!! BL target is not the auth function; refusing")

    data[off:off + 4] = patch
    out = args.out or args.lk.replace(".bin", "-fastboot-patched.bin")
    if out == args.lk:
        sys.exit("refusing to overwrite input")
    open(out, "wb").write(data)
    print(f"output  : {out} (sha256 {sha256(bytes(data))})")

    if Cs and not args.entry:
        md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
        base = LOAD_ADDR + off - 0x200
        for ins in md.disasm(bytes(data[off:off + 12]), base):
            print(f"  {ins.address:#x}: {ins.mnemonic:<8} {ins.op_str}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
