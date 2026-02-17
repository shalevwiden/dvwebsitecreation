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


BASE_DIR = Path(__file__).resolve().parent
print(f'BASE_DIR {BASE_DIR}')
        
dvexpansionfolder= BASE_DIR.parent / 'degreeview_expansion'

print(dvexpansionfolder)
print(dvexpansionfolder.exists())
rename_files(
    root_folder=dvexpansionfolder,
    old_name="unicolor",
    old_ext=".json",
    new_name="unidetails"
)