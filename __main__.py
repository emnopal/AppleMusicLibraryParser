import argparse
from apple_music_parse_xml import AppleMusicParseXML
from typing import Dict, TypeVar, Optional, List
from pathlib import Path


V = TypeVar("V")
T = TypeVar("T")

parser: argparse.ArgumentParser = argparse.ArgumentParser()

if __name__ == '__main__':

    home: str = str(Path.home())

    parser.add_argument('-p', '--path', help="Apple Music XML file location", default=f'{home}/Library.xml')
    parser.add_argument('-f', '--format', help="Converted xml file format; Options: (csv, json, yaml)", default='json')
    parser.add_argument('-s', '--select', help="Object which want to select in XML; Separate by comma", default=None)
    parser.add_argument(
        '-i', '--index',
        help="Showing or Hiding Index, True for Show, False for Hide; Only valid if format is csv",
        type=bool, default=False
    )
    parser.add_argument('-o', '--output', help="Output location of converted file", default=f'{home}/Library')

    args: Dict[str, V] = vars(parser.parse_args())

    xml_parser: AppleMusicParseXML = AppleMusicParseXML(args.get('path'))
    output_path: str = args.get('output')
    selected_obj: Optional[str] = args.get('select')
    obj: Optional[List[str]] = []

    if selected_obj:
        obj = selected_obj.split(",")

    try:
        if args.get('format') == 'csv':
            xml_parser.save_to_csv(f"{output_path}.csv", obj, show_index=args.get('index'))
        elif args.get('format') == 'json':
            xml_parser.save_to_json(f"{output_path}.json", obj)
        elif args.get('format') == 'yaml':
            xml_parser.save_to_yaml(f"{output_path}.yaml", obj)
    except (TypeError, KeyError):
        print("Invalid Format!")
    finally:
        print("Finished!")
