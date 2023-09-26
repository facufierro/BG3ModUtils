import subprocess
import logging
from typing import Literal


class LSLib:
    @staticmethod
    def execute_command(command: Literal["create-package", "extract-package", "convert-resource", "convert-loca"],
                        source_path: str, destination_path: str, input_format: str = None, output_format: str = None, package_priority: int = None) -> None:
        try:
            if package_priority is None:
                package_priority = 0
            package_priority = str(package_priority)

            if input_format is None or output_format is None:
                command_string = [
                    'src\\bg3modutils\\utils\\ExportTool',
                    "-g",
                    "bg3",
                    "-a",
                    command,
                    "-c",
                    "lz4",
                    "--source",
                    source_path,
                    "--destination",
                    destination_path,
                    "--package-priority",
                    package_priority,
                    "-l",
                    "all",
                ]
            else:
                command_string = [
                    'src\\bg3modutils\\utils\\ExportTool',
                    "-g",
                    "bg3",
                    "-a",
                    command,
                    "-c",
                    "lz4",
                    "--source",
                    source_path,
                    "--destination",
                    destination_path,
                    "--input-format",
                    input_format,
                    "--output-format",
                    output_format,
                    "--package-priority",
                    package_priority,
                    "-l",
                    "all",
                ]
            result = subprocess.run(command_string)
            if result.returncode == 0:
                return True
            else:
                return False
        except Exception as e:
            logging.error(
                f"An error occurred while executing the lslib command. Reason: {e}")
