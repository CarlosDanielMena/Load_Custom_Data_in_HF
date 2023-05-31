# Load_Custom_Data_in_HF

Load your own audio data into a Hugging Face Dataset object

# Description

The scripts in this repositopry are destined to help users to load their own speech data into a dataset object from the Hugging Face Module called "datasets".

The datasets objects are used in the tasks of training acoustic models or transcribe speech data. In this README file it will be explain how to use this repository for both tasks.

# Execute

The first step you should do is to clone the repo and execute it:

	$ git clone https://github.com/CarlosDanielMena/Load_Custom_Data_in_HF
	$ cd Load_Custom_Data_in_HF
	$ python3 create_tsvs.py

After executing these simple steps, you'll closer to understand how this repo works.

# Inspecting the repo files

When you clone and execute the repository, you will notice that the following directory tree is generated:

Load_Custom_Data_in_HF:

	| - Example_Corpus
		| - speech
			| - dev
				|- FADG0_SX289.wav
				|- MJFC0_SX403.wav
			| - test
				|- FDHC0_SI929.wav
				|- MWBT0_SI2183.wav
			| - train
				|- FSAG0_SI693.wav
				|- MRRE0_SX344.wav
		| - transcriptions
			| - dev.trans
			| - test.trans
			| - train.trans
	| - HF_DATA_REPO
		| - CACHE
		| - data
			| - dev.tsv
			| - test.tsv
			| - train.tsv
		| - loading_script.py
	| - create_tsvs.py
	| - LICENSE
	| - README.md

Notice that the directory "Example_Corpus" shows a typical corpus structure divided in portions such like: train, dev and test.

On the other hand, "HF_DATA_REPO" is a directory with the precise data structure that is needed to be loaded in the dataset object.

# Load Data for Training

Suppose that you to use the dataset object to train an acoustic model in Whisper or WAV2VEC. Imagine that you have some data for training and some data for testing but nothing for the dev portion.

What you have to do is to manually remove the audio files that are in the folders "Example_Corpus/speech/train" and "Example_Corpus/speech/test" and copy your own data there. Obviously, your training portion goes to the folder "Example_Corpus/speech/train" and your test portion goes to the folder "Example_Corpus/speech/test". It doesn't matter if your data comes in subfolders, the scripts in the repository will be able to find any audio file in a format flac, mp3 or wav. Don't worry about the folder "Example_Corpus/speech/dev", just leave it as it is. 

Now you will have to inspect the files "Example_Corpus/transcriptions/train.trans" and "Example_Corpus/transcriptions/test.trans". Notice that they come in this format:

**FSAG0_SI693 he who does not love abides in death**
**MRRE0_SX344 i know i didn't meet her early enough**

In other words, the format is:

**FILE_ID words of the transcription separated by one single space**

It is very important that your corpus has a unique file name for each audio file. Notice that  if your audio file has the following name **FSAG0_SI693.wav**, the corresponding file id will be **FSAG0_SI693**. That file id will go in the corresponding transcription file depending if the audio belogs to the train, test or dev portion of your corpus. Remeber that in this example, you don't have dev data, so just don't touch the file  "Example_Corpus/transcriptions/dev.trans"

What you have to do next is to modify the transcriptions files to add your own transcriptions with the respective file ids. Don't change the names "train.trans", "test.trans" or "dev.trans"; just modify them adding your data and removing the data that was there as a example.

If your audio files are in place and the transcription files are modified correctly, you just have to re-run the repo scripts as explianed in the section **Execute** above.

If everything went well, you will notice that the files "HF_DATA_REPO/data/train.tsv" and "HF_DATA_REPO/data/test.tsv" reflect now information about the data that you added.

At this point, the folder HF_DATA_REPO is ready to be loaded in a dataset object. If you want to see an example of how to do so, please see this [Notebook](https://colab.research.google.com/drive/11Lr4JK6gvbPfeNkAFW8hmrFK4yO2fsPK?usp=sharing)

# Load Data for Transcribing

Suppose that you only have audio files that you want to transcribe. In a similar way as in the section **Load data for Training**, you will have to copy your audio files in the folder "Example_Corpus/speech/test". As you obviously don't have the transcriptions, don't worry, just don't touch the transcription files.

Remeber that your audio files have to have a unique file name and they can be in any of the following formats: wav, flac or mp3.

After copying the files in the right folder, just re-run the repo scripts as explianed in the section **Execute** above.

At this point, the folder HF_DATA_REPO is ready to be loaded in a dataset object. If you want to see an example of how to do so, please see this [Notebook](https://colab.research.google.com/drive/11Lr4JK6gvbPfeNkAFW8hmrFK4yO2fsPK?usp=sharing)
