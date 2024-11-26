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
            # Count markdown links using a simple regex pattern
            # Matches both [text](url) and <url> formats
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
    Create a CSV log comparing markdown files across two date directories.

    Args:
        current_date_path (str): Path to current date's report directory
        previous_date_path (str): Path to previous date's report directory
    """
    output_log_path = os.path.join(current_date_path, 'change_log.csv')
    with open(output_log_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['DEPT', 'PREVIOUS_LINK_SUM',
                            'CURRENT_LINK_SUM', 'CHANGE_SUMMARY'])
        try:
            for current_file in Path(current_date_path).glob('**/*.md'):
                relative_path = os.path.relpath(
                    current_file, current_date_path)
                previous_file = Path(previous_date_path) / relative_path

                if not previous_file.exists():
                    continue

                previous_links = count_markdown_links(str(previous_file))
                current_links = count_markdown_links(str(current_file))

                if previous_links == current_links:
                    change_summary = 'NO CHANGE'
                elif previous_links < current_links:
                    change_summary = f'+{current_links - previous_links} LINKS'
                else:
                    change_summary = f'-{previous_links - current_links} LINKS'

                dept = current_file.stem.upper()

                csv_writer.writerow([
                    dept,
                    previous_links,
                    current_links,
                    change_summary
                ])
        except:
            print(f"Issue with {current_file.stem.upper()}")
