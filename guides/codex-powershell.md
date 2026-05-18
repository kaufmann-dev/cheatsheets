# Codex PowerShell Execution Policy Setup

Follow these steps to configure your execution policy for Codex in both PowerShell versions.

## 1. Configure Standard PowerShell (64-bit)
* Open your Windows Start Menu.
* Type `PowerShell`.
* Right-click **Windows PowerShell** and select **Run as Administrator**.
* Paste the following command and press Enter:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine`
* Type `Y` and press Enter to confirm the change.

## 2. Configure PowerShell x86 (32-bit)
* Open your Windows Start Menu again.
* Type `PowerShell x86`.
* Right-click **Windows PowerShell (x86)** and select **Run as Administrator**.
* Paste the same command and press Enter:
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine`
* Type `Y` and press Enter to confirm.

Your execution policies are now set up for Codex.
