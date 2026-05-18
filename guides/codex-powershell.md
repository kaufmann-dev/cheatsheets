# Codex PowerShell & Git Setup

## 1. PowerShell (64-bit)

1. Search **PowerShell** in the Start Menu, right-click it, and select **Run as Administrator**.
2. Run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
   ```
3. Press `Y` to confirm.

## 2. PowerShell x86 (32-bit)

1. Search **PowerShell x86** in the Start Menu, right-click it, and select **Run as Administrator**.
2. Run the same command:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
   ```
3. Press `Y` to confirm.

## 3. Git Safe Directory

Open any terminal and run:
```bash
git config --global --add safe.directory *
```

---

Done. Codex can now run PowerShell scripts and Git commands without errors.