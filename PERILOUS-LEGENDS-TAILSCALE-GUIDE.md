# Perilous Legends — Connecting via Tailscale
*For Mike: how to connect to the server without port forwarding*
*Written by Enoch — 2026-03-08*

---

## What is Tailscale?

Tailscale is a free VPN that lets two computers talk to each other directly over the internet as if they were on the same local network. No router configuration needed. Takes about 5 minutes to set up.

---

## PART 1 — Akasha Sets Up Tailscale (Server Side)

**Akasha does this once on the laptop that runs the server.**

### Step 1: Install Tailscale on the server laptop

Download from: **https://tailscale.com/download/windows**

Run the installer. It adds a Tailscale icon to the system tray (bottom right of taskbar).

### Step 2: Create a Tailscale account

Go to **https://login.tailscale.com** and sign up. Use Google or GitHub to sign in — no new password needed.

### Step 3: Authenticate the laptop

Click the Tailscale icon in the system tray → **Log in** → it opens a browser → approve the device.

### Step 4: Find your Tailscale IP

Click the Tailscale icon in the system tray → it shows your IP, something like:

```
100.x.x.x
```

**Send this IP to Mike** — this is what he connects to.

### Step 5: Share access with Mike

Go to **https://login.tailscale.com/admin/users** → **Invite user** → enter Mike's email.

Or share via the Tailscale app: click the tray icon → **Admin console** → **Users** → Invite.

---

## PART 2 — Mike Sets Up Tailscale (Client Side)

### Step 1: Install Tailscale

Download from: **https://tailscale.com/download/windows**

Run the installer.

### Step 2: Log in

Click the Tailscale icon in your system tray → **Log in** → sign in with Google or GitHub.

### Step 3: Accept the invite from Akasha

Check your email for a Tailscale invite from Akasha. Accept it — this joins you to his network.

> If you don't get an invite email, you can still connect as long as both of you are logged into Tailscale — Tailscale handles the routing automatically.

### Step 4: Verify connection

Click the Tailscale tray icon — you should see Akasha's laptop listed as a connected device with a `100.x.x.x` IP address.

---

## PART 3 — Connect to Perilous Legends

### Step 5: Install UO and ClassicUO

Follow the main player guide: **https://github.com/TestamentsTCG/Share-Files/blob/master/PERILOUS-LEGENDS-PLAYER-GUIDE.md**

### Step 6: Set up the server profile in ClassicUO

In ClassicUO Launcher → New Profile:

| Field | Value |
|-------|-------|
| Profile Name | Perilous Legends |
| UO Data Path | `C:\Program Files (x86)\Electronic Arts\Ultima Online Classic\` |
| Server IP | **Akasha's Tailscale IP (100.x.x.x)** |
| Port | `2593` |
| Client Version | `7.0.15.1` |

### Step 7: Launch and create your account

Click Play. At the login screen:
- Type a new username and password
- Click Login — account is created automatically on first login
- Tell Akasha your character name to get GM access

---

## Troubleshooting

### Can't see Akasha's device in Tailscale
- Make sure both of you are logged into Tailscale and it shows "Connected" in the tray
- Try signing out and back in on Tailscale

### Connection refused on port 2593
- Confirm Akasha's Tailscale IP (ask him to check his tray icon)
- Make sure the server is running — ask Akasha to confirm

### Tailscale shows connected but game won't connect
- Double-check the IP in your ClassicUO profile is the Tailscale IP (100.x.x.x), not a local IP (192.168.x.x)

---

*Once Tailscale is working this is the permanent solution — no router config ever needed.*
