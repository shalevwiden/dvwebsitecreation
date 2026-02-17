from pathlib import Path

def rename_files(root_folder, old_name, old_ext, new_name, new_ext=None):
    """
    Rename files inside root_folder (recursively).

    Parameters
    ----------
    root_folder : str or Path
        Folder to search
    old_name : str
        File name WITHOUT extension to match
    old_ext : str
        Extension to match ('.txt', '.py', etc)
    new_name : str
        New file name WITHOUT extension
    new_ext : str, optional
        New extension. If None, keeps old_ext
    """

    root = Path(root_folder)
    if new_ext is None:
        new_ext = old_ext

    for path in root.rglob(f"*{old_ext}"):
        if path.stem == old_name:
            new_file = path.with_name(new_name + new_ext)

            # Avoid overwriting existing files
            if new_file.exists():
                print(f"Skipping (exists): {new_file}")
                continue

            path.rename(new_file)
            print(f"Renamed: {path} → {new_file}")
rename_files(
    root_folder="my_folder",
    old_name="report",
    old_ext=".txt",
    new_name="final_report"
)