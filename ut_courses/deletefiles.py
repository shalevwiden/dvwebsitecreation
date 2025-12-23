import os


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

delete_files(
    root_path=path,
    filename_ending="namejson",
    file_extension=".json"
)
