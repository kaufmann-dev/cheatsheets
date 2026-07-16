# SSTP Split Tunneling for Remmina on Linux

Route a work RDP connection through an SSTP VPN while keeping normal internet traffic on the regular Wi-Fi or wired connection.

This guide uses NetworkManager and the following example values:

- VPN profile: `SSTP Bildungsdirektion`
- RDP server: `172.27.67.6`

Only traffic addressed to the RDP server uses the VPN. Other applications continue to use the normal internet connection.

> Confirm that the organization's VPN policy permits split tunneling before enabling it.

---

## 1. Check the saved VPN profile

List NetworkManager connections:

```bash
nmcli connection show
```

Check the relevant routing settings:

```bash
nmcli -f \
  connection.id,connection.type, \
  ipv4.never-default,ipv4.routes, \
  ipv6.never-default \
  connection show 'SSTP Bildungsdirektion'
```

---

## 2. Enable split tunneling

Prevent the VPN from replacing the normal IPv4 and IPv6 default routes:

```bash
nmcli connection modify 'SSTP Bildungsdirektion' \
  ipv4.never-default yes \
  ipv6.never-default yes
```

Add a host route so the RDP server uses the VPN:

```bash
nmcli connection modify 'SSTP Bildungsdirektion' \
  +ipv4.routes '172.27.67.6/32'
```

The `/32` suffix restricts the route to that single IPv4 address.

---

## 3. Connect the VPN

Connect from GNOME Settings, or run:

```bash
nmcli connection up 'SSTP Bildungsdirektion'
```

Open the saved Remmina connection after the VPN connects.

---

## 4. Verify the routes

Confirm that the RDP server uses the VPN interface, commonly `ppp0` for SSTP:

```bash
ip -4 route get 172.27.67.6
```

Expected shape:

```text
172.27.67.6 dev ppp0 src <vpn-address>
```

Confirm that ordinary internet traffic still uses the normal network interface:

```bash
ip -4 route get 1.1.1.1
```

Expected shape for Wi-Fi:

```text
1.1.1.1 via <router-address> dev <wifi-interface> src <local-address>
```

The exact interface and address names vary by machine.

---

## 5. Normal usage

1. Turn on `SSTP Bildungsdirektion` in GNOME Settings.
2. Open Remmina and connect to `172.27.67.6`.
3. Use other applications normally; their internet traffic remains outside the VPN.
4. Turn off the VPN after finishing work.

This configuration is destination-based rather than application-based. Any application connecting to `172.27.67.6` will use the VPN, while Remmina traffic to other addresses will not.

---

## Undo the configuration

Remove the RDP host route and allow the VPN to become the default route again:

```bash
nmcli connection modify 'SSTP Bildungsdirektion' \
  -ipv4.routes '172.27.67.6/32' \
  ipv4.never-default no \
  ipv6.never-default no
```

Disconnect and reconnect the VPN for the updated settings to take effect:

```bash
nmcli connection down 'SSTP Bildungsdirektion'
nmcli connection up 'SSTP Bildungsdirektion'
```

---

## Troubleshooting

### RDP no longer connects

Check that the destination stored in Remmina still matches the configured route:

```bash
rg '^server=' ~/.local/share/remmina ~/.config/remmina 2>/dev/null
```

If the server address changed, remove the old `/32` route and add the new address.

### Internet still uses the VPN

Verify both `never-default` values:

```bash
nmcli -f ipv4.never-default,ipv6.never-default \
  connection show 'SSTP Bildungsdirektion'
```

Both values should be `yes`.

### The work server uses a hostname

If Remmina uses a hostname instead of an IP address, corporate DNS may also need split-DNS configuration. Resolve the hostname while connected and configure the resulting company subnet or stable server address rather than assuming the address will remain unchanged.
