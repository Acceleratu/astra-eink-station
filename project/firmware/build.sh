#!/usr/bin/env bash
set -eu -o pipefail
: "${ZEPHYR_BASE:?Set ZEPHYR_BASE to the pinned Zephyr v4.3.0 checkout.}"
: "${ZEPHYR_SDK_INSTALL_DIR:?Set ZEPHYR_SDK_INSTALL_DIR to Zephyr SDK 0.17.4.}"
root="$(cd "$(dirname "$0")" && pwd)"
out="${ASTRA_OUTPUT_DIR:-$root/artifacts}"
mkdir -p "$out"
out="$(cd "$out" && pwd)"
work="$(mktemp -d)"
trap 'python3 -c "import shutil,sys;shutil.rmtree(sys.argv[1])" "$work"' EXIT
# A private source/build directory also works when the project lives in a path with an apostrophe.
mkdir "$work/app"
cp -R "$root/src" "$root/boards" "$root/dts" "$root/CMakeLists.txt" "$root/prj.conf" "$work/app"
cd "$ZEPHYR_BASE"
if [ "$(git rev-parse HEAD)" != 3568e1b6d5cdd51a6b964a2a1d6d29200fea2056 ]; then
  echo "This firmware release requires Zephyr v4.3.0 (3568e1b6)." >&2
  exit 1
fi
west build -b astra54/nrf54l15/cpuapp -d "$work/build" "$work/app" 2>&1 | tee "$out/build.log"
cp "$work/build/zephyr/zephyr.hex" "$out/astra.hex"
cp "$work/build/zephyr/zephyr.elf" "$out/astra.elf"
cp "$work/build/zephyr/zephyr.dts" "$out/resolved.dts"
cp "$work/build/zephyr/.config" "$out/zephyr.config"
python3 "$root/tests/verify_image.py" "$out/astra.elf" "$out/astra.hex" | tee "$out/image-check.txt"
