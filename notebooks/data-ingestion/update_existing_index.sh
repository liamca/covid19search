#!/bin/bash
python 01-Download-latest-publications.py
python 03-Upload-JSON-to-Azure-Search.py  
python 05-Apply-Metadata.py
python 06-Upload-Concepts-to-Azure-Search-v3.py
