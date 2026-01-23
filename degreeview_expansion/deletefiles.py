import os
import shutil


def delete_files(root_path, filename_ending, file_extension):
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(filename_ending + file_extension):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
path = "/Users/shalevwiden/Downloads/Projects/dvassets/texas/UT_courses"

# delete_files(
#     root_path=path,
#     filename_ending="namejson",
#     file_extension=".json"
# )

import os
import shutil

def delete_folders(parent_folder, folder_name_to_delete):
    """
    Deletes all subfolders named `folder_name_to_delete` inside `parent_folder`.
    """
    for root, dirs, files in os.walk(parent_folder):
        # Make a copy of dirs because we'll modify it during iteration
        for dir_name in dirs[:]:
            if dir_name == folder_name_to_delete:
                folder_path = os.path.join(root, dir_name)
                print(f"Deleting folder: {folder_path}")
                shutil.rmtree(folder_path)
                # Remove from dirs to avoid walking into it
                dirs.remove(dir_name)

# Example usage:
schoolname='stanford'
fillinlink=f'/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/degreeview_expansion/{schoolname}/assets'
delete_folders(fillinlink, "excelthemes")
