import os

def find_db_files():
    for root, dirs, files in os.walk('f:/projects/medi-bid'):
        for file in files:
            if file.endswith('.db'):
                print(os.path.join(root, file))

if __name__ == '__main__':
    find_db_files()
