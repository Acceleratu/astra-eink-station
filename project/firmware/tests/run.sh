#!/usr/bin/env bash
set -eu -o pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'python3 -c "import shutil,sys;shutil.rmtree(sys.argv[1])" "$work"' EXIT
"${CC:-cc}" -std=c11 -O1 -g -fsanitize=address,undefined -Wall -Wextra -Werror \
  -I"$root/src" "$root/src/state.c" "$root/src/panel.c" "$root/src/calendar.c" \
  "$root/tests/fault_test.c" -o "$work/fault_test"
"$work/fault_test" "$@"
"${CC:-cc}" -std=c11 -O1 -g -fsanitize=address,undefined -Wall -Wextra -Werror \
  -I"$root/src" -I"$root/tests/rtc_shim" "$root/src/clock.c" "$root/src/calendar.c" \
  "$root/tests/rtc_register_test.c" -o "$work/rtc_register_test"
"$work/rtc_register_test"
