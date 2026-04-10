# Akudemy Scripts

## exam_paper_scraper.py

Generates `data/exam_papers/` — 1,350 structured WAEC/NECO/JAMB questions.

> **Status**: Full migration pending. The stub file is a placeholder.
> Run `./docs/service-migrations/migrate-exam-papers.sh` from a local machine
> with `data/exam_papers/` and `mlops/exam_paper_scraper.py` present to complete
> the migration.

### Usage (once migrated)

```bash
pip install -r requirements.txt
python scripts/exam_paper_scraper.py --output data/exam_papers/
```

### Output

| File | Description |
|------|-------------|
| `data/exam_papers/INDEX.json` | Dataset manifest — 1,350 questions, 4 subjects, 27 topics |
| `data/exam_papers/<subject>/` | Per-subject JSON question files |
| `data/exam_papers/<subject>.csv` | Per-subject CSV question files |

### Data Sources

Scrapes and structures publicly available past questions from WAEC, NECO, and JAMB (2020–2024).
Covers: Mathematics, English Language, Physics, Chemistry.

See `EXAM_SCRAPER_DELIVERABLES.md` for full specification (added during full migration).
