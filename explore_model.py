# standard library
import json
import argparse

# third-party libraries
import torch

# project libraries
from decoder import GreedyDecoder
from test import evaluate
from data.data_loader import AudioDataLoader, SpectrogramDataset
from model import DeepSpeech

parser = argparse.ArgumentParser(description="evaluates model and shows model contents")
parser.add_argument('--model-path', default='', type=str, help='path to model to load')



if __name__ == "__main__":

    args = parser.parse_args()
    
    model_path = args.model_path
    package = torch.load(model_path, map_location=lambda storage, loc: storage)
    model = DeepSpeech.load_model_package(package)
    print(f"package keys: {[key for key in package.keys()]}")
    show_keys = ['version', 'hidden_size', 'hidden_layers', 'rnn_type', 'audio_conf', 'labels',
                 'bidirectional', 'amp', 'epoch', 'loss_results', 'cer_results', 'wer_results']
    for key in package.keys():
        if key in show_keys:
            print(f"key: {key}, contents: {package.get(key)}")
    print(f"model: {model}") 
