#!/usr/bin/env bash
set -eu -o pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
output="${1:?Pass the destination directory.}"
work="$(mktemp -d)"
trap 'python3 -c "import shutil,sys;shutil.rmtree(sys.argv[1])" "$work"' EXIT
"${CC:-cc}" -std=c11 -O2 -Wall -Wextra -Werror -I"$root/src" "$root/src/state.c" "$root/tests/fixture_frames.c" -o "$work/fixture"
for temperature in 15 25 35; do
  mkdir -p "$output/${temperature}C"
  (cd "$output/${temperature}C" && "$work/fixture" "$temperature" | tee mask.txt)
done
