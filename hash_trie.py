import os
import uuid
import shutil

# path from UUID 

BASE_PATH = os.path.abspath("./image_library")
TEST_DATA_PATH = os.path.abspath("./test_images")


#HELPER FUNCTIONS
def flush_images():
    shutil.rmtree(BASE_PATH)

def make_test_data():
    objs = os.scandir(TEST_DATA_PATH)
    for item in objs:
        item_name = item.name
        item_path = os.path.join(TEST_DATA_PATH, item_name)
        item_uuid = uuid.uuid4().hex
        insert_file(item_path, item_uuid)
        

def get_path_from_uuid(id: str):

    path = BASE_PATH
    for i in range(0,len(id),2):
        path = os.path.join(path,id[i:i+2])
    
    path = os.path.join(path,'')
    return path


def insert_file(src_path, id: str):
    

    hash_trie_path = get_path_from_uuid(id)
    os.makedirs(hash_trie_path, exist_ok=True)

    filename = os.path.basename(src_path)
    file_destination = os.path.join(hash_trie_path, filename)



    shutil.copyfile(src_path, file_destination)

    return

def retrieve_file_path(id: str):
    
    #given a uuid, return file path for that file
    file_directory = get_path_from_uuid(id)
    obj = os.scandir(file_directory)
    
    filename = ''
    for entry in obj:
        filename = entry.name
    
    return os.path.join(file_directory, filename)
    
def delete_file(id: str):
    
    os.remove(retrieve_file_path(id))
    os.removedirs(get_path_from_uuid(id))
    return




if __name__ == "__main__":
    os.makedirs(BASE_PATH, exist_ok=True)
    flush_images()
    make_test_data()
    # print("Testing insertion")

    # image_1_path = "./test_images/brainchem.jpg"
    # image_1_uuid = uuid.uuid4().hex    
    # insert_file(image_1_path, image_1_uuid)

    # print("\n\n Testing Lookup")
    # print(retrieve_file_path(image_1_uuid))

    # print("\n\n Testing Delete")
    # delete_file(image_1_uuid)

#lookup
#insert
#delete