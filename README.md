# WP:SK

Some cleanup scripts for plwiki articles etc.

Don't run scripts unless you have time fix things later.

## Requirements

Scripts use globally installed Pywikibot (PWB). You must install and configure it. 

  - You should have a bot user.
  - Install Python (tested with Python 3.10).
  - Install PWB with `mwparserfromhell`.
  - Prepare auth in `user-config.py` and `user-password.py`.
  
See: [Pywikibot installation](https://doc.wikimedia.org/pywikibot/stable/installation.html).

Check if pwb is working and get some info:
```
pwb -help
```
## Modules

```
git submodule add "https://github.com/Eccenux/wikibot-utils.git" "utils"
```

## Executing changes

1. You need a list of pages first.
2. Use the list to make a dry run via one of `execute--*.py`.
3. Make a non-dry run to make changes in articles.

Note that you might need to prepare new `execute--*.py` or modify the custom one with a simple, one-time change.
