# Fantasy Universe

This repository is a writing workspace for fantasy stories that share one fictional universe. It keeps world canon, story planning, manuscripts, continuity notes, and writing guidance together so new work can build on what is already established.

The guiding principle is to **preserve consistency without restricting creativity**. Treat established facts carefully, label uncertain material, and keep story-specific plans distinct from universe-wide canon.

## Start here

- [Agent instructions](AGENTS.md) explain how to work with this repository, select relevant references, and handle canon and continuity.
- [World foundation](world/setting-foundation.md) is the current shared setting reference. Check its status labels and source trail when using its details.
- [Prompts](prompts/) provide task-specific guidance for drafting, editing, worldbuilding, and creating a Story Bible.
- [Stories](stories/) contains each writing project's planning files, manuscript, continuity records, and related materials.

## Repository layout

```text
.
├── AGENTS.md
├── prompts/
│   ├── editor.md
│   ├── story-bible-creator.md
│   ├── worldbuilder.md
│   └── writer.md
├── world/
│   └── setting-foundation.md
└── stories/
    └── The Road Beyond Hazelwood/
        ├── 01_SOURCE_ANALYSIS.md
        ├── 02_REIMAGINING_PLAN.md
        ├── 03_STORY_BIBLE.md
        ├── 04_CHAPTER_BLUEPRINT.md
        ├── 05_SOURCE_MAPPING.md
        ├── 06_CONTINUITY_AND_DECISIONS.md
        ├── manuscript/
        ├── progress/
        └── tmp/
```

### `world/`

Shared, universe-level references belong here. Prefer one authoritative home for each piece of lore, and link back to the story or source material that established it. The current foundation centers on Hazelwood, the Big River, and Malcore; it also records where wider geography and history remain undecided.

### `stories/`

Each story has its own planning and continuity documents. The current project, [*The Road Beyond Hazelwood*](stories/The%20Road%20Beyond%20Hazelwood/), includes source analysis, a reimagining plan, Story Bible, chapter blueprint, source mapping, continuity decisions, a 28-chapter Markdown draft, and progress notes. Start with the [Story Bible](stories/The%20Road%20Beyond%20Hazelwood/03_STORY_BIBLE.md), [manuscript](stories/The%20Road%20Beyond%20Hazelwood/manuscript/), [living continuity](stories/The%20Road%20Beyond%20Hazelwood/progress/LIVING_CONTINUITY.md), or [writing progress](stories/The%20Road%20Beyond%20Hazelwood/progress/WRITING_PROGRESS.md), depending on the task. The progress and continuity files describe the manuscript's current state; consult them rather than assuming a draft or plan is final.

The project folder also contains source and export files, including PDF, DOCX, ODT, and EPUB formats. The `tmp/` directory holds working files and formatting or rendering artifacts; the Markdown planning and manuscript files are the navigable sources for ongoing writing work.

### `prompts/`

Use the prompt that matches the task: `writer.md` for drafting, `editor.md` for editing, `story-bible-creator.md` for Story Bible work, and `worldbuilder.md` for lore development. `worldbuilder.md` is currently empty; use `AGENTS.md` and the relevant world files for worldbuilding guidance until it is filled in.

## Working with canon

The instructions in [AGENTS.md](AGENTS.md) define the full authority hierarchy and working rules. In brief:

- Distinguish established **CANON** from **PLANNED**, **OPEN**, **DISPUTED**, and **DEPRECATED** material.
- Keep objective facts separate from what a character or society believes.
- Treat drafts and proposals as provisional unless the author has approved them or finalized prose establishes them.
- Check magic, chronology, character knowledge, and other cross-story dependencies before adding significant details.
- When a finished story establishes a fact that matters beyond that story, update the appropriate world reference and retain the source trail.

For a new task, read only the relevant prompt, story documents, and world references. Make targeted edits in the most appropriate existing file, preserve links and formatting, and note unresolved conflicts instead of silently deciding them.

## Tooling

This is a text-first writing repository; there is no repository-wide software build or test command. The story project includes helper scripts for manuscript formatting and export under its `tmp/` directory.
