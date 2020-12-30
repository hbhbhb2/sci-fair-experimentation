"""char_dataset dataset."""

import tensorflow_datasets as tfds
import csv

_DESCRIPTION = """
Character dataset extracted from the Kaggle transcription of 400,000 handwritten names (https://www.kaggle.com/landlord/handwriting-recognition).

Processing steps:
 * Corrupted examples skipped
 * Characters of names incorrectly divided by pytesseract skipped
 * Images cropped to 256x256
"""

# TODO(char_dataset): BibTeX citation
_CITATION = """
"""


class CharDataset(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for char_dataset dataset."""

  MANUAL_DOWNLOAD_INSTRUCTIONS = """
    Download the train.zip and place in the manual_dir/.
  """

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            # These are the features of your dataset like images, labels ...
            'image': tfds.features.Image(shape=(256, 256, 3), encoding_format='jpeg'),
            'label': tfds.features.ClassLabel(names=[*"ABCDEFGHIJKLMNOPQRSTUVWXYZ-'"])
        }),
        # If there's a common (input, target) tuple from the
        # features, specify them here. They'll be used if
        # `as_supervised=True` in `builder.as_dataset`.
        supervised_keys=('image', 'label'),  # e.g. ('image', 'label')
        homepage='https://www.kaggle.com/landlord/handwriting-recognition',
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    zip_path = dl_manager.manual_dir / 'train.zip'
    path = dl_manager.extract(zip_path)

    return {
        'train': self._generate_examples(
            img_path = path / 'train',
            csv_path = path / 'train.csv'
          ),
    }

  def _generate_examples(self, img_path, csv_path):
    """Yields examples."""
    with csv_path.open() as f:
      for row in csv.DictReader(f):
        id = row['FILENAME']
        yield id, {
          'image': img_path / id,
          'label': row['IDENTITY']
        }
