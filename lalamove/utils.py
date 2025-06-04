import inflection


def to_camel_case(s: str) -> str:
    return inflection.camelize(s, False)


def convert_keys_to_camel_case(obj):
    if isinstance(obj, dict):
        return {
            to_camel_case(key): convert_keys_to_camel_case(value)
            for key, value in obj.items()
        }
    elif isinstance(obj, list):
        return [convert_keys_to_camel_case(item) for item in obj]
    else:
        return obj
