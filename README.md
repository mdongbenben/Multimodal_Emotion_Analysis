#### Download Links

Please download both the datasets _before_ cloning this repository <br/>

Processed Dataset - http://sorena.multicomp.cs.cmu.edu/downloads/MOSEI/ <br/>
Raw Dataset - http://sorena.multicomp.cs.cmu.edu/downloads_raw/MOSEI <br/>


#### Structure of Pickle Files

##### 1. Emotions.pkl 

Let *emo_intsts* be  = array([Anger_Intensity, Disgust_Intensity, Fear_Intensity, Happy_Intensity ,Sad_Intensity,   Surprise_Intensity] <br/>
{"Video Name": {"Segment ID i_1 ": emo_intsts,"Segment ID i_2 ": emo_intsts, .... ,"Segment ID i_n ": emo_intsts}} <br/>

##### Train Set Emotion Intensity Stats: <br/>
 
        0-1 = 94964
        1-2 = 3275 
        2-3 = 515 
        Max Intensity  = 3.0
        Min Intensity  = 0.0 
        Mean Intensity = 0.17
        Mean Non-Zero Intensity = 0.74
##### Validation Set Emotion Intensity Stats: <br/>
        
        0-1 = 11031 
        1-2 = 278 
        2-3 = 37 
        Max Intensity  = 3.0
        Min Intensity  = 0.0
        Mean Intensity = 0.15
        Mean Non-Zero Intensity = 0.68

##### 2. Words.pkl 

##### 3. Embeddings.pkl 

##### 4. Train/Test/Valid.pkl 

Contains a set of all the train/test/validation video names <br/>

Length of Dataset - 3228 Videos divided into 22677 Video Clips of ~3-8 seconds <br/>
Length of Training Set - 2250 Videos divided into 16127 Video Clips <br/>
Length of Validation Set - 300 Videos divided into 1835 Video Clips <br/>
Length of Test Set - 678 Videos divided into 4625 Video Clips <br/>
Length of Truncated Set: <br/>
('train', 11112) <br/>
('test', 3303) <br/>
('val', 1341) <br/>


##### 5. Facet.pkl 
Let *facet_features* be  = array([feature_1_val,feature_2_val,....,feature_35_val]) <br/>
There are 35 features for each frame <br/>
{ "facet" :{"Video Name": {"Segment ID i_1 ": ((start_time_frame_1,end_time_frame_1,facet_features),...      (start_time_frame_n,end_time_frame_n,facet_features)),"Segment ID i_2 ": ..., .... ,"Segment ID i_n ": ....}}}

##### 6. Sentiments.pkl 

##### 7. Covarep.pkl 

Let *covarep_features* be  = array([feature_1_val,feature_2_val,....,feature_74_val]) <br/>
COVAREP features are taken at a time interval of 0.01sec(10ms) which is the original sampling rate of the COVAREP authors.<br/>
There are 74 features for each 0.01 segment. <br/>
{ "facet" :{"Video Name": {"Segment ID i_1 ": ((start_time_frame_1,end_time_frame_1,covarep_features),...      (start_time_frame_n,end_time_frame_n,covarep_features)),"Segment ID i_2 ": ..., .... ,"Segment ID i_n ": ....}}}


#### TO DOs After Cloning the Repository

1. Put all downloaded pickle files in the same directory. <br/>
2. Run creating_audio_files.py using python2.7 (This might take a while depending on your machine). This will generate a folder with all the audio_files containing covarep features with the corresponding video name. 
