#-*- coding: utf-8 -*- 
########################################################################
#create_tsvs.py

#Author   : Carlos Daniel Hernández Mena
#Date     : May 30th, 2023
#Location : Reykjavík University

#Usage:

#	$ python3 create_tsvs.py

#Description:

#This script creates the TSV files of the Example_Corpus and
#put them in the HF_DATA_REPO.

#Notice: This program is intended for Python 3
########################################################################
#Imports

import sys
import re
import os

########################################################################
#Important variables

os.chdir("../")

CORPUS_PATH="Load_Custom_Data_in_HF/Example_Corpus"

TRAIN_TRANS = os.path.join(CORPUS_PATH,"transcriptions","train.trans")
TEST_TRANS  = os.path.join(CORPUS_PATH,"transcriptions","test.trans")
DEV_TRANS   = os.path.join(CORPUS_PATH,"transcriptions","dev.trans")

TRAIN_PORTION_DIR = os.path.join(CORPUS_PATH,"speech","train")
TEST_PORTION_DIR  = os.path.join(CORPUS_PATH,"speech","test")
DEV_PORTION_DIR   = os.path.join(CORPUS_PATH,"speech","dev")

REPO_DATA_DIR=os.path.join("Load_Custom_Data_in_HF/HF_DATA_REPO","data")

CACHE_DIR=os.path.join("Load_Custom_Data_in_HF/HF_DATA_REPO","CACHE")

########################################################################
#Create important directories
if not os.path.exists(REPO_DATA_DIR):
	os.mkdir(REPO_DATA_DIR)
#ENDIF

if not os.path.exists(CACHE_DIR):
	os.mkdir(CACHE_DIR)
#ENDIF

########################################################################
#Global Functions
def load_trans(trans_path):
	HASH_TRANS={}
	file_in=open(trans_path,'r')
	for line in file_in:
		line=line.replace('\n','')
		line=re.sub('\s+',' ',line)
		line=line.strip()
		list_line=line.split(' ')
		file_id=list_line[0]
		list_line.pop(0)
		trans=' '.join(list_line)
		HASH_TRANS[file_id]=trans
	#ENDFOR
	file_in.close()
	return HASH_TRANS
#ENDDEF
#----------------------------------------------------------------------#
def find_audios(PORTION_DIR):
	HASH_PATHS={}
	valid_formats=['wav','flac','mp3']
	for root, dirs, files in os.walk(PORTION_DIR):
		for filename in files:
			path_to_file=os.path.join(root,filename)
			lista_path=path_to_file.split('.')
			extension=lista_path[-1]
			extension=extension.lower()
			if extension in valid_formats:
				lista_path.pop(-1)
				audio_path='.'.join(lista_path)
				file_id=os.path.basename(audio_path)
				HASH_PATHS[file_id]=path_to_file
			#ENDIF
		#ENDFOR
	#ENDFOR
	return HASH_PATHS
#ENDDEF
#----------------------------------------------------------------------#
def create_tsv(PORTION,HASH_TRANS,HASH_PATHS):
	HEADER="audio_id\tnormalized_text\tabsolute_path\n"
	file_name=PORTION+".tsv"
	file_out_path=os.path.join(REPO_DATA_DIR,file_name)
	file_out=open(file_out_path,'w')
	file_out.write(HEADER)
	for file_id in HASH_PATHS:
		audio_id=file_id
		absolute_path=HASH_PATHS[file_id]
		if file_id in HASH_TRANS:
			normalized_text=HASH_TRANS[file_id]
		else:	
			normalized_text="empty"
		#ENDIF
		line_out=audio_id+'\t'+normalized_text+'\t'+absolute_path+'\n'
		file_out.write(line_out)
	#ENDFOR
	file_out.close()
#ENDDEF

########################################################################
#Load the transcriptions in memory

HASH_TRAIN_TRANS = load_trans(TRAIN_TRANS)
HASH_TEST_TRANS  = load_trans(TEST_TRANS)
HASH_DEV_TRANS   = load_trans(DEV_TRANS)

#Load the absolute paths of the audios in memory

HASH_TRAIN_PATHS = find_audios(TRAIN_PORTION_DIR)
HASH_TEST_PATHS  = find_audios(TEST_PORTION_DIR)
HASH_DEV_PATHS   = find_audios(DEV_PORTION_DIR)

#Create the TSVs

create_tsv("train",HASH_TRAIN_TRANS,HASH_TRAIN_PATHS)
create_tsv("test",HASH_TEST_TRANS,HASH_TEST_PATHS)
create_tsv("dev",HASH_DEV_TRANS,HASH_DEV_PATHS)

########################################################################

