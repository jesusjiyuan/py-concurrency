import os
from tqdm import tqdm

file_path = r"D:\workspace\spaceai\datasets\test\face1\\"
train_list = [
    file
    for file in os.listdir(file_path)
    if file.startswith('胡歌')
]
train_list = tqdm(train_list)
j = 0

for i in train_list:
    os.rename( file_path + i
               , file_path + '{:0>4s}'.format(str(j)) + '.jpg')
    j += 1

# for i in range(100):
#     s = str(i + 1)
#     s = s.zfill(6)
#     os.rename('C:/Users/dell/Desktop/HR/DIV2K_' + s + '.png', 'C:/Users/dell/Desktop/HR/' + str(i+1) + '.jpg')
