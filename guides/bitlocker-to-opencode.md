# Migration Guide: BitLocker → VeraCrypt + exFAT + FreeFileSync

## Overview

This guide migrates you from a Windows-only BitLocker multi-drive backup system to a cross-platform setup using VeraCrypt containers on exFAT-formatted drives, synced with FreeFileSync. The result works on Windows, macOS, and Linux.

**Target setup:**
- Drive A (primary) — exFAT + VeraCrypt container
- Drive B (backup) — exFAT + VeraCrypt container
- FreeFileSync mirrors A → B on demand

### Why exFAT — and its one rule

exFAT lacks journaling, which means an interrupted write can corrupt the filesystem. However, in this setup the outer exFAT drive only ever manages **one single file** (the VeraCrypt container), and VeraCrypt performs a clean flush on dismount before the OS touches the drive again. This eliminates virtually all corruption risk — **as long as you always dismount via VeraCrypt before unplugging.** Never yank the drive while the container is mounted. That is the only rule.

---

## Before You Start

**What you need:**
- Your two new NVMe drives in enclosures
- A third temporary drive or enough free space on your PC (to hold data during migration)
- VeraCrypt installed: https://veracrypt.fr
- FreeFileSync installed: https://freefilesync.org

**Time estimate:** 2–6 hours depending on data size.

> ⚠️ Do NOT format or touch your existing BitLocker drives until your data is fully on the new drives and verified.

---

## Phase 1 — Decrypt Your Existing BitLocker Data

### Step 1: Unlock your BitLocker drives

1. Plug in your existing BitLocker drive(s)
2. Windows will prompt for your BitLocker password/PIN — enter it
3. The drive appears as normal in File Explorer

### Step 2: Copy data to a temporary location

Copy everything off your BitLocker drives onto your PC's internal drive (or a temporary external drive). You need a staging area while you set up the new drives.

```
Suggested temp folder: C:\Migration_Temp\
```

Do **not** skip this step. You want your data in at least two places at all times.

### Step 3: Verify the copy

After copying, spot-check a few folders and files. Make sure nothing is missing or corrupted before continuing.

---

## Phase 2 — Prepare Drive A (Primary)

### Step 4: Format Drive A as exFAT

1. Plug in Drive A (your first new NVMe enclosure)
2. Open **Disk Management** (Win+X → Disk Management)
3. Find the new drive — right-click → **Format**
4. Settings:
   - File system: **exFAT**
   - Allocation unit size: **Default**
   - Volume label: e.g. `DriveA`
5. Click OK and wait

> On Linux you can use: `mkfs.exfat /dev/sdX`  
> On macOS: Disk Utility → Erase → exFAT

### Step 5: Create a VeraCrypt container on Drive A

1. Open VeraCrypt
2. Click **Create Volume**
3. Choose **Create an encrypted file container**
4. Choose **Standard VeraCrypt volume**
5. Click **Select File** → navigate to Drive A → name it something like `vault.vc`
6. Encryption settings (leave defaults — they're excellent):
   - Encryption: AES
   - Hash: SHA-512
7. Set the **container size** — leave ~1–2 GB free on the drive, use the rest
8. Set a **strong password** (20+ characters recommended — use a passphrase like 4 random words)
9. Format options:
   - Filesystem inside the container: **exFAT** (for large file support)
   - Click **Format** and move your mouse randomly to generate entropy
10. Wait for formatting to complete — click **Exit**

> 💡 Save your password in a password manager (Bitwarden) immediately.

### Step 6: Mount and fill Drive A

1. In VeraCrypt, click **Select File** → choose `vault.vc` on Drive A
2. Pick any drive letter (e.g. `Y:`) → click **Mount**
3. Enter your password
4. Drive A's container is now mounted as `Y:\`
5. Copy your data from `C:\Migration_Temp\` into `Y:\`
6. When done, go back to VeraCrypt → **Dismount**

---

## Phase 3 — Prepare Drive B (Backup)

### Step 7: Format Drive B as exFAT

Same as Step 4, but for Drive B. Label it `DriveB`.

### Step 8: Create a VeraCrypt container on Drive B

Repeat Step 5 exactly — same size, **same password** (this keeps things simple when syncing).

> Using the same password for both containers means FreeFileSync can sync the raw container file, and you can open either drive with the same password. If you prefer different passwords for extra security, that works too — just remember both.

---

## Phase 4 — Set Up FreeFileSync

FreeFileSync will sync the VeraCrypt **container file** (vault.vc) from Drive A to Drive B. The containers stay encrypted during sync — FreeFileSync never sees the contents.

### Step 9: Create a sync job

1. Open FreeFileSync
2. Left side (source): path to `vault.vc` on Drive A (e.g. `E:\vault.vc`)
3. Right side (target): path to `vault.vc` on Drive B (e.g. `F:\vault.vc`)
4. Click the arrow between them → set to **Mirror →**
   - Mirror means Drive B always becomes an exact copy of Drive A
   - Files deleted on A will also be deleted on B
5. Click **Compare** to see the differences
6. Click **Synchronize** to run the sync

### Step 10: Save as a batch job

1. File → **Save as Batch Job**
2. Save it to your desktop as `sync-backup.ffs_batch`
3. Now you can double-click this file anytime to run the sync in one click

> 💡 You can also schedule it via Windows Task Scheduler to run automatically, e.g. every Sunday night.

---

## Phase 5 — Verify Everything Works

### Step 11: Full verification checklist

- [ ] Mount `vault.vc` from Drive A → browse files → all data present
- [ ] Dismount Drive A
- [ ] Run FreeFileSync sync job
- [ ] Mount `vault.vc` from Drive B → browse files → matches Drive A
- [ ] Dismount Drive B
- [ ] Unplug both drives, replug → mount successfully on password entry

### Step 12: Test on another OS (optional but recommended)

If you're switching to Linux, test now while still on Windows:
- Boot a Linux live USB (Ubuntu)
- Install VeraCrypt
- Mount Drive A's container
- Confirm files are accessible

---

## Phase 6 — Clean Up BitLocker Drives

Only do this after Step 11 is fully complete and you're confident in the new setup.

### Step 13: Wipe old BitLocker drives

1. In Disk Management, right-click the old drive → **Format**
2. Or use VeraCrypt to **wipe** them: Create Volume → Encrypt non-system partition → Full format (overwrites with random data for secure erasure)

---

## Daily Workflow Going Forward

```
1. Plug in drive → mount vault.vc in VeraCrypt → work normally
2. When done → Dismount in VeraCrypt FIRST → then unplug
3. Never unplug while the container is still mounted
4. Weekly (or whenever) → run sync-backup.ffs_batch to mirror A → B
5. Drives sit encrypted and unplugged when not in use
```

> ⚠️ **The dismount rule.** exFAT has no journaling. VeraCrypt's dismount is your safety net — it flushes all pending writes and closes the container cleanly before the drive is touched. Skipping this and unplugging while mounted is the one thing that can cause corruption. Make it muscle memory: dismount before unplug, always.

---

## Switching to Linux Later

When you move to Linux, the workflow is identical:

```bash
# Install VeraCrypt
sudo apt install veracrypt   # or download from veracrypt.fr

# Mount container
veracrypt /media/driveA/vault.vc /mnt/vault

# Dismount
veracrypt -d /mnt/vault
```

FreeFileSync also has a native Linux build — same batch job file works.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| VeraCrypt won't mount | Check password, check drive is not write-protected |
| FreeFileSync shows container as "different" even after sync | Check both containers are same size; a size mismatch means recreate Drive B container |
| Drive not recognised on Linux | Install `exfat-utils`: `sudo apt install exfat-fuse exfat-utils` |
| Forgot password | No recovery possible — this is by design. Use Bitwarden. |
| Container file corrupted | Restore from Drive B — this is why you have two drives |
| Drive unplugged while container was mounted | Check exFAT with `fsck.exfat /dev/sdX` on Linux or chkdsk on Windows; if container is damaged, restore from Drive B |