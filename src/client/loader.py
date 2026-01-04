import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DatasetLoader:
    def __init__(self, cache_dir: Path = None):
        # Allow cache_dir to be injected, or default to standard location relative to project root
        if cache_dir is None:
            # Assuming this file is in src/client/, project root is ../../
            self.cache_dir = Path(__file__).resolve().parent.parent.parent / ".cache"
        else:
            self.cache_dir = cache_dir
            
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def load(self, num_samples: int = 1000) -> list:
        cache_file = self.cache_dir / f"msmarco_pairs_{num_samples}.json"

        if cache_file.exists():
            logger.info(f"Loading cached pairs from {cache_file}")
            with open(cache_file) as f:
                pairs = json.load(f)
            logger.info(f"Loaded {len(pairs)} cached query-passage pairs")
            return [(p[0], p[1]) for p in pairs]

        return self._download_and_cache(num_samples, cache_file)

    def _download_and_cache(self, num_samples: int, cache_file: Path) -> list:
        try:
            from datasets import load_dataset as hf_load_dataset

            logger.info("Downloading MS MARCO dataset (first time only)...")
            dataset = hf_load_dataset("ms_marco", "v1.1", split="train", streaming=True)

            pairs = []
            for i, item in enumerate(dataset):
                if i >= num_samples:
                    break
                query = item["query"]
                passages = item.get("passages", {})
                passage_texts = passages.get("passage_text", [])
                if passage_texts:
                    pairs.append([query, passage_texts[0]])
                else:
                    pairs.append([query, query])

            with open(cache_file, "w") as f:
                json.dump(pairs, f)
            logger.info(f"Cached {len(pairs)} pairs to {cache_file}")
            return [(p[0], p[1]) for p in pairs]

        except ImportError:
            logger.warning("datasets not installed, using synthetic pairs")
            pairs = [
                (f"query {i}", f"document {i} with some text content") for i in range(num_samples)
            ]
            with open(cache_file, "w") as f:
                json.dump([[p[0], p[1]] for p in pairs], f)
            return pairs
