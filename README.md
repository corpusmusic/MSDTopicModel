# Million Song Dataset(MSD) Topic Modelling
##Requirements
To run this program, there are some necessities you will need on your computer. The programs also assume some information on the location of certain files. However, this can be changed via establised program arguments or editing the code itself. 
Requirements:
- Numpy  
- MSD hdf5_getters.py file (It is provided in the PythonSrc directory)
- The subset directory containing the .h5 files we are looking at (It is assumed that it is found in '../db_data/')

## Process Description
This repo provides tools to create a tsv file containing TID, artist, song title, given genre (from tagtraum dataset), along with an ordered list of the most fitting topic numbers. The topic modelling data was created using mallet. Below, there is a description of how we created this data, including how many topics were used in total.

## Running Mallet Topic Modeling
The code below is the process used to create the topic model information used. The first line adds mallet to the terminal's path. The directory given needs to be edited to where you have mallet saved.
```
# The export line should be adjusted as such:
export PATH=/Path/To/Mallet/bin:$PATH'

# After this is done, the following code is used to perform the topic model, and create files with the information
# This line creates the mallet file to use. Again, make sure the path to the lyrics folder is the same
mallet import-dir --input ../db_data/lyrics/ --output all_lyrics.mallet   --keep-sequence --remove-stopwords

# This line runs the topic model and creates output files
mallet train-topics  --input all_lyrics.mallet --num-topics 25 --optimize-interval 20 --output-state topic-state.gz \
	--output-topic-keys lyric_topic_info.txt --output-doc-topics song_topic_data.txt 

# Now that the topic modelling has bee been completed, the data created should be cleaned with the follow line
# Please note that the number following --num-topics should be the same as the one used in the mallet line above
python getTrackInfo.py --num-topics 25 --save-unordered True
```
