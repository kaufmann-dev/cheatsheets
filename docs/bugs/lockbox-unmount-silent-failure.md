# Lockbox Unmount Silently Leaves Folder Mounted

Fixed: 2026-06-28 22:34:17 CEST (+0200)

Commit at diagnosis: 3def5671432688b73673915b7ff4e4ce9a6744cf

## Symptom

Running `lockbox unmount` returned to the shell without printing anything. The unlocked folder still appeared accessible afterward, so the command looked successful even though it did not clearly confirm that the folder was unmounted.

## Confirmed root cause

The wrapper called:

```sh
sirikali -u "$mount_dir"
```

SiriKali's CLI unmount path checks for `-u`, but reads the target path from `-d`. Passing the mount path as the value after `-u` meant SiriKali did not receive the path it expected. The wrapper also did not verify that the mount point disappeared after the command.

Evidence:

- SiriKali source handles CLI unmount by reading `utility::cmdArgumentValue(args, "-d")`.
- The wrapper used `sirikali -u "$mount_dir"` instead of `sirikali -u -d "$mount_dir"`.
- The wrapper printed no success or failure message after the SiriKali command.

## Changes made

- Call SiriKali unmount as `sirikali -u -d "$mount_dir"`.
- Fail loudly if SiriKali returns a non-zero status.
- Re-check the mount point after unmount and fail loudly if it is still mounted.
- Print `Unmounted: <path>` after a verified successful unmount.
