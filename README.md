# AI Photo Prompts

A searchable, editable library of 81 AI photo-editing prompts. Everything is in a single `index.html` file.

**Live:** https://mrvishalpatil16-tech.github.io/ai-photo-prompts/

- Search, filter by album and by style category
- One-click copy on every prompt
- Two auto-scrolling rows of prompt titles (pause on hover, click to jump)
- Owner-only add/edit: unlock with the lock button and your password; changes are committed to `prompts.json` and go live for everyone
- Visitors can browse, search and copy only
- Light/dark mode, works on phones

Shortcuts: `/` search · `N` new prompt (owner)

## Owner password

`owner.json` holds a GitHub token (repo-scoped, Contents: read & write) encrypted with the owner password (PBKDF2-SHA256, 600k iterations → AES-256-GCM). The password never leaves the browser.

- First time / token expired: open the site with `?setup` at the end of the address, paste the token, choose a password.
- Change password: owner mode → Backup → Change password.
