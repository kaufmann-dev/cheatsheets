# Lockbox Shows Password Prompt Twice

Fixed: 2026-06-28 22:39:44 CEST (+0200)

Commit at diagnosis: 3944181aff5176b3aaf0e8964ddfec7bf80aab70

## Symptom

Running `lockbox mount` showed two password prompts:

```text
Password:
Password:
Opening: /home/david/.SiriKali/Secret Folder
```

## Confirmed root cause

`lockbox` printed its own password prompt before reading the password silently. SiriKali also printed `Password:` while reading the piped password from stdin. Because SiriKali's output was passed through directly, both prompts appeared even though the password was only entered once.

## Changes made

- Capture SiriKali output during mount.
- Suppress SiriKali's duplicate `Password:` prompt on successful mount.
- Print captured SiriKali errors in red on failure.
- Add colored output helpers:
  - red for errors
  - green for verified success messages
  - yellow for benign warning states such as already mounted or not mounted
