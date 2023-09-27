import os
import shutil
import json
import time
from lxml import etree
from bg3modutils import Log
from concurrent.futures import ProcessPoolExecutor
from typing import Optional, Literal, Tuple, List, Dict


class FileManager:
    # Creates a directory if it doesn't exist
    @staticmethod
    def create_folder(path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                Log.debug(f"Created directory {path}")
            except Exception as e:
                Log.error(f"Failed to create directory {path}: {e}")
                return False

    @staticmethod
    def delete_folder(path):
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
        except Exception as e:
            Log.error(f"An error occurred while deleting folder: {e}")
    # Deletes all files and folders in the specified folder

    @staticmethod
    def clean_folder(folder_path):
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        # Log.debug(f'Successfully deleted {file_path}')
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        # Log.debug(f'Successfully deleted directory {file_path}')
                except Exception as e:
                    Log.error(f'Failed to delete {file_path}. Reason: {e}')
        except Exception as e:
            Log.error(f'Failed to clean folder. Reason: {e}')

    # Searches for files with the specified names in the specified folder
    @staticmethod
    def find_files(folder_path: str, target_filenames: Optional[List[str]] = None, target_extensions: Optional[List[str]] = None) -> List[str]:
        try:
            time_start = time.time()
            found_files = []

            # First, search the top-level directory without multiprocessing
            found_files.extend(deep_search((folder_path, target_filenames, target_extensions)))

            MAX_WORKERS = os.cpu_count()

            # Use multiprocessing to search only the immediate subdirectories of folder_path
            directories_to_search = [d.path for d in os.scandir(folder_path) if d.is_dir()]

            with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
                args = [(dir_path, target_filenames, target_extensions) for dir_path in directories_to_search]
                for result in executor.map(deep_search, args):
                    found_files.extend(result)

            time_end = time.time()
            Log.success(f"Found {len(found_files)} files in {time_end - time_start} seconds")
            return found_files
        except Exception as e:
            Log.error(f"An error occurred while searching for files: {e}")

    # Searches for folders with the specified names in the specified folder
    @staticmethod
    def find_folders(folder_path: str, target_folder_names: List[str]) -> Dict[str, str]:
        found_folders = {}
        try:
            for root, dirs, _ in os.walk(folder_path):
                for dir_name in dirs:
                    if dir_name in target_folder_names:
                        found_folders[dir_name] = os.path.join(root, dir_name)
        except Exception as e:
            Log.error(f"An error occurred while searching for target folders: {e}")

        return found_folders

    # Creates a file if it doesn't exist
    @staticmethod
    def create_file(path):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write('')  # Create an empty file
            # Log.debug(f"Created file {path}")
        except Exception as e:
            Log.error(f"Failed to create file {path}: {e}")
            return False

    @staticmethod
    def delete_file(path):
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            Log.error(f"An error occurred while deleting file: {e}")
    # Saves an object instance to a JSON file

    @staticmethod
    def save_object_to_json(obj, path):
        try:
            with open(path, 'w') as f:
                if isinstance(obj, dict):
                    json.dump(obj, f)
                else:
                    json.dump(obj.__dict__, f)
            # Log.info(f"Saved object instance to {path}")
        except Exception as e:
            Log.error(f"Failed to save object instance to {path}: {e}")

    # Loads an object instance from a JSON file
    @staticmethod
    def load_object_from_json(obj, path):
        try:
            with open(path, 'r') as f:
                data = f.read()
                if not data:
                    return {}
                return json.loads(data)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            Log.error(f"Failed to decode JSON from {path}")
            return {}

    # writes a list of strings to a file
    @staticmethod
    def write_file(file_path: str, content_list: List[str], mode: Literal['a', 'w'] = 'w'):
        try:
            with open(file_path, mode) as file:
                for line in content_list:
                    file.write(f"{line}\n")
        except Exception as e:
            print(f"Failed to write to file {file_path} in {mode} mode: {e}")

    # Inserts the specified data after the last node with the specified id in the specified XML file
    @staticmethod
    def insert_string_to_xml(xml_file_path, xpath_expr, string_to_insert, namespace=None, position: Literal['first', 'last'] = 'last'):
        # Parse the XML file
        tree = etree.parse(xml_file_path)
        root = tree.getroot()

        # If a namespace is provided, update the XPath expression to include it
        if namespace:
            xpath_expr = xpath_expr.replace('//', f"//{namespace}:")

        # Find all nodes using the XPath expression
        nsmap = {namespace: root.nsmap[None]} if namespace else None
        nodes = root.xpath(xpath_expr, namespaces=nsmap)

        # If no node matching the XPath is found, return
        if not nodes:
            return "No node found"

        # Parse the string to insert into an Element object
        new_element = etree.fromstring(string_to_insert)

        # Check if the element already exists
        existing_nodes = [node for node in nodes if (
            node.tag == new_element.tag and
            node.attrib == new_element.attrib and
            len(node) == len(new_element) and
            all(c1.tag == c2.tag and c1.attrib == c2.attrib for c1, c2 in zip(node, new_element))
        )]

        if existing_nodes:
            return "Element already exists"

        # Choose the target node based on the position parameter
        target_node = nodes[0] if position == 'first' else nodes[-1]

        # Insert the new element after the last node
        parent = target_node.getparent()
        index = parent.index(target_node)
        parent.insert(index + 1, new_element)

        # Save the modified XML back to the file
        tree.write(xml_file_path, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    # converts an XML file to a string
    @staticmethod
    def xml_to_string(xml_file_path):
        try:
            with open(xml_file_path, 'r', encoding='utf-8') as file:
                # remove first line
                # file.readline()
                meta_string = file.read()
            return meta_string
        except Exception as e:
            Log.error(f"Failed to convert XML file to string: {e}")
            return None

    # removes loose strings from an XML file
    @staticmethod
    def remove_loose_strings_from_xml(file_path):
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(file_path, parser)
            root = tree.getroot()

            def recurse_remove_text(element):
                element.text = None
                element.tail = None
                for child in element:
                    recurse_remove_text(child)

            recurse_remove_text(root)

            with open(file_path, 'wb') as f:
                tree.write(f)
        except Exception as e:
            Log.error(f"An error occurred while removing loose strings from {file_path}: {e}")

    @staticmethod
    def get_file_names(folder_path: str, extension: str) -> List[str]:
        try:
            return [os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.lower().endswith(f".{extension.lower()}")]
        except Exception as e:
            Log.error(f"An error occurred while getting file names: {e}")
            return []

    @staticmethod
    def copy_folder(src_path, dest_path):
        try:
            if not os.path.exists(src_path):
                Log.debug(f"Source folder {src_path} does not exist. Skipping...")
                return
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)

            for item in os.listdir(src_path):
                s = os.path.join(src_path, item)
                d = os.path.join(dest_path, item)

                if os.path.isdir(s):
                    if not os.path.exists(d):
                        os.makedirs(d)
                    FileManager.copy_folder(s, d)
                else:
                    shutil.copy2(s, d)  # This will overwrite the file if it already exists
        except Exception as e:
            Log.error(f"An error occurred while copying folder: {e}")

    @staticmethod
    def get_attribute_from_xml(xml_file_path, key, value, attribute_name) -> str:
        try:
            # Parse the XML file
            tree = etree.parse(xml_file_path)
            root = tree.getroot()

            # Create XPath expression (using // to search through all descendant nodes)
            xpath_expr = f"//node[attribute[@id='{key}'][@value='{value}']]/attribute[@id='{attribute_name}']/@value"

            # Execute XPath query
            attribute_value = root.xpath(xpath_expr)

            # The XPath query returns a list, so we get the first item
            return attribute_value[0] if attribute_value else None

        except Exception as e:
            Log.error(f"An error occurred while getting attribute from XML: {e}")
            return None


def deep_search(directory_and_target: Tuple[str, Optional[List[str]]]) -> List[str]:
    directory, target_filenames = directory_and_target
    local_found_files = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if target_filenames is None or filename in target_filenames:
                local_found_files.append(os.path.join(root, filename))

    return local_found_files
