from main import transform

def covert_image_to_json(image_file, json_file):
    json_payload = transform.encode_to_json(image_file)
    save_json_to_file(json_payload , json_file)


def save_json_to_file(json_data, file_name):
  with open(file_name, 'w') as json_fid:
        json_fid.write(json_data)

def read_json_from_file(json_file):
    with open(json_file, 'r') as fid:
        content = fid.read()
    return content