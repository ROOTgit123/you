# YouTube Video Editor Action

This repository contains a GitHub Action to download, clip, and concatenate segments from a YouTube video.

## How to use

1.  Go to the **Actions** tab in your GitHub repository.
2.  Select the **Edit YouTube Video** workflow.
3.  Click **Run workflow**.
4.  Enter the **YouTube Video URL**.
5.  Enter the **Timeline list** (e.g., `01:10-01:15, 03:20-03:35`).
6.  Click **Run workflow**.
7.  Once finished, the edited video will be available as an artifact named `final_video`.

## Timeline Format

The timeline should be a comma-separated list of time ranges. Each range should be in the format `START-END`, where `START` and `END` can be in `MM:SS` or `HH:MM:SS` format.

Example: `01:10-01:15, 03:20-03:35, 06:45-07:05, 10:15-10:25`
