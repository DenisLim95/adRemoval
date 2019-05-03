from MyImage import MyImage 
import sys
import json
import os
import numpy as np
from scipy.io import wavfile

def recognize_logo(video_path, logo_path, method, output_dir):
    first_encounter = -1
    file = open(video_path, 'rb')
    for i in range(0, 150):
        # 10 is a Buffered time period to create more output
        if (i > first_encounter + 5 and first_encounter != -1):
            return first_encounter * 60
            
        mBytes = None
        for j in range(0, 60): # skip every 60 frame to increase processing time
            mBytes = file.read(480 * 270 * 3)
        img = MyImage()
        img.ReadImage(mBytes)
        try:
            # max = img.TemplateMatch(i)
            if (method == "ATEMPLATE"):
                max, loc = img.ATemplate(i, logo_path, output_dir)
                print(max)
                if (max > 0.85 and first_encounter == -1):
                    first_encounter = i
                    print("Detected Logo at frame " + str(first_encounter))
                    print("Detected Logo at frame " + str(first_encounter))
                    print("Detected Logo at frame " + str(first_encounter))

            elif (method == "ASIFT"):
                found = img.ASiftMatch(i, logo_path, output_dir)
                print (found)
                if (found and first_encounter == -1):
                    first_encounter = i
                    print("Detected Logo at frame " + str(first_encounter))
        except:
            # return first_encounter
            print ("Except encountered")
            pass
    return -1

if __name__ == '__main__':
    video_path = sys.argv[1]
    audio_path = sys.argv[2]

    with open(sys.argv[3], 'r') as f:
        datastore = json.load(f)

    output_video_path = sys.argv[4]
    output_audio_path = sys.argv[5]

    for data in datastore:
        logo_path = data["logo_path"]
        method = data["method"]
        output_dir = data["output_dir"]
        # first_encounter = recognize_logo(video_path, logo_path, method, output_dir)
        # print (first_encounter)
        # data["first_encounter"] = first_encounter
    
    infile = open(video_path, 'rb')
    in_file_size = int(os.path.getsize(video_path) / (480 * 270 * 3)) 

    rate, audio_data1 = wavfile.read(audio_path)

    outfile = open(output_video_path, 'wb')
    idx = 0
    displace = 0
    
    audio_data = np.zeros(len(audio_data1), dtype = np.int16)
    for i in range(0, len(audio_data1)):
        audio_data[i] = audio_data1[i][0]
    print(audio_data)
    for ifile_size in range(0, in_file_size):
        mBytes = infile.read(480 * 270 * 3)
        outfile.write(mBytes)
        idx += 1
        for data in datastore:
            file_size = os.path.getsize(data["ad_video"])
            frame_length = file_size / (480 * 270 * 3)
            ad_video = open(data["ad_video"], 'rb')
            if (idx == data["first_encounter"] + displace):
                rate1, data1 = wavfile.read(data["ad_audio"])
                audio_data = np.insert(audio_data, idx * 1600, data1)
                for i in range(0, int(frame_length)):
                    mBytes = ad_video.read(480 * 270 *3)
                    outfile.write(mBytes)
                    idx += 1
                displace += frame_length
    
    print(len(audio_data))

    wavfile.write(output_audio_path, rate, audio_data)



    

