import re
import xml.etree.ElementTree as ET
from pathlib import Path
from subprocess import run
from tempfile import gettempdir

from pydantic import BaseModel

BIN_PATH = Path(__file__).parent / "bin" / "UsbTreeView.exe"


class Node(BaseModel):
    name: str
    attributes: dict[str, str]
    children: list["Node"]


def extract_attributes(texts: list[ET.Element]):
    attributes: dict[str, str] = {}
    for t in texts:
        if t.text:
            for key, value in re.findall(r"([ a-zA-Z0-9]+):(.+)", t.text):
                attributes[key.strip()] = value.strip()
    return attributes


def extract_node(node: ET.Element) -> Node:
    texts = [n for n in node if n.tag == "text"]
    nodes = [n for n in node if n.tag == "node"]

    return Node(
        name=node.attrib["text"],
        attributes=extract_attributes(texts),
        children=[extract_node(n) for n in nodes],
    )


def extract_xml(file_path: str | Path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return extract_node(root[0])


def get_devices():
    path = Path(gettempdir()) / "usb.xml"
    run([BIN_PATH, f"-X={path}"], timeout=30)
    return extract_xml(path)
