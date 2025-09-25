#!/usr/bin/env bash
set -euo pipefail

# use: nix-shell -p python3Packages.fonttools python3Packages.brotli

ICONS="power_settings_new keyboard_arrow_up keyboard_arrow_left keyboard_arrow_right keyboard_arrow_down arrow_back home menu volume_mute volume_down volume_up"
SRC_URL="https://fonts.gstatic.com/s/materialsymbolsrounded/v284/sykg-zNym6YjUruM-QrEh7-nyTnjDwKNJ_190Fjzag.woff2"
OUT_FILE="samsung_remote/assets/material-symbols.woff2"
TMP_FONT='/tmp/material-symbols.woff2'
TMP_INST="/tmp/material-symbols-rounded.inst.ttf"

if [[ ! -s "$TMP_FONT" ]]; then
  curl -L --fail --no-progress-meter -o "$TMP_FONT" "$SRC_URL"
fi

# 2) instantiate axes: Filled@wght=400, opsz=24 (Rounded file; FILL axis controls filled)
fonttools varLib.instancer "$TMP_FONT" FILL=1 wght=400 GRAD=0 opsz=24 -o "$TMP_INST"

# 3) subset to just the ligature names (+ underscore for names)
pyftsubset "$TMP_INST" \
  --output-file="$OUT_FILE" \
  --flavor=woff2 \
  --text="$ICONS" \
  --unicodes=U+005F \
  --layout-features='liga' \
  --no-hinting \
  --drop-tables+=DSIG
