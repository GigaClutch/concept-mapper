# Putting Your Concept Map Online (No Coding Required)

This guide takes your map from your laptop to a real public web link, using a free service called
**GitHub Pages**. You don't need to understand any of the code — just follow the steps in order.

You'll do two kinds of things:
- **Click around a website** (github.com) — easy, like any other site.
- **Copy-paste a few commands** into **PowerShell** — the exact text is below. Copy, paste, Enter.

Total time: about **10–15 minutes**, most of it waiting.

---

## First, two reassurances

**1. Your secret API key will NOT be uploaded.** The key lives in a file called `.env`, which the
project deliberately skips when uploading (it's listed in `.gitignore`). Your key stays private on
your computer. This has been double-checked.

**2. The live "research" feature is intentionally off in the public version.** That feature needs a
small program running on your own computer, which a public website can't do. Online, your map shows
all its concepts, connections, importance, filters, path-finding, and sourced quotes — it just won't
have the live research button. This is on purpose. Nothing is broken.

---

## Step 1 — Create a free GitHub account (skip if you have one)

1. Go to **https://github.com**.
2. Click **Sign up** (top-right).
3. Enter your email (you can use **gigaclutch@gmail.com**), pick a password, and choose a **username**.
   - **Write your username down** — you'll need it. (e.g. if you pick `gigaclutch`, that's your username.)
4. Verify your email. Done.

> Wherever you see **`<username>`** below, replace it with your username — no angle brackets.

---

## Step 2 — Create a new empty repository

1. Signed in at **https://github.com**, click the **+** (top-right) → **New repository**.
2. Fill in:
   - **Repository name:** `concept-mapper`
   - **Public / Private:** choose **Public**.
   - **VERY IMPORTANT — do NOT check any "Initialize this repository" boxes.** Leave **"Add a README"
     unchecked**, and leave **.gitignore** and **license** set to **None**. Your computer already has
     these; checking the box causes a conflict.
3. Click the green **Create repository**.

Leave that page open.

---

## Step 3 — Connect your computer and upload

1. Open **PowerShell** (Start menu → type `PowerShell` → Windows PowerShell).
2. Go into your project folder:

   ```powershell
   cd "C:/Dev/Concept Mapper Fable"
   ```

3. Link to your GitHub repo — **replace `<username>` first**, then Enter:

   ```powershell
   git remote add origin https://github.com/<username>/concept-mapper.git
   ```

   (Nothing visible happens — that's normal.)

4. Upload everything:

   ```powershell
   git push -u origin master
   ```

5. **A sign-in window may pop up.** The first time, GitHub opens your browser asking you to sign in /
   authorize. Click **Sign in with your browser**, log in, approve. You only do this once.

When it finishes you'll see text ending like `master -> master`. Refresh the GitHub page — your files
are there.

> **If you see "remote origin already exists"**, run this one line, then redo step 4:
> ```powershell
> git remote set-url origin https://github.com/<username>/concept-mapper.git
> ```

---

## Step 4 — Turn on GitHub Pages

All clicking, no commands.

1. On your repo page (`https://github.com/<username>/concept-mapper`), click **Settings** (gear, top-right).
2. Left menu → **Pages**.
3. Under **Build and deployment**, open the **Source** dropdown.
4. Choose **GitHub Actions**.

There's no save button — selecting it is enough. The automated recipe already in your project
(`.github/workflows/pages.yml`) takes over and publishes your map.

---

## Step 5 — Wait for the green check

1. Click the **Actions** tab on your repo.
2. A job runs with a **yellow spinning dot** (~1–2 minutes).
3. Refresh until it's a **green check** ✅ — your site is live.

> A **red X** just means a hiccup — click in, then **Re-run jobs**. Usually green on the first try.

---

## Step 6 — Find your public link

1. Back to **Settings → Pages**.
2. At the top: **"Your site is live at"** with your link and a **Visit site** button.

Your link looks like:

```
https://<username>.github.io/concept-mapper/
```

e.g. `https://gigaclutch.github.io/concept-mapper/`. Share it with anyone — it works on phones,
tablets, and computers.

---

## Good to know

- **The link is permanent** — bookmark and share freely.
- **To update the map later**, in PowerShell:
  ```powershell
  cd "C:/Dev/Concept Mapper Fable"
  git add -A
  git commit -m "Update the map"
  git push
  ```
  Your live site refreshes a minute or two later. No need to touch Settings again.
- **Your API key stays safe** every time — `.env` is permanently skipped.
