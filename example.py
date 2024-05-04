import json

from pyusb_tree import extract_xml

data = extract_xml("usb.xml")

# preety print
print(json.dumps(data.model_dump(), indent=2))
