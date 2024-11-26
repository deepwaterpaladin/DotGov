import csv
import os
from pathlib import Path


def count_markdown_links(file_path: str) -> int:
    """
    Count the number of markdown links in a file.

    Args:
        file_path (str): Path to the markdown file

    Returns:
        int: Number of markdown links found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            import re
            markdown_links = re.findall(r'\[.*?\]\(.*?\)|\<.*?\>', content)
            return len(markdown_links)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return 0


def create_log(current_date_path: str, previous_date_path: str) -> None:
    """
    Create a CSV log comparing markdown files across two date directories,
    sorted by change summary.

    Args:
        current_date_path (str): Path to current date's report directory
        previous_date_path (str): Path to previous date's report directory
    """
    output_log_path = os.path.join(current_date_path, '.change_log.csv')

    log_rows = []

    try:
        for current_file in Path(current_date_path).glob('**/*.md'):
            relative_path = os.path.relpath(
                current_file, current_date_path)
            previous_file = Path(previous_date_path) / relative_path

            if not previous_file.exists():
                continue

            previous_links = count_markdown_links(str(previous_file))-1
            current_links = count_markdown_links(str(current_file))-1

            if previous_links == current_links:
                change_summary = 'NO CHANGE'
                sort_key = float('inf')  # Push NO CHANGE to end
            elif previous_links < current_links:
                change_summary = f'+{current_links - previous_links} LINKS'
                sort_key = current_links - previous_links
            else:
                change_summary = f'-{previous_links - current_links} LINKS'
                sort_key = -(previous_links - current_links)

            dept = current_file.stem.upper()

            log_rows.append({
                'dept': dept,
                'previous_links': previous_links,
                'current_links': current_links,
                'change_summary': change_summary,
                'sort_key': sort_key
            })

        sorted_rows = sorted(
            log_rows,
            key=lambda x: (
                abs(x['sort_key']) if x['change_summary'] != 'NO CHANGE' else float(
                    'inf'),
                2 if x['change_summary'].startswith('-') else 1,
                x['sort_key']
            )
        )

        with open(output_log_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(
                ['DEPT', 'PREVIOUS_LINK_SUM', 'CURRENT_LINK_SUM', 'CHANGE_SUMMARY'])

            for row in sorted_rows:
                csv_writer.writerow([
                    row['dept'],
                    row['previous_links'],
                    row['current_links'],
                    row['change_summary']
                ])

    except Exception as e:
        print(f"Issue processing log: {e}")
        import traceback
        traceback.print_exc()
