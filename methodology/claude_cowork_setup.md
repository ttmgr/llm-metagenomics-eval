# Claude Cowork Setup Guide
> Practical setup, workarounds, and skill strategies for heavy non-coding users.  
> Community-sourced — originally shared on Reddit.

---

## Table of Contents
1. [The Shared Folder](#1-the-shared-folder)
2. [Handoff Docs](#2-handoff-docs)
3. [AskUserQuestion Widget Bug](#3-askuserquestion-widget-bug)
4. [Unarchiving Tasks](#4-unarchiving-tasks)
5. [Skills Overview](#5-skills-overview)
6. [Writing Style Skill](#6-writing-style-skill)
7. [Self-Improving Skills](#7-self-improving-skills)
8. [Dual-Layer Skill Activation](#8-dual-layer-skill-activation)
9. [Chrome Browser Integration](#9-chrome-browser-integration)

---

## 1. The Shared Folder

**Always select your shared folder at the very start of a task.**  
There is currently no way to add a folder after a session has begun.

### Tips
- Use a single dedicated Cowork folder across all tasks.
- Start with an empty folder — it will organically grow into a structured knowledge base with subfolders.
- If you forget to select the folder and the task has already progressed, ask Claude to generate a **handoff doc**, then start a new task with the folder selected from the beginning.

---

## 2. Handoff Docs

Handoff docs let you move work seamlessly between sessions, chats, and devices.

### When to use them
- You forgot to attach the shared folder at session start.
- You planned something on the Claude mobile app and want to continue in a Cowork task.
- You want to start a fresh session without losing progress.

### How to create one
Ask Claude:
Take the doc to a new Cowork task and attach your shared folder at the start.

---

## 3. AskUserQuestion Widget Bug

**Symptom:** Cowork appears frozen on "sending message" with no way to interact.

**Cause:** An intermittent bug with the structured question widget causes it to fail silently.

### Quick fix
1. Manually stop the generation.
2. The blocked messages will reappear.
3. Ask Claude to pick up where it left off — normally nothing important is lost.

### Permanent workaround (via custom skill)
Build a skill with the following rule:
- Try the AskUserQuestion widget **once per session**.
- If it fails, fall back to **plain text questions** for the rest of the session.

> **Self-healing behaviour:** Every new session tests the widget. Once the bug is fixed upstream, the skill automatically stops falling back without any manual changes needed.

---

## 4. Unarchiving Tasks

Cowork currently has **no built-in UI** for viewing or restoring archived tasks.  
Once archived, a task disappears from the interface.

### Workaround
Build a small skill that generates a terminal command to:
1. Search the session JSON files on disk.
2. Flip the `archived` flag back to `false`.

The manual solution was originally documented in [this Reddit thread](https://www.reddit.com/r/ClaudeAI/comments/1qqaung/where_are_archived_cowork_chats/).

---

## 5. Skills Overview

Skills are reusable instructions, workflows, and knowledge blocks that Claude loads into any session.

### What you can use skills for
- Encoding your personal processes and workflows
- Fixing missing UI features (like the unarchive workaround)
- Compensating for intermittent bugs (like the widget fallback)
- Applying consistent style, tone, or output format across all tasks

> Skills are most powerful when combined with a `CLAUDE.md` file — see [Dual-Layer Skill Activation](#8-dual-layer-skill-activation).

---

## 6. Writing Style Skill

A writing style skill is an easy, high-value first skill to build.

### How to create it
1. Collect several examples of your best pre-AI writing.
2. Ask Claude to analyse the samples and extract your writing style.
3. Ask Claude to turn that analysis into a reusable skill.

### What to expect
- Results will be imperfect at first.
- Expect several weeks of active refinement.
- Combine with the meta-skill (below) to automate improvements over time.

---

## 7. Self-Improving Skills

**Meta-skill:** [github.com/rebelytics/one-skill-to-rule-them-all](https://github.com/rebelytics/one-skill-to-rule-them-all)

This open-source meta-skill runs passively in the background of every session.

### How it works
- Watches how your other skills perform during each session.
- Logs an **observation** whenever you correct Claude's output, explain a process, or make a judgement call not captured in any skill.
- At end of session, ask: *"Any observations logged?"* — Claude summarises what it noticed.
- Over time, observations are applied back to the relevant skills, making them progressively better.

### Self-referential behaviour
The meta-skill also monitors **itself**: if its own observation format is unclear or it misses something it should have caught, it logs that too.

---

## 8. Dual-Layer Skill Activation

**Problem:** Relying on skill trigger descriptions alone is unreliable — Claude is focused on the task, not on remembering to load background skills.

### Solution: Two-layer approach

| Layer | Role |
|---|---|
| `CLAUDE.md` instruction | **Primary** — explicitly tells Claude to load specific skills at the start of every task |
| Skill trigger descriptions | **Backup** — catches cases the CLAUDE.md instruction may miss |

### Setting up CLAUDE.md
If you don't have a `CLAUDE.md` file yet, ask Claude to help you create one. Add a line such as:
`Load the Cowork Setup Skill and Writing Style Skill at the start of every task.`

---

## 9. Chrome Browser Integration

**Problem:** Cowork's built-in web fetch tool is limited and frequently blocked by Cloudflare and other bot protection systems.

**Solution:** Install the **Claude Chrome extension** to give Cowork access to your actual Chrome browser.

### Benefits
- Navigates websites as a real user — bypasses bot detection.
- Runs in the background while you work on other things.
- You can optionally watch it navigate in the Chrome window.
