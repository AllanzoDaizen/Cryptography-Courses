import os

target = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'Victim', 'ransomware.py')
)
os.makedirs(os.path.dirname(target), exist_ok=True)

with open(target, 'w') as f:
    f.write('Hello, World!\n')

print(f'Wrote file: {target}')