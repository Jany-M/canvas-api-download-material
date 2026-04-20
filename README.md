# Canvas Material Downloader

This repository is a Python foundation for pulling course material out of Canvas and storing it in one local place for students.

The initial scaffold focuses on a clean CLI, environment-based configuration, Canvas API pagination, and downloading course files with per-course manifests. It also stores module metadata so the project can grow into pages, assignments, announcements, and richer exports later.

## What it does today

- Lists the Canvas courses available to the authenticated user
- Syncs one course or all visible courses
- Downloads course files into a local `downloads/` directory
- Stores `course.json`, `files.json`, and `modules.json` metadata per course
- Skips re-downloading unchanged files when size and `updated_at` still match

## Project layout

```text
.
├── src/canvas_material_downloader/
├── tests/
├── .env.example
├── pyproject.toml
└── README.md
```

Downloaded content is written like this:

```text
downloads/
└── 12345 - CS101 - Intro to Biology/
    ├── course.json
    ├── files.json
    ├── modules.json
    └── files/
        ├── 99881 - Syllabus.pdf
        └── 99882 - Week 01 Slides.pdf
```

## Setup

1. Create a virtual environment if you want one:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Copy `.env.example` to `.env` and fill in your Canvas values:

   ```env
   CANVAS_BASE_URL=https://your-school.instructure.com
   CANVAS_ACCESS_TOKEN=your-access-token
   CANVAS_OUTPUT_DIR=downloads
   ```

3. Install the package in editable mode:

   ```powershell
   python -m pip install -e .
   ```

## Usage

List available courses:

```powershell
python -m canvas_material_downloader list-courses
```

Sync one course:

```powershell
python -m canvas_material_downloader sync-course 12345
```

Sync every available course:

```powershell
python -m canvas_material_downloader sync-all
```

Include concluded courses too:

```powershell
python -m canvas_material_downloader sync-all --include-concluded
```

Skip files or modules when you only want part of the sync:

```powershell
python -m canvas_material_downloader sync-course 12345 --skip-files
python -m canvas_material_downloader sync-course 12345 --skip-modules
```

## Canvas token note

Most Canvas instances let users create an access token from their account settings page. Once you have that token, place it in `.env` as `CANVAS_ACCESS_TOKEN`.

## Good next steps

- Download pages, assignments, and announcements in addition to files
- Preserve Canvas folder structure instead of a flat per-course `files/` directory
- Export module content as Markdown for easier offline browsing
- Add selective filters such as term, course code, or include/exclude lists
- Add integration tests against a mocked Canvas API

