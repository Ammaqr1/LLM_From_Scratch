import os
import lzma
from tqdm import tqdm

def xz_files_in_subsets(base_directory):
    files = []
    
    # Iterate over each subset folder
    for subset_folder in os.listdir(base_directory):
        subset_folder_path = os.path.join(base_directory, subset_folder)
        
        # Check if it is a directory and matches the pattern
        if os.path.isdir(subset_folder_path) and subset_folder.startswith('urlsf_subset'):
            openwebtext_path = os.path.join(subset_folder_path, 'openwebtext')
            
            # Check if the openwebtext directory exists
            if os.path.isdir(openwebtext_path):
                for filename in os.listdir(openwebtext_path):
                    if filename.endswith('.xz') and os.path.isfile(os.path.join(openwebtext_path, filename)):
                        files.append(os.path.join(openwebtext_path, filename))
                        
    return files

folder_path = r'C:\Users\ammar\Desktop\more_proj\llm_from_scratch\openwebtext\subsets'

output_file_train = 'output_train.txt'
output_file_val = 'output_val.txt'
vocab_file = 'vocab.txt'


files = xz_files_in_subsets(folder_path)
print(files)
total_files = len(files)

split_index = int(total_files * 0.9)
files_train = files[:split_index]
files_val = files[split_index:]

vocab = set()

with open(output_file_train,'w',encoding='utf-8') as outfile:
    for filename in tqdm(files_train,total=len(files_train)):
        file_path = os.path.join(folder_path,filename)
        with lzma.open(file_path,'rt',encoding='utf-8') as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)
            
with open(output_file_val,'w',encoding='utf-8') as outfile:
    for filename in tqdm(files_val,total=len(files_val)):
        file_path = os.path.join(folder_path,filename)
        with lzma.open(file_path,'rt',encoding='utf-8') as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)
            
with open(vocab_file,'w',encoding='utf-8') as vfile:
    for char in vocab:
        vfile.write(char + '\n')

