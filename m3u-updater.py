#!/usr/bin/env python
import os

def get_bigrams(string):
    s = string.lower()
    return [s[i:i+2] for i in xrange(len(s) - 1)]

# From http://www.catalysoft.com/articles/StrikeAMatch.html
def strike_a_match(str1, str2):
    pairs1 = get_bigrams(str1)
    pairs2 = get_bigrams(str2)
    union  = len(pairs1) + len(pairs2)
    hit_count = 0
    for x in pairs1:
        for y in pairs2:
            if x == y:
                hit_count += 1
                break
    return (2.0 * hit_count) / union

def is_music_file(filename):
    spliced = filename[-4:]
    if spliced == "flac": return True
    spliced = spliced[1:]
    if spliced == "mp3" or spliced == "wav" or spliced == "aac" or spliced == "ogg" or spliced == "ogg" or spliced == "m4a" or spliced == "m4p":
        return True
    return False

rootdir = raw_input("Enter root directory for music\n")
pfile_dir = raw_input("Enter a playlist file name\n")
pfile = open(pfile_dir)
best_cmps = []
file_locs = []

for line in pfile:
    if line[0] != "#":
        best_cmps.append(0)
        file_locs.append(line)

print "Finding local matching files (this might take a while)"
if rootdir != "":
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            path = os.path.join(subdir, file)
            songNo = 0
            pfile.seek(0)
            for line in pfile:
                if line[0] == "#":
                    continue
                res = strike_a_match(str(path), line)
                if res > 0.5 and res > best_cmps[songNo] and is_music_file(path):
                    best_cmps[songNo] = res
                    file_locs[songNo] = path
                songNo += 1

mfiles_indexes = []
for i in range(len(best_cmps)):
    if best_cmps[i] == 0:
        mfiles_indexes.append(i)
    
print "Writing new playlist file"

songNo = 0
out = ""
pfile.seek(0)
for line in pfile:
    if line[0] == "#":
        if songNo in mfiles_indexes:
            try:
                print "Skipping \"" + line.split(",")[1][:-1] + "\" because local file could not be found"
            except IndexError:
                pass
        else:
            out += line
    else:
        if not songNo in mfiles_indexes:
            out += file_locs[songNo] + "\n"
        songNo += 1

nfile = open(pfile_dir[:-4] + "_new.m3u", "w")
nfile.write(out)
nfile.close()

print "Done"
