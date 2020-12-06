from pathlib import Path
import pandas as pd
import json
import jsonschema as jc


def create_error(file_name, schema_name, error_message, file_property='', schema_path=''):
    return {
        'File': file_name,
        'Schema': schema_name,
        'Error': error_message,
        'Property with error': file_property,
        'Path to rule in schema': schema_path
    }


def get_dict_with_jsons(dir):
    jsons_dict = {}
    for file in dir.iterdir():
        with open(file) as f:
            jsons_dict[file.stem] = json.load(f)
    return jsons_dict


def check_schemas(schemas_dict):
    errors_list = []
    for name, schema in schemas_dict.items():
        try:
            jc.Draft7Validator.check_schema(schema)
        except jc.SchemaError as e:
            errors_list.append(create_error('-', name, 'Invalid schema'))
    return errors_list


def check_readability(events_dict):
    errors_list = []
    events_to_check = {}
    for name, event in events_dict.items():
        if not isinstance(event, dict):
            errors_list.append(create_error(name, '-', "Unpropriate format"))
        elif 'event' not in event:
            errors_list.append(create_error(name, '-', "Missing key 'event'"))
        elif 'data' not in event or event['data'] is None:
            errors_list.append(create_error(name, '-', "Missing key 'data'"))
        else:
            events_to_check[name] = event
    return errors_list, events_to_check


def _compare_with_all_schemas(name, event):
    errors_list = []
    for schema_name, schema in schema_validators.items():
        errors = validate_data(schema, name, event)
        if len(errors) == 0:
            error_message = "File with key 'event'={} is valid for {}.schema".format(event['event'], schema_name)
            errors_list.append(create_error(name, schema_name, error_message))
    if len(errors_list) == 0:
        errors_list.append(create_error(name, '-', "There is no {}.schema".format(event['event'])))
    return errors_list


def convert_path(path):
    path = [str(i) for i in list(path)]
    return ': '.join(path)


def validate_data(schema_validator, name, event):
    errors = []
    for err in schema_validator.iter_errors(event['data']):
        errors.append(create_error(name, event['event'], err.message,
                                   file_property=convert_path(err.path),
                                   schema_path=convert_path(err.schema_path)))
    return errors


def validate_events_data(events_dict, schema_validators):
    errors_list = []
    for name, event in events_dict.items():
        event_key = event['event']
        if event_key not in schema_validators:
            errors_list.extend(_compare_with_all_schemas(name, event))
        else:
            event_errors = validate_data(schema_validators[event_key], name, event)
            if len(event_errors) == 0:
                errors_list.append(create_error(name, event_key, 'File is OK'))
            else:
                errors_list.extend(event_errors)
    return errors_list


main_dir = Path(r'C:\Users\mahakomar\Desktop\task_folder')
event_dir = main_dir / 'event'
schema_dir = main_dir / 'schema'

events_dict = get_dict_with_jsons(event_dir)
schemas_dict = get_dict_with_jsons(schema_dir)

errors_list = []
# Check validity of schemas
errors_list.extend(check_schemas(schemas_dict))
# Check readability of events json files
read_errors, events_to_check = check_readability(events_dict)
errors_list.extend(read_errors)
# Compare data with schemas
schema_validators = {name: jc.Draft7Validator(schema) for name, schema in schemas_dict.items()}
errors_list.extend(validate_events_data(events_to_check, schema_validators))

errors_df = pd.DataFrame(errors_list,
                         columns=['File', 'Schema', 'Error',
                                  'Property with error',
                                  'Path to rule in schema']).set_index(['File', 'Schema', 'Error'])
with open('errors_table.html', 'w') as f:
    f.write(errors_df.to_html())






