# Trac to Markdown Redmine Converter

This is a hacked-together converter that will convert a Redmine DB from using Trac formatting based on [my Redmine Trac formatter plugin](https://github.com/jthomerson/redmine_trac_formatter_plugin/) to the newer Redmine built-in Markdown formatting.

## Usage

 1. Edit `migrate.yml` and insert the correct parameters.
   a. NOTE: the `author_id` field is used when recording change events on issue descriptions and wiki pages.
 2. Run `python migrate.py`

## Complaints

Don't complain. Just use it. This is a "write once, run once" utility that I won't be maintaining. If you find a bug, fix it. Feel free to submit pull requests. I will merge them.
