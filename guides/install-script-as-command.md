# Install a Script as a Terminal Command

Use this when you have a script file and want to run it by typing a simple command name anywhere in the terminal.

## 1. Pick a command name

Example:

```bash
my-command
```

The command name should usually be lowercase and use hyphens instead of spaces.

## 2. Rename the script

Replace `script.sh` and `my-command` with your actual file name and desired command name:

```bash
mv script.sh my-command
```

If the file name contains spaces, use quotes:

```bash
mv "My Script.sh" my-command
```

## 3. Make it executable

```bash
chmod +x my-command
```

## 4. Install it globally

```bash
sudo install -m 755 my-command /usr/local/bin/my-command
```

Now you can run it from anywhere:

```bash
my-command
```

## 5. Test it

```bash
my-command --help
```

If the script has no help command, just run:

```bash
my-command
```

## Update the command later

If you edit the script, reinstall it with the same command:

```bash
sudo install -m 755 my-command /usr/local/bin/my-command
```

## Remove the command

```bash
sudo rm /usr/local/bin/my-command
```

## If it says `command not found`

Check that `/usr/local/bin` is in your PATH:

```bash
echo "$PATH"
```

On most Linux systems, `/usr/local/bin` is already included.