# Manual: Using Claude Cowork + Firefox to Cross-Reference Citations in a DOCX

> **Important note on Firefox:** Anthropic's official Claude browser
> extension is Chrome-only. Firefox is not natively supported due to
> API compatibility differences between the two browsers. This manual
> covers the best available workarounds to achieve the same result
> in Firefox.

---

## Table of Contents
1. [What This Workflow Does](#1-what-this-workflow-does)
2. [Prerequisites](#2-prerequisites)
3. [Option A — Chrome Extension (Recommended)](#3-option-a--chrome-extension-recommended)
4. [Option B — Firefox via ClaudeCodeBrowser](#4-option-b--firefox-via-claudecodebrowser)
5. [Preparing Your DOCX](#5-preparing-your-docx)
6. [The Core Cowork Workflow](#6-the-core-cowork-workflow)
7. [Prompt Templates](#7-prompt-templates)
8. [Interpreting Results](#8-interpreting-results)
9. [Skill for Repeating This Workflow](#9-skill-for-repeating-this-workflow)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. What This Workflow Does

This workflow lets Claude Cowork:
- Read a `.docx` file you provide
- Extract all citations, references, or URLs from it
- Open each source in a real browser (not a limited web fetch)
- Verify whether the source exists, is accessible, and matches
  the claim made in your document
- Return a structured report of what it found

This is especially useful for academic papers, research reports,
literature reviews, or any document with a reference list.

---

## 2. Prerequisites

- A Claude Pro or Max account with Cowork access
- Your `.docx` file saved locally
- A dedicated Cowork shared folder set up (see note below)
- A browser Claude can control — see Options A and B below

> **Shared folder tip:** Always select your shared folder at the
> very start of the Cowork session. There is currently no way to
> add it after the session has begun.

---

## 3. Option A — Chrome Extension (Recommended)

This is the most reliable path. Even if you normally use Firefox,
consider keeping Chrome installed solely for this workflow.

### Setup steps
1. Install the **Claude for Chrome** extension from the
   Chrome Web Store.
2. Sign in with your Anthropic account inside the extension.
3. Open Chrome and keep it running in the background.
4. In your Cowork task, tell Claude:
   ```
   You have access to my Chrome browser via the browser extension.
   Please use it to navigate websites — do not use your built-in
   web fetch tool, as it gets blocked by many sites.
   ```

### Why Chrome works better
Claude's built-in web fetch is frequently blocked by Cloudflare
and other bot protection systems. The Chrome extension lets Claude
navigate as a real user, bypassing these blocks entirely. You can
watch it work in the Chrome window while you do other things.

---

## 4. Option B — Firefox via ClaudeCodeBrowser

If you want to stay in Firefox, use the community-built
**ClaudeCodeBrowser** extension. It connects Claude Code to
Firefox via a native messaging host.

### What it supports
- Screenshot capture (viewport or full page)
- Clicking elements by coordinates or CSS selector
- Typing text into input fields
- Scrolling and navigating pages
- Tab management (list, switch, create, close)

### Setup steps

1. Install the extension from Mozilla Add-ons:
   https://addons.mozilla.org/en-US/firefox/addon/claudecodebrowser/

2. Install the native messaging host from GitHub:
   https://github.com/nanogenomic/ClaudeCodeBrowser

3. Follow the repo instructions to install the Python host:
   ```bash
   # In the /native-host/ directory of the repo:
   pip install -r requirements.txt
   python claudecodebrowser_host.py
   ```

4. Register the native messaging manifest:
   - On macOS/Linux, copy `claudecodebrowser.json` to:
     `~/.mozilla/native-messaging-hosts/`
   - On Windows, register it via the registry key specified
     in the repo README.

5. Restart Firefox and verify the extension shows as connected.

> **Note:** ClaudeCodeBrowser runs via Claude Code CLI, not
> directly via the Cowork UI. You will need Claude Code
> installed (`npm install -g @anthropic-ai/claude-code`)
> and will run this workflow from your terminal rather than
> the Cowork interface. For a fully no-code experience,
> use Option A.

### Read-only alternative (simplest Firefox option)
If you only need Claude to **read** pages (not interact with them),
install **Page Assist** for Firefox:
https://addons.mozilla.org/en-US/firefox/addon/page-assist/

Connect it to Claude via your Anthropic API key. This gives
solid read-only functionality — sufficient for checking whether
a URL resolves and reading its content — but cannot click,
scroll, or fill forms.

---

## 5. Preparing Your DOCX

Before starting the Cowork session, prepare your document:

1. **Save a clean copy** of your `.docx` to your Cowork shared folder.
2. **Check formatting:** Proper heading levels and paragraph styles
   help Claude identify sections accurately.
3. **Isolate the reference list** if possible — copy it into a
   separate plain `.txt` file alongside the `.docx`. This gives
   Claude a clean list of citations to work through without having
   to parse the full document repeatedly.

### What Claude can extract from a DOCX
- Document title and section hierarchy
- Table of contents, captions, and footnotes
- Inline citations (e.g. author-year, numbered)
- Reference list at the end
- Embedded URLs and DOIs

---

## 6. The Core Cowork Workflow

### Step 1 — Start your Cowork task
Open a new Cowork task and **select your shared folder immediately**.

### Step 2 — Upload your DOCX
Upload the `.docx` (and optional `.txt` reference list) into the session.

### Step 3 — Extract all citations
Use this prompt:
```
Please read the attached document and extract every citation,
reference, and URL. Output them as a numbered list with:
- The citation as it appears in the document
- The URL or DOI if present
- The claim or sentence it supports (quoted from the document)
```

### Step 4 — Cross-reference each citation
Once Claude has the list, use this prompt:
```
Now use the browser to verify each citation in the list.
For each one:
1. Open the URL or search for the source title
2. Check whether the page/paper exists and is accessible
3. Check whether the source actually supports the claim made
   in the document
4. Note the date of the source and whether it is still live

Output a table with: Citation | Status | Claim Supported? | Notes
```

### Step 5 — Save the report
```
Please save the verification report as a markdown file called
citation-check-report.md in our shared folder.
```

---

## 7. Prompt Templates

### Extract citations only
```
Read [filename.docx] and list every reference in the bibliography
or reference section. Format as: [Number] | [Authors] | [Title] |
[Year] | [URL or DOI if available]
```

### Verify a single citation
```
Open this URL in the browser: [URL]
Check whether it is accessible. If yes, read the page and tell me
whether it supports this claim from my document:
"[paste the claim here]"
```

### Full batch verification
```
Work through the citation list we extracted. For each citation:
- Try the URL or DOI first
- If no URL, search Google Scholar or the publisher's site
  for the title
- Flag any that are: broken links | paywalled | not found |
  claim mismatch | date issues
Take your time — accuracy matters more than speed here.
```

### Final summary prompt
```
Summarise the citation check. How many citations were verified?
How many had issues? List the problematic ones with a brief
description of each issue. Format as a markdown report.
```

---

## 8. Interpreting Results

| Status | Meaning | Action |
|---|---|---|
| ✅ Verified | Source found, claim supported | No action needed |
| ⚠️ Partial | Source found but claim is not directly supported | Review and revise the claim |
| 🔒 Paywalled | Source exists but content could not be read | Manually verify via institutional access |
| ❌ Broken link | URL returns 404 or does not resolve | Find an archived version (e.g. Wayback Machine) or replace the source |
| ❓ Not found | Source could not be located at all | Remove or replace the citation |
| 📅 Date issue | Source post-dates the claim or is very old | Review relevance |

---

## 9. Skill for Repeating This Workflow

To avoid re-explaining this process every session, ask Claude
to build it into a reusable skill:

```
Based on what we just did, please create a Cowork skill called
"Citation Checker" that encodes this full workflow. It should:
- Know to extract citations from an uploaded DOCX first
- Know to use the browser (not web fetch) for verification
- Know the output format (table + markdown report)
- Know to save the report to the shared folder

Save the skill to our shared folder as citation-checker-skill.md
```

Then add to your `CLAUDE.md`:
```
At the start of every task, load the Citation Checker skill
from the shared folder if the task involves document review
or citation verification.
```

---

## 10. Troubleshooting

**Claude is using web fetch instead of the browser**
→ Explicitly tell it: *"Do not use your web fetch tool. Use the
browser extension only."*

**Pages are loading but Claude can't read the content**
→ Some sites use JavaScript rendering. Ask Claude to take a
screenshot of the page instead and describe what it sees.

**Session appears frozen on "sending message"**
→ This is the AskUserQuestion widget bug. Manually stop generation —
the blocked messages will reappear. Ask Claude to continue.

**ClaudeCodeBrowser native host not connecting**
→ Confirm the `.json` manifest is in the correct directory for
your OS, and that the Python host script is running in a terminal
before you start the session.

**DOCX formatting is causing extraction errors**
→ Export your document to `.txt` or copy-paste the reference list
directly into the chat as plain text. This bypasses all DOCX
parsing issues.
