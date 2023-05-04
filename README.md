# RenPy Multilang Plugin
This is a plugin that adds "multilanguage" support to RenPy but in a really hacky way. Because the VN I was working on needed to add/remove lines as it was being written and it was also made with multiple langauges in mind.

**If your VN is finished, you should not use this, you do not need this.**

P.S. Looking for a simple VN engine with multilanguage support built in? Check out RepliCant!

## Usage

Add 01_init_custom_func.rpy to your renpy game.

Then add "tl" command before text, like this

No speaker example: `tl None "Hello world!" "Spanish goes here" "Japanese goes here"`

Speaker example: `tl e "Hello world!" "Spanish goes here" "Japanese goes here"`

## Import/Export
Importing/exporting to csv and back is supported, but since I only wrote this for a VN I helped with it's up to you to modify the scripts for your own use.

`import_es_ja_script.py` - Very hastily written script, ES means renpy translation style and JA means tsv. Imports translations into the renpy dialogue script you specify. **Choices in a TSV need to be prefixed with %**

`JA_TO_TEXTMAP.py` - This just reads from a textfile and a renpy script at the same time and tries to combine them into tsv. If you have any foresight and are planning to make your RenPy VN multilanguage you should just use Google Sheets for the dialogue in the first place so this isn't needed.

# License
LGPLV2, this means you ONLY need to publish source code if you modify it and only this modified plugin. Yes, v2, you can tivoize it if you want, you can resell it if you want.

The scripts are also LGPLv2, but you are not required to distribute them after modification as the GPL does not cover using software to generate other software.
