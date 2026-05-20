# Passwordless SSH Login on Windows Terminal

Connect to your Linux VPS without entering a password every time.

---

## Step 1: Generate an SSH Key

Open **PowerShell** or **Command Prompt** and run:

```powershell
ssh-keygen -t ed25519
```

- Press **Enter** to accept the default save path
- Leave the passphrase **blank** (just press Enter) for no password prompt

Your keys are saved to:
- Private key: `C:\Users\YourName\.ssh\id_ed25519`
- Public key: `C:\Users\YourName\.ssh\id_ed25519.pub`

> **Why ed25519?** It's faster, more secure, and produces smaller keys than the default RSA. Use RSA only if your server is very old (pre-2014).

---

## Step 2: Copy Your Public Key to the VPS

Run this command, replacing `user` and `your-vps-ip` with your actual details:

```powershell
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh user@your-vps-ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

You'll be asked for your password **one last time**.

---

## Step 3: Test the Connection

```powershell
ssh user@your-vps-ip
```

It should connect immediately with no password prompt.

---

## Step 4: Fix Permissions (if it still asks for a password)

SSH on Linux is strict about file permissions. Log in and run:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

## Optional: Specify the Key in Your Windows Terminal Profile

If you have multiple keys, tell SSH which one to use with `-i`:

```
ssh -i C:\Users\YourName\.ssh\id_ed25519 user@your-vps-ip
```

If you only have one key, SSH picks it up automatically.