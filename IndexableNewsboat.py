#!/usr/bin/env python
# coding: utf-8

#    Released under the GNU General Public License v3.
#    Copyright (C) - 2021 - user "thiswillbeyourgithub" of "github.com"
#    This file is IndexableNewsboat. It aims to make
#    your newsboat database indexable by desktop search engines.
#
#    IndexableNewsboat is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    IndexableNewsboat is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with IndexableNewsboat.  If not, see https://www.gnu.org/licenses/.

#    for more information or to get the latest version go to :
#    https://github.com/thiswillbeyourgithub/IndexableNewsboat
#    Version : March 2021


# imports ###################################################
import pandas as pd
import sqlite3
import os
import re
import argparse
from tqdm import tqdm


# arguments ###################################################
parser = argparse.ArgumentParser()
parser.add_argument("-n",
                    "--newsboat_path",
                    help="The path to the newsboat folder(ex:\
/home/USER/snap/newsboat/current/.newsboat)",
                    dest="nwb_loc",
                    metavar="NEWSBOAT_PATH")
parser.add_argument("-o",
                    "--output_dir",
                    help="The path to the output folder",
                    dest="output_dir",
                    metavar="OUTPUT_PATH")
args = parser.parse_args().__dict__


# checks ###################################################
if args['nwb_loc'] is None or args['output_dir'] is None:
    print(f"Problem with provided arguments:\n{args}\nExiting.")
    raise SystemExit()
else:
    args['nwb_loc_full'] = f'{args["nwb_loc"]}/cache.db'

if not os.path.exists(args["nwb_loc_full"]):
    print(f"Newsboat db not found.\n{args}\nExiting.")
    raise SystemExit()
else:
    print(f"Found db {args['nwb_loc_full']}...")

os.system(f'cp --remove-destination "{args["nwb_loc_full"]}" /tmp/newsboat_temporary.db')

# main code ###################################################


conn = sqlite3.connect('/tmp/newsboat_temporary.db')
query = "SELECT * FROM rss_item"
db = pd.read_sql_query(query, conn).copy()
conn.close()

db = db.set_index("id")
db.sort_index()


print("Adjusting DataFrame...")
db.drop(columns=['unread', 'enclosure_url', 'enclosure_type', 'enqueued',
        'flags', 'deleted', 'base', 'content_mime_type'], inplace=True)
db.sort_index()


def text_processor(content):
    "to remove useless html"
    content = re.sub('\\n|<div>|</div>|<br>', " ", content)  # removes newline
    content = re.sub("<.*?>", " ", content)  # removes all html markups
    return content


print("Processing text content...")
db["content"] = [text_processor(content) for content in tqdm(db["content"])]


os.system('rm -r "/tmp/IndexableNewsboat"')
os.system('mkdir -p "/tmp/IndexableNewsboat/"')


def save_entry_as_file(entry_id):
    with open(f'/tmp/IndexableNewsboat/Newsboat_{entry_id}.txt',
              'w', encoding="utf-8") as f:
        string = "NEWSBOAT RSS EXPORT AS TXT\n"
        string += f"id: {entry_id}\n"
        string += f"guid: {db.loc[entry_id]['guid']}\n"
        string += f"\nurl: {db.loc[entry_id]['url']}\n"
        string += f"title: {db.loc[entry_id]['title']}\n"
        string += f"author: {db.loc[entry_id]['author']}\n"
        string += f"feedurl: {db.loc[entry_id]['feedurl']}\n"
        string += f"pubDate: {db.loc[entry_id]['pubDate']}\n"
        string += f"\n\ncontent:\n{db.loc[entry_id]['content']}\n"
        f.write(string)


print("Saving entries as txt...")
for i in tqdm(db.index):
    save_entry_as_file(i)

print("Compressing as a zip archive...")
os.system(f"rm -r {args['output_dir']}/IndexableNewsboat.zip")
os.system(f"cd /tmp/IndexableNewsboat && zip -9 {args['output_dir']}/IndexableNewsboat.zip *")

print("Cleaning up...")
os.system("rm -r /tmp/IndexableNewsboat")

print("Done!\nExiting...")
