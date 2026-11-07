#!/usr/bin/env bash
# Build a patched + SBC-re-signed LK for the Oppo A35 (PEFM00 / MT6765).
#
#   ./build_lk.sh stock-lk.bin [v6|legacy] [path/to/sign_mtk_cert.py]
#
# 1. patch the fastboot authorisation call site            (patch_lk_fastboot.py)
# 2. re-sign CERT2 with hash overrides                     (pwnage24mtk)
# 3. truncate back to the 4 MiB "lk" partition
#
# sign_mtk_cert.py comes from https://github.com/kasnria001/pwnage24mtk
# (clone it anywhere and pass the path, or keep it in ./tools/).
set -euo pipefail
cd "$(dirname "$0")"

SRC=${1:?usage: $0 <stock-lk.bin> [v6|legacy] [sign_mtk_cert.py]}
MODE=${2:-v6}
SIGN=${3:-./tools/pwnage24mtk/sign_mtk_cert.py}

[ -f "$SIGN" ] || {
	echo "!! missing $SIGN" >&2
	echo "   git clone https://github.com/kasnria001/pwnage24mtk tools/pwnage24mtk" >&2
	exit 1
}

BASE=${SRC%.bin}
PATCHED="$BASE-fastboot-patched.bin"
python3 patch_lk_fastboot.py "$SRC" -o "$PATCHED"

SIGNED="$BASE-$MODE-signed.bin"
if [ "$MODE" = "legacy" ]; then
	python3 "$SIGN" -w --legacy "$PATCHED" -o "$SIGNED"
else
	python3 "$SIGN" -w "$PATCHED" -o "$SIGNED"
fi

OUT="$BASE-$MODE-4m.bin"
python3 - "$SIGNED" "$OUT" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
d = open(src, "rb").read()
if len(d) < 4194304:
    sys.exit("signed image smaller than the lk partition (4 MiB)")
if any(d[4194304:]):
    sys.exit("content beyond 4 MiB - refusing to truncate")
open(dst, "wb").write(d[:4194304])
print(f"wrote {dst} (4194304 bytes)")
PY
sha256sum "$OUT"
