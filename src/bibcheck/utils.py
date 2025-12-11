import json
import re
import unicodedata
import string
import os
import html
from pathlib import Path

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load exclusions file {path}: {e}")
        return {}

def load_source_patterns(extra_files=None):
    package_dir = Path(__file__).resolve().parent
    default_path = package_dir / "exclusions.json"

    exclusions = load_json(default_path)

    # User-provided extra files (list of paths)
    for path in extra_files or []:
        user_excl = load_json(path)
        exclusions.update(user_excl)

    return exclusions

exclusions = load_source_patterns()


def remove_special_chars(s):
    s = html.unescape(s) 
    s = re.sub(r'<mml:[^>]+>', '', s)
    s = re.sub(r'</mml:[^>]+>', '', s)
    s = re.sub(r'<[^>]+>', '', s)    
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r'[\u2010-\u2015\u2212]', '-', s)    
    s = re.sub(r'\b([A-Z][a-z]+)\s+([a-z])\b', r'\1\2', s)
    
    return s

def format_for_url(text):
    text = text.lower()
    text = text.replace('\n', '').replace(' ', '')
    return text


def normalize_authors(author_block):
    cleaned = remove_special_chars(author_block).replace('  ', ' ')
    cleaned = re.sub(r'\b([A-Z][a-z]+)\s+([a-z])\b', r'\1\2', cleaned)
    return cleaned

def normalize_title(title):
    title = remove_special_chars(title)
    title = re.sub(r'\s+', ' ', title)
    title = title.replace('- ', ' ')
    title = re.sub(r'(?<![0-9A-Za-z])([B-HJ-Z])\s+([a-z])', r'\1\2', title)
    return title.lower().strip(" .,") 

def normalize_concat_title(title):
    title = remove_special_chars(title)
    title = re.sub(r'\s+', ' ', title)    
    title = title.replace('- ', '')
    title = re.sub(r'(?<![0-9A-Za-z])([B-HJ-Z])\s+([a-z])', r'\1\2', title)
    return title.lower().strip(" .,") 


def normalize_hyphen_title(title):
    title = remove_special_chars(title)
    title = re.sub(r'\s+', ' ', title)    
    title = title.replace('- ', '-')
    title = re.sub(r'(?<![0-9A-Za-z])([B-HJ-Z])\s+([a-z])', r'\1\2', title)
    return title.lower().strip(" .,") 



