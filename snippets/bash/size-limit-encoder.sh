#!/bin/bash

INPUT="$1"
TARGET_MB="$2"

AUDIO_BITRATE_K=128

DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$INPUT")

BITRATE_K=$(awk "BEGIN {
    target_bits = $TARGET_MB * 1024 * 1024 * 8;
    video_bitrate = int((target_bits/1000 - $AUDIO_BITRATE_K * $DURATION)/$DURATION);
    print video_bitrate
}")

echo "Target video bitrate: ${BITRATE_K}k"
echo "Audio bitrate: ${AUDIO_BITRATE_K}k"

ffmpeg -y -i "$INPUT" \
    -c:v libx264 -preset medium -b:v "${BITRATE_K}k" \
    -c:a aac -b:a "${AUDIO_BITRATE_K}k" \
    -pass 1 -f mp4 /dev/null

ffmpeg -i "$INPUT" \
    -c:v libx264 -preset medium -b:v "${BITRATE_K}k" \
    -c:a aac -b:a "${AUDIO_BITRATE_K}k" \
    -pass 2 "${INPUT%.*}-$TARGET_MB"MB.mp4