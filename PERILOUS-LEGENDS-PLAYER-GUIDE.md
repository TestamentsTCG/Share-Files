# Perilous Legends — Player Setup Guide for Mike
*How to install UO, connect to the server, and get started*
*Written by Enoch — 2026-03-08*

---

## What You're Installing

- **Ultima Online** — the game client (data files)
- **ClassicUO** — the modern launcher/client that connects to private shards
- **Perilous Legends profile** — the server connection settings

---

## PART 1 — Install Ultima Online Client

You need the UO data files first. The easiest source is the official free download.

### Step 1: Download UO Classic Client

Go to: **https://uo.com/client-download/**

Download the **Ultima Online Classic Client** installer. Run it and install to the default location:
```
C:\Program Files (x86)\Electronic Arts\Ultima Online Classic\
```

> This gives you the data files (art, sounds, maps). You won't actually play through this launcher — ClassicUO replaces it.

---

## PART 2 — Install ClassicUO Launcher

### Step 2: Download ClassicUO Launcher

Go to: **https://github.com/ClassicUO/ClassicUO/releases/latest**

Download `ClassicUOLauncher-win-x64-Release.zip` (or the latest Windows release).

Extract it anywhere — suggested location:
```
C:\ClassicUO\
```

Run `ClassicUOLauncher.exe` once to initialize it.

---

## PART 3 — Set Up Perilous Legends Profile

### Step 3: Create a new profile in ClassicUO

1. Open `ClassicUOLauncher.exe`
2. Click **New Profile** (or the + button)
3. Fill in:

| Field | Value |
|-------|-------|
| Profile Name | Perilous Legends |
| UO Data Path | `C:\Program Files (x86)\Electronic Arts\Ultima Online Classic\` |
| Server IP | **[ASK AKASHA FOR IP]** |
| Port | `2593` |
| Client Version | `7.0.15.1` |

4. Save the profile

### Step 4: Launch the game

Click **Play** on the Perilous Legends profile.

---

## PART 4 — Create Your Account

### Step 5: Account creation (in-game)

When the login screen appears:
1. Type a new username in the **Account Name** field
2. Type a password in the **Password** field
3. Click **Login** — if the account doesn't exist, ServUO creates it automatically

> You don't need to register anywhere first. Just type the name you want and log in.

### Step 6: Create your character

- Pick a name
- Choose **Human** race
- Distribute your starting skills however you like — you'll be getting GM access anyway
- Pick any starting location

---

## PART 5 — Getting GM Access

Once you're in the game, tell Akasha your character name and he'll grant GM access.

**Akasha's instructions (for granting GM):**
In-game, Akasha types:
```
[setaccesslevel "CharacterName" GameMaster
```
Or via the ServUO admin panel.

With GM access you can:
- Use `[add` to spawn items and NPCs
- Use `[go` to teleport anywhere
- Use `[props` to inspect and edit objects
- Use `[where` to find coordinates
- Right-click anything for admin context menu

---

## PART 6 — GitHub Access (Proposals Repo)

You have been invited to two repos in the **PerilousLegends** GitHub organization:

| Repo | Your Access | Link |
|------|-------------|------|
| PerilousLegends (main code) | Read only | github.com/PerilousLegends/PerilousLegends |
| Proposals (your sandbox) | Read + Write | github.com/PerilousLegends/Proposals |

### Accepting the invites

Check your email (mhaid32@gmail.com) for two GitHub invitation emails. Click **Accept invitation** in each one.

Or go directly to: **github.com/notifications** and accept from there.

### Submitting a proposal

1. Clone the Proposals repo:
```bash
git clone https://github.com/PerilousLegends/Proposals.git
```

2. Create a folder in `proposals/` named with today's date and a short description:
```
proposals/2026-03-10-new-class-idea/
```

3. Add a `README.md` following the template in the repo's main README

4. Commit and push:
```bash
git add .
git commit -m "Proposal: [short description]"
git push
```

5. Tell Akasha — he'll have Enoch review it before anything gets merged to the main codebase

---

## Troubleshooting

### Can't connect to server
- Verify the IP and port are correct in your ClassicUO profile
- Make sure you're using port `2593`
- Check with Akasha that the server is running

### Login fails
- Double-check your username/password — they're case sensitive
- Try a different username if account creation fails

### Game crashes on launch
- Verify your UO data path points to the correct folder
- Make sure ClassicUO version matches the server version (`7.0.15.1`)

---

*Contact Akasha on Telegram if anything isn't working.*
