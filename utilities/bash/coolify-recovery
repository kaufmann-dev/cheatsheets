#!/usr/bin/env bash
# Coolify deployment recovery: diagnose and fix Docker build cache,
# unused image bloat, and missing swap on small VPSs.
# Run on the Coolify server as root or with sudo access.
# Requires: docker, bash 4+, GNU coreutils, awk, grep.

set -euo pipefail

# ---------------------------------------------------------------------------
# Colors and output helpers
# ---------------------------------------------------------------------------

if [[ -t 1 ]]; then
    RED='\033[0;31m'
    YEL='\033[1;33m'
    GRN='\033[0;32m'
    CYN='\033[0;36m'
    RST='\033[0m'
else
    RED=''
    YEL=''
    GRN=''
    CYN=''
    RST=''
fi

info() { printf "%b[info]%b  %s\n" "$CYN" "$RST" "$*"; }
warn() { printf "%b[warn]%b  %s\n" "$YEL" "$RST" "$*"; }
bad()  { printf "%b[!]%b     %s\n" "$RED" "$RST" "$*"; }
ok()   { printf "%b[ok]%b    %s\n" "$GRN" "$RST" "$*"; }

separator() { printf '\n%s\n\n' '────────────────────────────────────────────'; }

confirm() {
    local prompt="$1"

    if [[ ! -t 0 ]]; then
        bad "Confirmation required, but stdin is not interactive."
        return 1
    fi

    printf "%b%s [y/N]%b " "$YEL" "$prompt" "$RST"
    local ans
    read -r ans
    [[ "$ans" =~ ^[Yy]$ ]]
}

# ---------------------------------------------------------------------------
# Runtime setup and preflight
# ---------------------------------------------------------------------------

SUDO=()
DOCKER=(docker)

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || {
        bad "Missing required command: $1"
        exit 1
    }
}

setup_sudo() {
    if [[ $EUID -eq 0 ]]; then
        SUDO=()
        return 0
    fi

    if command -v sudo >/dev/null 2>&1; then
        SUDO=(sudo)
        return 0
    fi

    SUDO=()
}

need_root() {
    if [[ $EUID -eq 0 ]]; then
        return 0
    fi

    if [[ ${#SUDO[@]} -gt 0 ]]; then
        return 0
    fi

    bad "This action requires root. Re-run as root or install/use sudo."
    return 1
}

setup_docker_cmd() {
    if docker info >/dev/null 2>&1; then
        DOCKER=(docker)
        return 0
    fi

    if [[ ${#SUDO[@]} -gt 0 ]] && sudo docker info >/dev/null 2>&1; then
        DOCKER=(sudo docker)
        return 0
    fi

    bad "Docker is installed but not reachable. Run as root, use sudo, or fix Docker first."
    exit 1
}

preflight() {
    if (( BASH_VERSINFO[0] < 4 )); then
        bad "Bash 4+ is required. Current version: ${BASH_VERSION}"
        exit 1
    fi

    require_cmd docker
    require_cmd awk
    require_cmd grep
    require_cmd df
    require_cmd free
    require_cmd tail
    require_cmd tr
    require_cmd wc

    setup_sudo
    setup_docker_cmd
}

# ---------------------------------------------------------------------------
# Size and disk helpers
# ---------------------------------------------------------------------------

bytes_to_gib() {
    local bytes="$1"
    awk -v b="$bytes" 'BEGIN { printf "%.1fGiB", b / 1024 / 1024 / 1024 }'
}

parse_size_to_bytes() {
    # Accepts Docker-ish values such as: 123B, 42kB, 1.5MB, 3.74GB, 0B.
    local raw="$1"
    local num unit

    num=$(printf '%s' "$raw" | grep -oE '^[0-9]+([.][0-9]+)?' || true)
    unit=$(printf '%s' "$raw" | grep -oE '[[:alpha:]]+$' || true)

    if [[ -z "$num" ]]; then
        printf '0'
        return 0
    fi

    awk -v n="$num" -v u="$unit" '
        BEGIN {
            if (u == "B" || u == "") m = 1
            else if (u == "kB" || u == "KB") m = 1000
            else if (u == "MB") m = 1000 * 1000
            else if (u == "GB") m = 1000 * 1000 * 1000
            else if (u == "TB") m = 1000 * 1000 * 1000 * 1000
            else if (u == "KiB") m = 1024
            else if (u == "MiB") m = 1024 * 1024
            else if (u == "GiB") m = 1024 * 1024 * 1024
            else if (u == "TiB") m = 1024 * 1024 * 1024 * 1024
            else m = 1
            printf "%.0f", n * m
        }
    '
}

path_available_bytes() {
    local path="$1"
    df -B1 --output=avail "$path" 2>/dev/null | tail -n 1 | tr -dc '0-9'
}

path_used_percent() {
    local path="$1"
    df --output=pcent "$path" 2>/dev/null | tail -n 1 | tr -dc '0-9'
}

choose_swap_size() {
    # Automatic swap sizing based on free disk on /.
    # Thresholds intentionally leave free space after creating the swap file:
    #   >= 12GiB free -> 8G swap
    #   >=  7GiB free -> 4G swap
    #   >=  4GiB free -> 2G swap
    #   otherwise     -> do not create swap
    local avail_bytes
    avail_bytes=$(path_available_bytes /)

    local gib=$((1024 * 1024 * 1024))

    if [[ -z "$avail_bytes" ]]; then
        printf '0G'
    elif (( avail_bytes >= 12 * gib )); then
        printf '8G'
    elif (( avail_bytes >= 7 * gib )); then
        printf '4G'
    elif (( avail_bytes >= 4 * gib )); then
        printf '2G'
    else
        printf '0G'
    fi
}

size_to_bytes_for_swap() {
    local size="$1"
    case "$size" in
        2G) printf '%s' $((2 * 1024 * 1024 * 1024)) ;;
        4G) printf '%s' $((4 * 1024 * 1024 * 1024)) ;;
        8G) printf '%s' $((8 * 1024 * 1024 * 1024)) ;;
        *)  printf '0' ;;
    esac
}

# ---------------------------------------------------------------------------
# 1. Diagnostics
# ---------------------------------------------------------------------------

diagnose() {
    info "Hostname: $(hostname)"
    separator

    info "Disk usage"
    df -hT
    separator

    info "Inode usage"
    df -ih
    separator

    info "Memory & swap"
    free -h
    separator

    info "Swap devices"
    swapon --show 2>/dev/null || echo "(none)"
    separator

    info "Uptime / load"
    uptime
    separator

    info "Docker root"
    "${DOCKER[@]}" info --format 'DockerRootDir={{.DockerRootDir}} Driver={{.Driver}}' 2>/dev/null || warn "Could not read Docker info."
    separator

    info "Docker disk usage"
    "${DOCKER[@]}" system df
    separator

    info "BuildKit cache"
    "${DOCKER[@]}" builder du 2>/dev/null || warn "Could not read builder cache."
    separator
}

# ---------------------------------------------------------------------------
# 2. Analyse and flag problems
# ---------------------------------------------------------------------------

analyse() {
    local problems=0

    NEED_SWAP=0
    NEED_CACHE_PRUNE=0
    NEED_IMAGE_PRUNE=0

    # --- Swap check ---
    local swap_total
    swap_total=$(free -b | awk '/^Swap:/ {print $2}')
    if [[ "${swap_total:-0}" -eq 0 ]]; then
        local auto_size
        auto_size=$(choose_swap_size)
        if [[ "$auto_size" == "0G" ]]; then
            bad "No swap configured, and there is not enough free disk for automatic 2G/4G/8G swap creation."
        else
            bad "No swap configured. Recommended automatic swap size: $auto_size."
            NEED_SWAP=1
        fi
        ((problems++))
    else
        local swap_h
        swap_h=$(free -h | awk '/^Swap:/ {print $2}')
        ok "Swap present: $swap_h"
    fi

    # --- Disk free on Docker root ---
    local docker_root
    docker_root=$("${DOCKER[@]}" info --format '{{.DockerRootDir}}' 2>/dev/null || echo '/var/lib/docker')

    local disk_pct
    disk_pct=$(path_used_percent "$docker_root")
    if [[ -n "$disk_pct" ]] && (( disk_pct >= 85 )); then
        bad "Docker root ($docker_root) is at ${disk_pct}% usage."
        ((problems++))
    else
        ok "Docker root disk at ${disk_pct:-??}%"
    fi

    # --- BuildKit cache size ---
    local builder_du total_size cache_bytes
    builder_du=$("${DOCKER[@]}" builder du 2>/dev/null || true)
    total_size=$(printf '%s\n' "$builder_du" | awk '/^Total:/ {print $2; exit}')
    cache_bytes=$(parse_size_to_bytes "${total_size:-0B}")

    if [[ "$cache_bytes" -gt $((2 * 1024 * 1024 * 1024)) ]]; then
        bad "BuildKit cache is large: $(bytes_to_gib "$cache_bytes")"
        NEED_CACHE_PRUNE=1
        ((problems++))
    else
        ok "BuildKit cache size looks acceptable: $(bytes_to_gib "$cache_bytes")"
    fi

    # --- Unused images ---
    local dangling all_images
    dangling=$("${DOCKER[@]}" images --filter 'dangling=true' -q | wc -l | tr -d ' ')
    all_images=$("${DOCKER[@]}" images -q | wc -l | tr -d ' ')

    if [[ "$dangling" -gt 5 ]] || [[ "$all_images" -gt 30 ]]; then
        bad "Found $dangling dangling and $all_images total images."
        NEED_IMAGE_PRUNE=1
        ((problems++))
    else
        ok "$all_images images, $dangling dangling"
    fi

    # --- Recent OOM / disk errors in kernel log ---
    if command -v journalctl >/dev/null 2>&1; then
        local oom_hits
        oom_hits=$("${SUDO[@]}" journalctl -k --since '30 minutes ago' --no-pager 2>/dev/null \
            | grep -ciE 'oom|killed|no space|overlay|buildkit' || true)
        if [[ "$oom_hits" -gt 0 ]]; then
            bad "Kernel log mentions OOM/disk issues ($oom_hits hits in last 30 min)."
            ((problems++))
        fi
    fi

    separator
    if [[ "$problems" -eq 0 ]]; then
        ok "No obvious problems detected."
    else
        warn "$problems problem(s) detected."
    fi
}

# ---------------------------------------------------------------------------
# 3. Docker cleanup
# ---------------------------------------------------------------------------

docker_cleanup() {
    info "Docker cleanup."
    warn "This will NOT remove Docker volumes and will NOT stop or remove running containers."
    warn "It WILL remove stopped containers, BuildKit cache, and all images not referenced by any container."
    warn "Removed images may need to be pulled or rebuilt later."
    separator

    # Important: prune stopped containers first, so their old image references do not
    # prevent image cleanup from reclaiming space.
    if confirm "Prune stopped containers?"; then
        "${DOCKER[@]}" container prune --force
        ok "Stopped containers pruned."
    fi

    if confirm "Prune all images not referenced by containers?"; then
        "${DOCKER[@]}" image prune --all --force
        ok "Unused images pruned."
    fi

    if confirm "Prune BuildKit cache?"; then
        "${DOCKER[@]}" builder prune --all --force
        ok "BuildKit cache pruned."
    fi

    separator
    info "Post-cleanup disk state:"
    df -hT
    "${DOCKER[@]}" system df
}

# ---------------------------------------------------------------------------
# 4. Add swap
# ---------------------------------------------------------------------------

add_swap() {
    need_root || return 1

    local requested_size="${1:-auto}"
    local size

    if [[ "$requested_size" == "auto" ]]; then
        size=$(choose_swap_size)
    else
        size="$requested_size"
    fi

    if [[ "$size" != "2G" && "$size" != "4G" && "$size" != "8G" ]]; then
        bad "Invalid or impossible swap size: $size. Allowed: auto, 2G, 4G, 8G."
        return 1
    fi

    local swapfile='/swapfile'

    # Safety first: this script is meant to add missing swap, not stack extra swap
    # on top of an already configured system. If any swap is active, do nothing.
    if swapon --noheadings --show=NAME 2>/dev/null | grep -q .; then
        ok "Swap is already active. No new swap file will be created."
        swapon --show
        return 0
    fi

    local avail_bytes size_bytes
    avail_bytes=$(path_available_bytes /)
    size_bytes=$(size_to_bytes_for_swap "$size")

    if [[ -z "$avail_bytes" ]] || (( avail_bytes <= size_bytes )); then
        bad "Not enough free disk space to create $size swap at $swapfile."
        return 1
    fi

    if [[ -f "$swapfile" ]]; then
        warn "$swapfile exists but is not active. Trying to activate it."
        "${SUDO[@]}" chmod 600 "$swapfile"
        "${SUDO[@]}" swapon "$swapfile"
        ensure_swap_fstab "$swapfile"
        ok "Swap activated."
        free -h
        swapon --show
        return 0
    fi

    info "Creating $size swap file at $swapfile. Free disk before creation: $(bytes_to_gib "$avail_bytes")."

    if ! "${SUDO[@]}" fallocate -l "$size" "$swapfile" 2>/dev/null; then
        warn "fallocate failed. Falling back to dd; this can take a bit."
        local count_mb
        case "$size" in
            2G) count_mb=2048 ;;
            4G) count_mb=4096 ;;
            8G) count_mb=8192 ;;
        esac
        "${SUDO[@]}" dd if=/dev/zero of="$swapfile" bs=1M count="$count_mb" status=progress
    fi

    "${SUDO[@]}" chmod 600 "$swapfile"
    "${SUDO[@]}" mkswap "$swapfile"
    "${SUDO[@]}" swapon "$swapfile"
    ensure_swap_fstab "$swapfile"

    ok "Swap active:"
    free -h
    swapon --show
}

ensure_swap_fstab() {
    local swapfile="$1"

    if ! "${SUDO[@]}" grep -qsE "^[[:space:]]*${swapfile}[[:space:]]+none[[:space:]]+swap" /etc/fstab; then
        printf '%s\n' "$swapfile none swap sw 0 0" | "${SUDO[@]}" tee -a /etc/fstab >/dev/null
        ok "Added $swapfile to /etc/fstab."
    fi
}

# ---------------------------------------------------------------------------
# 5. Collect failure logs
# ---------------------------------------------------------------------------

collect_logs() {
    separator
    info "Docker service logs (last 10 min, tail 250)"
    if command -v journalctl >/dev/null 2>&1; then
        "${SUDO[@]}" journalctl -u docker --since '10 minutes ago' --no-pager 2>/dev/null \
            | tail -n 250 || warn "Could not read Docker journal."
    else
        warn "journalctl not found."
    fi
    separator

    info "Kernel OOM / disk errors (last 10 min)"
    if command -v journalctl >/dev/null 2>&1; then
        "${SUDO[@]}" journalctl -k --since '10 minutes ago' --no-pager 2>/dev/null \
            | grep -Ei 'oom|killed|no space|overlay|docker|buildkit|context canceled' || ok "No matches."
    else
        warn "journalctl not found."
    fi
    separator

    info "Docker disk usage"
    "${DOCKER[@]}" system df
    "${DOCKER[@]}" builder du 2>/dev/null || true
}

# ---------------------------------------------------------------------------
# 6. Restart Docker
# ---------------------------------------------------------------------------

restart_docker() {
    need_root || return 1

    warn "This will briefly interrupt all running containers."
    if confirm "Restart Docker?"; then
        "${SUDO[@]}" systemctl restart docker
        ok "Docker restarted."
    fi
}

# ---------------------------------------------------------------------------
# Interactive menu
# ---------------------------------------------------------------------------

menu() {
    echo ''
    info "Coolify Deployment Recovery"
    echo "  1) Diagnose        – show disk, memory, swap, Docker state"
    echo "  2) Analyse         – flag likely problems"
    echo "  3) Docker cleanup  – prune stopped containers, unused images, BuildKit cache"
    echo "  4) Add swap        – create auto-sized 2G/4G/8G swap file"
    echo "  5) Collect logs    – grab recent Docker and kernel logs"
    echo "  6) Restart Docker  – last resort, interrupts containers"
    echo "  7) Auto-fix        – run analyse → cleanup → swap if needed"
    echo "  q) Quit"
    echo ''
}

auto_fix() {
    NEED_SWAP=0
    NEED_CACHE_PRUNE=0
    NEED_IMAGE_PRUNE=0

    info "Running diagnostics."
    diagnose
    analyse

    if [[ "$NEED_CACHE_PRUNE" -eq 1 ]] || [[ "$NEED_IMAGE_PRUNE" -eq 1 ]]; then
        docker_cleanup
    else
        ok "Docker cleanup not needed."
    fi

    if [[ "$NEED_SWAP" -eq 1 ]]; then
        local auto_size
        auto_size=$(choose_swap_size)
        if [[ "$auto_size" == "0G" ]]; then
            bad "Swap is needed, but there is not enough free disk for automatic swap creation."
        elif confirm "Add $auto_size swap file?"; then
            add_swap "$auto_size"
        fi
    fi

    separator
    ok "Auto-fix complete. Retry one deployment in Coolify."
    warn "If it fails again, run option 5 (Collect logs) immediately after the failed deployment."
}

usage() {
    cat <<'USAGE'
Usage:
  coolify-recovery.sh                 # interactive menu
  coolify-recovery.sh diagnose
  coolify-recovery.sh analyse|analyze
  coolify-recovery.sh cleanup
  coolify-recovery.sh swap [auto|2G|4G|8G]
  coolify-recovery.sh logs
  coolify-recovery.sh restart
  coolify-recovery.sh auto
USAGE
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

main() {
    preflight

    if [[ $# -gt 0 ]]; then
        case "$1" in
            diagnose)       diagnose ;;
            analyse|analyze) diagnose; analyse ;;
            cleanup)        docker_cleanup ;;
            swap)           add_swap "${2:-auto}" ;;
            logs)           collect_logs ;;
            restart)        restart_docker ;;
            auto)           auto_fix ;;
            -h|--help|help) usage ;;
            *)              bad "Unknown command: $1"; usage; exit 1 ;;
        esac
        exit 0
    fi

    while true; do
        menu
        printf "%bChoose [1-7/q]:%b " "$CYN" "$RST"
        read -r choice
        case "$choice" in
            1) diagnose ;;
            2) diagnose; analyse ;;
            3) docker_cleanup ;;
            4) add_swap auto ;;
            5) collect_logs ;;
            6) restart_docker ;;
            7) auto_fix ;;
            q|Q) echo 'Bye.'; exit 0 ;;
            *) warn "Invalid choice." ;;
        esac
    done
}

main "$@"