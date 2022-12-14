import hashlib
from dataclasses import dataclass


@dataclass
class Source:
    # ID is late initialized
    link: str
    name: str

    def __post_init__(self):
        self.id = self._generate_id()

    def _generate_id(self):
        text = self.name.replace(" ", "").lower().encode("utf-8")
        m = hashlib.md5()
        m.update(text)
        return str(int(m.hexdigest(), 16))[0:12]

    def to_dict(self) -> dict:
        temp_dict = self.__dict__
        dict_obj = dict()
        dict_obj["id"] = temp_dict["id"]
        del temp_dict["id"]
        for key, value in temp_dict.items():
            if value is not None:
                dict_obj[key] = value

        return dict_obj
