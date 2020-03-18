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
    
    

    val_manifest = "data/dev-clean_manifest.csv"
    device = "cuda"
    
    model_path = args.model_path
    package = torch.load(model_path, map_location=lambda storage, loc: storage)
    model = DeepSpeech.load_model_package(package)
    labels = model.labels
    audio_conf = model.audio_conf
    model.to(device)
    
    test_dataset = SpectrogramDataset(audio_conf=audio_conf, manifest_filepath=val_manifest, labels=labels, normalize=True, speed_volume_perturb=False, spec_augment=False)
    test_loader = AudioDataLoader(test_dataset, batch_size=20, num_workers=4)
    
    decoder = GreedyDecoder(model.labels, blank_index=model.labels.index('_'))
    target_decoder = GreedyDecoder(model.labels, blank_index=model.labels.index('_'))
    with torch.no_grad():
        evaluate(test_loader, device, model, decoder, target_decoder, verbose=True)
    print("made it this far")
