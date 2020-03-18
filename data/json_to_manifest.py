# standard library
import os
import json
import argparse


def main(json_path:str)->None:
    """
    Converts the data json used by Speech by Awni Hanun into
    manifest.csv files used by Deepspeech2 by Sean Naren.
    Enteries in data.json look like:
    {"text": [<comma separated labels>], "duration": X.XX, "audio": <path_to_audio>}
    Entries in manifest.csv look like:
    path/to/audio,path/to/txt_labels
    This file will parse the data.json, save the labels in a txt
    file, and then output a manifest file
    """

    with open(json_path, 'r') as fid:
        data_json = [json.loads(line) for line in fid]

    manifest_name = os.path.basename(json_path).replace(".json", "_manifest.csv")
    convert_to_manifest(data_json, manifest_name)


def convert_to_manifest(data_json:list, manifest_name:str):
    """
    parses the data_json, writes phone label list to txt file, and
    puts audio and label path in manifest.csv format
    Arguments:
        data_json (list(dict))
        manifest_name (str): name of file to write
    """
    
    audio_txt_paths = parse_write_labels(data_json)
    write_manifest(audio_txt_paths, manifest_name)
    
def parse_write_labels(data_json:list):
    
    data_paths = list(tuple())
    for sample in data_json:
        phones = sample.get("text", [])
        audio_path = sample.get("audio", "")
        extensions = [".wav", ".wv"]
        audio_ext = list(filter(lambda x: x in audio_path, extensions))[0]
        txt_path = audio_path.replace(audio_ext, ".txt")
        write_to_file(phones, txt_path)
        data_paths.append((audio_path, txt_path))
     
    return data_paths


def write_to_file(phones:list, txt_path:str):
    """
    writes phonemes in phones to txt_path
    """
    with open(txt_path, 'w') as fid:
        phone_str = " ".join(phones) 
        fid.write(phone_str) 


def write_manifest(audio_text_paths:list, manifest_name:str):
    
    manifest_path = os.path.join("./", manifest_name)
    with open(manifest_path, 'w') as fid:
        for audio_path, text_path in audio_text_paths:
            fid.write(f"{audio_path},{text_path}\n")


if __name__=="__main__":
    parser = argparse.ArgumentParser(
            description="Converts a data.json into manifest.csv")
    parser.add_argument("--json-path", 
        help="A path to the data json with the audio file path and labels.")
    args = parser.parse_args()

    main(args.json_path)
