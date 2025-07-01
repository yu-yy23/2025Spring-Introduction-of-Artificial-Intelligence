import os

os.makedirs('model', exist_ok=True)
os.system('python3 src/coding_transform.py')

os.system('python3 src/binary_pipeline.py')
# os.system('python3 src/multi_pipeline.py')
