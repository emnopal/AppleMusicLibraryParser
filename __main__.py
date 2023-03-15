import argparse
import sys
from typing import Dict, TypeVar, Optional, List
from pathlib import Path
from src.apple_music_parse_xml import AppleMusicParseXML
from src.exceptions import PythonVersionIncompatible


V = TypeVar("V")
T = TypeVar("T")

parser: argparse.ArgumentParser = argparse.ArgumentParser()

if __name__ == "__main__":

    if sys.version_info.major < 3:
        raise PythonVersionIncompatible(f"Not compatible Python version, need Python 3 but you have version {sys.version_info.major}")
    if sys.version_info.minor < 10:
        raise PythonVersionIncompatible(f"Not compatible Python version, need Python 3.10 or above but you have version 3.{sys.version_info.minor}")

    home: str = str(Path.home())

    parser.add_argument("-p", "--path", help="Apple Music XML file location", default=f"{home}/Library.xml")
    parser.add_argument("-f", "--format", help="Converted xml file format; Options: (csv, json, yaml)", default="csv")
    parser.add_argument("-s", "--select", help="Object which want to select in XML; Separate by comma", default=None)
    parser.add_argument(
        "-i", "--index", help="Showing or Hiding Index, True for Show, False for Hide; Only valid if format is csv", type=bool, default=False
    )
    parser.add_argument("-o", "--output", help="Output location of converted file", default=f"{home}/Library")

    args: Dict[str, V] = vars(parser.parse_args())

    xml_parser: AppleMusicParseXML = AppleMusicParseXML(args.get("path"))
    output_path: str = args.get("output")
    selected_obj: Optional[str] = args.get("select")
    obj: Optional[List[str]] = []

    if selected_obj:
        obj = selected_obj.split(",")

    match args.get("format"):
        case "csv":
            xml_parser.save_to_csv(f"{output_path}.csv", obj, show_index=args.get("index"))
            print(f"Saved to: {output_path}.csv")
        case "json":
            xml_parser.save_to_json(f"{output_path}.json", obj)
            print(f"Saved to: {output_path}.json")
        case "yaml":
            xml_parser.save_to_yaml(f"{output_path}.yaml", obj)
            print(f"Saved to: {output_path}.yaml")
        case "txt":
            xml_parser.save_to_csv(f"{output_path}.txt", obj, show_index=args.get("index"))
            print(f"Saved to: {output_path}.txt")
        case _:
            xml_parser.save_to_csv(f"{output_path}.csv", obj, show_index=args.get("index"))
            print(f"Saved to: {output_path}.csv")
