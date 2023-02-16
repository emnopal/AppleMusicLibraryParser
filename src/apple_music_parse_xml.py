import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import List, Dict, Set, Tuple, Optional, TypeVar
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

import pandas as pd
import yaml

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class AppleMusicParseXML:

    def __init__(self, path: str) -> None:
        self.path: str = path

    def _read_apple_music_xml(self) -> Element:
        tree: ElementTree = ET.parse(self.path)
        root: Element = tree.getroot()

        return root

    def _parse_apple_music_xml(self) -> List[Element]:
        root: Element = self._read_apple_music_xml()
        global_dict: List[Element] = root.findall('dict')
        global_dict_element: Element = global_dict[0]
        tracks_dict: Element = [element for element in global_dict_element if element.tag == 'dict'][0]
        tracklist: List[Element] = list(tracks_dict.findall('dict'))

        return tracklist

    def get_track(self) -> List[List[Element]]:
        tracklist: List[Element] = self._parse_apple_music_xml()
        tracks: List[List[Element]] = []

        for track in tracklist:
            track_elements: List[Element] = list(track)
            for element_num in range(len(track_elements)):
                if track_elements[element_num].text == "Apple Music" and track_elements[element_num + 1].tag == 'true':
                    tracks.append(track_elements)

        return tracks

    def length_tracks(self) -> int:
        tracks: List[List[Element]] = self.get_track()
        _length_tracks: int = len(tracks)

        return _length_tracks

    def _get_readable_track_elements(self) -> Tuple[Dict[str, Dict[str, str]], List[str]]:
        tracks: List[List[Element]] = self.get_track()
        readable_tracks_element_temp: Dict[str, Dict[str, str]] = defaultdict(dict)
        readable_tracks_column_temp: Set[str] = set()
        track_id: Optional[str] = None
        readable_track_element: Optional[str] = None

        for track in range(len(tracks)):
            for track_element in range(len(tracks[track])):
                if tracks[track][track_element].tag == "key":
                    if tracks[track][track_element].text == 'Track ID':
                        track_id = tracks[track][track_element + 1].text
                    readable_track_element = tracks[track][track_element].text
                    readable_tracks_element_temp[track_id][readable_track_element] = tracks[track][
                        track_element + 1].text
                readable_tracks_column_temp.add(readable_track_element)

        readable_tracks_element: Dict[str, Dict[str, str]] = dict(readable_tracks_element_temp)
        readable_tracks_columns: List[str] = list(readable_tracks_column_temp)

        return readable_tracks_element, readable_tracks_columns

    def get_readable_tracks_element(self, cols_to_select: Optional[List[str]] = None) -> Dict[str, Dict[str, str]]:
        tracks_element: Dict[str, Dict[str, str]] = self._get_readable_track_elements()[0]

        if cols_to_select:
            tracks_element = AppleMusicParseXML.destructuring_dict_obj(tracks_element, cols_to_select)

        return tracks_element

    def get_readable_tracks_column(self) -> List[str]:
        column: List[str] = self._get_readable_track_elements()[1]

        return column

    def save_to_json(
            self,
            path_to_save: Optional[str] = None,
            cols_to_select: Optional[List[str]] = None,
            **kwargs
    ) -> None:
        _path_to_save: Optional[str] = 'Library.json' if not path_to_save else path_to_save
        readable_tracks_element: Dict[str, Dict[str, str]] = self.get_readable_tracks_element(cols_to_select)

        with open(_path_to_save, 'w') as file:
            file.write(json.dumps(readable_tracks_element, indent=4, **kwargs))

    def save_to_yaml(
            self,
            path_to_save: Optional[str] = None,
            cols_to_select: Optional[List[str]] = None,
            **kwargs
    ) -> None:
        _path_to_save: Optional[str] = 'Library.yaml' if not path_to_save else path_to_save
        readable_tracks_element: Dict[str, Dict[str, str]] = self.get_readable_tracks_element(cols_to_select)

        with open(_path_to_save, 'w') as file:
            yaml.dump(readable_tracks_element, file, default_flow_style=False, allow_unicode=True, **kwargs)

    def _to_dataframe(
            self,
            cols_to_select: Optional[List[str]] = None,
            **kwargs
    ) -> pd.DataFrame:
        readable_tracks_element: Dict[str, Dict[str, str]] = self.get_readable_tracks_element()
        readable_tracks_element_dataframe: pd.DataFrame = pd.DataFrame.from_dict(readable_tracks_element).T

        if cols_to_select:
            readable_tracks_element_dataframe = readable_tracks_element_dataframe[cols_to_select]

        return readable_tracks_element_dataframe

    def save_to_csv(
            self,
            path_to_save: Optional[str] = None,
            cols_to_select: Optional[List[str]] = None,
            show_index: bool = False,
            **kwargs
    ) -> None:
        _path_to_save: Optional[str] = 'Library.csv' if not path_to_save else path_to_save
        readable_tracks_element_dataframe: pd.DataFrame = self._to_dataframe(cols_to_select)

        readable_tracks_element_dataframe.to_csv(_path_to_save, index=show_index, **kwargs)

    @staticmethod
    def destructuring_dict_obj(dict_obj: Dict[K, V], dict_ele: List[T]) -> Dict[K, V]:
        destructured_dict_obj: Dict[K, V] = defaultdict(dict)

        for _key, _vals in dict_obj.items():
            for ele in dict_ele:
                destructured_dict_obj[_key][ele] = _vals.get(ele, "")

        return destructured_dict_obj
