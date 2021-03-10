# IndexableNewsboat
Makes the db of [newsboat](https://newsboat.org/) (a great rss reader) indexable by desktop search engine like [recoll](https://www.lesbonscomptes.com/recoll/) or [docfetcher](https://sourceforge.net/p/docfetcher/wiki/).


## Please read:
* **Why did I make this?** I wanted to make my newsboat rss entries searchable though [Recoll](https://www.lesbonscomptes.com/recoll/) 
* **What do you think of issues and contributions?** They are more than welcome, even just for typos, don't hesitate to open an issue.
* **Will this change my database?** No, it makes a copy before hand and doesn't change a thing.
* **What version of python should I use?** It has been tested on Python 3.9
* **I'd like to index my anki database into recoll, is it possible?** I created just that [over there](https://github.com/thiswillbeyourgithub/IndexableAnki)
* **How does it work?** It finds your databse, copies it inside /tmp (otherwise it might be locked), loads it into pandas, drops useless columns, saves each entry as a .txt file, zips all the txt files together, moves the zip in the desired folder, deletes the txt files and the temporary db.
* **Is it cross platform?** Currently no, only linux, and OSX could maybe work quite easily. It's on the todo list but don't be afraid to ask if you think you need this.


## Usage:
    ` python3 ./IndexableNewsboat.py -a ~/snap/newsboat/current/.newsboat/ -o ~/Documents/`
```
usage: IndexableNewsboat.py [-h] [-n NEWSBOAT_PATH] [-o OUTPUT_PATH]

optional arguments:
-h, --help            show this help message and exit
-n NEWSBOAT_PATH, --newsboat_path NEWSBOAT_PATH
                    The path to the newsboat folder(ex: /home/USER/snap/newsboat/current/.newsboat)
-o OUTPUT_PATH, --output_dir OUTPUT_PATH
                    The path to the output folder
```

## How do entries look like afterwards?
Here's an example entry :

```
NEWSBOAT RSS EXPORT AS TXT
id:  [XXXXXXXXXXXXX]
guid: [XXXXXXXXXXXXX]

url: [XXXXXXXXXXXXX]
title:  [XXXXXXXXXXXXX]
author: [XXXXXXXXXXXXX]
feedurl:  [XXXXXXXXXXXXX]
pubDate:  [XXXXXXXXXXXXX]

content:
[XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX]
```
