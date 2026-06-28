# Lockbox Mount Fails When Unlocked Folder Exists

Fixed: 2026-06-28 22:28:22 CEST (+0200)

Commit at diagnosis: 9bee155543667b36bd0660eb98b1de68b06051e2

## Symptom

Running `lockbox mount` prompted for the password, then SiriKali printed:

```text
Failed To Create Mount Point.
lockbox: mount failed
```

## Confirmed root cause

`lockbox config` and `lockbox mount` created the final unlocked folder before calling SiriKali. SiriKali CLI mounting passes `reUseMP=false`, so an existing mount directory is rejected with `Failed To Create Mount Point.`

Evidence:

- The saved config used `mount_dir=/home/david/.SiriKali/Secret Folder`.
- That directory existed and was empty, but was not mounted.
- SiriKali source checks `utility::pathExists(opt.mountPoint)` and returns `failedToCreateMountPoint` when `reUseMP` is false.

## Changes made

- Stop creating the final unlocked folder during `lockbox config`; create only its parent directory.
- Before mounting, remove the configured unlocked folder only if it already exists and is empty.
- Refuse to mount if the unlocked folder exists and is not empty, to avoid hiding existing files.
- Keep opening the unlocked folder with `xdg-open` after a successful mount.
