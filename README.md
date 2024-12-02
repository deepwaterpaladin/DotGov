# DotGov Project

## Explanation

- Project dedicated to tracking the changes in .gov websites between the 46th & 47th American Presidential administrations.

## Reporting Structure

- Videos are taken on each subpage of the base `.gov` url for a given site
- A full markdown report is saved for each site, found in the `reports/` directory

## Contributing

1. Install dependencies `pip install -r requirements.txt`
1. Install playwright browser(s) `playwright install`

## TODO:

1. Properly track subpages for HHS and SEC, & CIA websites
1. ~~Enable page recording in pipeline~~
1. ~~Implement site-specific change log~~
