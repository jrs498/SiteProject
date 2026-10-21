import os
import shutil

def directory_copy_delete(source: str, destination :str):
    if not os.path.exists(destination):
        os.mkdir(destination)
    else:
        shutil.rmtree(destination)
        os.mkdir(destination)


    if os.path.exists(source):
        for item in os.listdir(source):
            src_path = os.path.join(source, item)
            dest_path = os.path.join(destination, item)

            if os.path.isfile(src_path):
                print(f"Coppied {src_path} to {dest_path}")
                shutil.copy2(src_path, dest_path)
            else:
                print(f"Coppied {src_path} to {dest_path}")
                directory_copy_delete(src_path, dest_path)
