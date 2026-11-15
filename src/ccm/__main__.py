"""Allow `python -m src.ccm` for scheduled / cron runs.

Equivalent to `python -m src.ccm.cli run`.
"""
from src.ccm.cli import main

if __name__ == "__main__":
    main()
