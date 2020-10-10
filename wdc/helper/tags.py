from typing import List


def array_to_tags_string(tags: List[str]) -> str:
    tags.sort()
    return ','.join(map(str, tags))
