from collections import defaultdict
import os
import json
import csv

import datasets

_NAME="loading_script"
_VERSION="1.0.0"

_DESCRIPTION = """
This is a script to load a dataset in a Hugging Face object.
"""

_CITATION = """
@misc{menaloadingscript2023,
      title={Loading Script.}, 
      author={Hernandez Mena, Carlos Daniel},
      year={2023},
      url={https://huggingface.co/carlosdanielhernandezmena},
}
"""

_HOMEPAGE = "https://huggingface.co/carlosdanielhernandezmena"

_LICENSE = "CC-BY-4.0, See https://creativecommons.org/licenses/by/4.0/"

_BASE_DATA_DIR = "data/"
_METADATA_TRAIN = _BASE_DATA_DIR + "train.tsv"
_METADATA_TEST = _BASE_DATA_DIR + "test.tsv"
_METADATA_DEV = _BASE_DATA_DIR + "dev.tsv"

class DummyCorpusAsrEsConfig(datasets.BuilderConfig):
    """BuilderConfig for Loading Script."""

    def __init__(self, name, **kwargs):
        name=_NAME
        super().__init__(name=name, **kwargs)

class DummyCorpusAsrEs(datasets.GeneratorBasedBuilder):
    """Loading Script."""

    VERSION = datasets.Version(_VERSION)
    BUILDER_CONFIGS = [
        DummyCorpusAsrEsConfig(
            name=_NAME,
            version=datasets.Version(_VERSION),
        )
    ]

    def _info(self):
        features = datasets.Features(
            {
                "audio_id": datasets.Value("string"),
                "audio": datasets.Audio(sampling_rate=16000),
                "normalized_text": datasets.Value("string"),
                "absolute_path": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
    
        metadata_train=dl_manager.download_and_extract(_METADATA_TRAIN)
        metadata_test=dl_manager.download_and_extract(_METADATA_TEST)
        metadata_dev=dl_manager.download_and_extract(_METADATA_DEV)
        
        meta_paths={"train":metadata_train,"test":metadata_test,"dev":metadata_dev}
        
        with open(metadata_train) as f:
            hash_meta_train = {x["audio_id"]: x for x in csv.DictReader(f, delimiter="\t")}

        with open(metadata_test) as f:
            hash_meta_test = {x["audio_id"]: x for x in csv.DictReader(f, delimiter="\t")}

        with open(metadata_dev) as f:
            hash_meta_dev = {x["audio_id"]: x for x in csv.DictReader(f, delimiter="\t")}            
        
        hash_audios=defaultdict(dict)
        hash_audios["train"]=[]
        for audio_in in hash_meta_train:
            hash_audios["train"].append(hash_meta_train[audio_in]["absolute_path"])

        hash_audios["test"]=[]
        for audio_in in hash_meta_test:
            hash_audios["test"].append(hash_meta_test[audio_in]["absolute_path"])
        
        hash_audios["dev"]=[]
        for audio_in in hash_meta_dev:
            hash_audios["dev"].append(hash_meta_dev[audio_in]["absolute_path"])

        absolute_paths=hash_audios
        
        audio_paths = dl_manager.download(hash_audios)
        
        local_extracted_audio_paths = dl_manager.download_and_extract(audio_paths)

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "audio_archives":[dl_manager.iter_archive(archive) for archive in audio_paths["train"]],
                    "local_extracted_archives_paths": local_extracted_audio_paths["train"],
                    "metadata_paths": meta_paths["train"],
                    "absolute_paths":absolute_paths["train"],
                }
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={
                    "audio_archives": [dl_manager.iter_archive(archive) for archive in audio_paths["dev"]],
                    "local_extracted_archives_paths": local_extracted_audio_paths["dev"],
                    "metadata_paths": meta_paths["dev"],
                    "absolute_paths":absolute_paths["dev"],
                }
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "audio_archives": [dl_manager.iter_archive(archive) for archive in audio_paths["test"]],
                    "local_extracted_archives_paths": local_extracted_audio_paths["test"],
                    "metadata_paths": meta_paths["test"],
                    "absolute_paths":absolute_paths["test"],
                }
            ),
        ]

    def _generate_examples(self, audio_archives, local_extracted_archives_paths, metadata_paths,absolute_paths):

        features = ["normalized_text","absolute_path"]
        
        meta_path = metadata_paths

        with open(meta_path) as f:
            metadata = {x["audio_id"]: x for x in csv.DictReader(f, delimiter="\t")}

        for audio_archive,local_path,rel_path in zip(audio_archives,local_extracted_archives_paths,absolute_paths):
            audio_id =os.path.splitext(os.path.basename(rel_path))[0]
            path = local_path
                        
            yield audio_id, {
                "audio_id": audio_id,
                **{feature: metadata[audio_id][feature] for feature in features},
                "audio": {"path": path},
            }

