import os
import shutil
import logger as logger


def get_logger(print_to_screen=False):


    """
    Uses the logger.py module to create a logger.

    Args:
        print_to_screen: for printing to screen as well as file.
    """
    return logger.initialize_logger(print_to_screen)


def get_renamed_file_path(existing_name, string_to_find, string_to_replace, prefix, suffix):


    """
    Returns the target file path given an existing file name and string operations.

    Args:
        existing_name: the existing file's name.
        string_to_find: a string, list, or tuple of strings to find and replace.
        string_to_replace: the string to replace occurrences of string_to_find with.
        prefix: a string to insert at the beginning of the filename.
        suffix: a string to append to the end of the filename.
    """
    directory, filename = os.path.split(existing_name)
    name, ext = os.path.splitext(filename)

    #making sure string_to_find is either a list or tuple, if not turn it to a list
    if isinstance(string_to_find, (list, tuple)):  
        string_to_find = list(string_to_find)  
        string_to_find.sort(reverse=True) 
        for target in string_to_find:
            name = name.replace(str(target), string_to_replace)  
    elif isinstance(string_to_find, str):
        name = name.replace(string_to_find, string_to_replace)  #replace if it's a string

    #apply prefix and suffix
    new_name = f"{prefix}{name}{suffix}{ext}"
    return os.path.join(directory, new_name)


def get_files_with_extension(folder_path, extension):


    """
    Returns a list of file paths in a given folder that match the specified extension.

    Args:
        folder_path: The path of the folder to search.
        extension: The file extension to filter by.
    """
    if not os.path.isdir(folder_path):
        return []

    return [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and f.endswith(extension)
    ]


def rename_file(logger, existing_name, new_name, copy=False):


    """
    Renames or copies a file.

    Args:
        logger: Logger instance for logging operations.
        existing_name: Full path to the existing file.
        new_name: Full path for the renamed file.
        copy: If True, copies the file instead of renaming it.
    """
    if not os.path.isfile(existing_name):
        logger.error(f"File not found: {existing_name}")
        return False

    if os.path.isfile(new_name):
        logger.warning(f" File already exists: {new_name}")
        return False

    try:
        if copy:
            shutil.copy(existing_name, new_name)
            logger.info(f"Copied file: {existing_name} -> {new_name}")
        else:
            shutil.move(existing_name, new_name)
            logger.info(f"Renamed file: {existing_name} -> {new_name}")

        return True

    except Exception as e:
        logger.error(f"Error in renaming {existing_name} to {new_name}: {e}")
        return False


def rename_files_in_folder(logger, folder_path, extension, string_to_find, string_to_replace, prefix, suffix, copy=False):


    """
    Renames or copies all files in a folder with a given extension.

    Args:
        logger: Logger instance.
        folder_path: The folder containing files to rename.
        extension: The file extension to filter.
        string_to_find: A string, list, or tuple of strings to find and replace.
        string_to_replace: The string to replace occurrences with.
        prefix: A string to prepend to the filename.
        suffix: A string to append to the filename.
        copy: If True, copies the file instead of renaming it.
    """
    files = get_files_with_extension(folder_path, extension)

    if not files:
        logger.warning(f"No files found with extension {extension} in {folder_path}")
        return

    for file in files:
        new_path = get_renamed_file_path(file, string_to_find, string_to_replace, prefix, suffix)
        rename_file(logger, file, new_path, copy)