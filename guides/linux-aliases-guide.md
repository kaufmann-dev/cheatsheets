# Simple Guide: Linux Aliases

Aliases let you create short custom commands for your terminal.

Example:

```bash
alias ls='eza --icons'
```

After this, typing `ls` will run `eza --icons`.

---

## 1. Check which shell you use

Run:

```bash
echo $SHELL
```

Common results:

```bash
/bin/bash
/bin/zsh
/bin/fish
```

---

## 2. Add an alias for Bash

If you use Bash, add aliases to:

```bash
~/.bashrc
```

Example:

```bash
echo "alias ls='eza --icons'" >> ~/.bashrc
source ~/.bashrc
```

---

## 3. Add an alias for Zsh

If you use Zsh, add aliases to:

```bash
~/.zshrc
```

Example:

```bash
echo "alias ls='eza --icons'" >> ~/.zshrc
source ~/.zshrc
```

---

## 4. Add an alias for Fish

If you use Fish, add aliases to:

```bash
~/.config/fish/config.fish
```

Example:

```fish
echo "alias ls='eza --icons'" >> ~/.config/fish/config.fish
source ~/.config/fish/config.fish
```

---

## 5. Recommended way: edit the file manually

Open your shell config file:

```bash
nano ~/.bashrc
```

or:

```bash
nano ~/.zshrc
```

Then add aliases at the bottom:

```bash
alias ls='eza --icons'
alias ll='eza -la --icons'
alias gs='git status'
alias gc='git commit'
```

Save and reload:

```bash
source ~/.bashrc
```

or:

```bash
source ~/.zshrc
```

---

## 6. See your active aliases

Run:

```bash
alias
```

To check one alias:

```bash
alias ls
```

---

## 7. Remove an alias temporarily

This only removes it for the current terminal session:

```bash
unalias ls
```

To remove it permanently, delete the alias line from your shell config file.

---

## 8. Bypass an alias

If `ls` is aliased but you want the original system command, use:

```bash
command ls
```

or:

```bash
/bin/ls
```

This is useful in scripts or coding-agent environments.

---

## 9. Important notes

Aliases usually affect your interactive terminal only.

They normally do not affect:

- scripts
- CI/CD
- most coding agents
- commands run in non-interactive shells

But if a tool opens an interactive shell that loads your config, then aliases can affect it.

---

## 10. Good alias examples

```bash
alias ls='eza --icons'
alias ll='eza -la --icons'
alias la='eza -a --icons'
alias grep='grep --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias gs='git status'
alias gp='git pull'
alias gl='git log --oneline --graph --decorate'
```
