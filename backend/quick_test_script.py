# pylint: skip-file
# from song.models import Song, TempoEstimator
# from segmentation.models import Segmenter
# from source_separation.models import SegmentGrouper, SourceExtractor
# import numpy as np
# import h5py
# import numpy as np
# from music_decompose.services.audio_io import create_directory_for_file_if_needed

# song = Song.objects.first()
# song.tempo_estimators.all().delete()
# tempo_estimator = TempoEstimator.objects.create(
#     parent=song,
#     method='classic',
# )

# tempo_estimator.process_and_save(asynch=False)
# segmenter = Segmenter.objects.create(
#     parent=tempo_estimator,
#     method='blind',
#     n_tempo_lags_per_segment=4,
# )
# segmenter.process_and_save(asynch=False)
# segment_grouper = SegmentGrouper.objects.create(
#     parent=segmenter,
#     method='classic',
# )
# segment_grouper = SegmentGrouper.objects.first()
# segment_grouper.process_and_save(asynch=False)
# source_extractor = SourceExtractor.objects.create(
#     parent=segment_grouper,
#     method='classic',
# )

from song.models import Song, TempoEstimator
from segmentation.models import Segmenter
from source_separation.models import SegmentGrouper, SourceExtractor
import numpy as np
import h5py
import numpy as np
from music_decompose.services.audio_io import create_directory_for_file_if_needed

source_extractor = SourceExtractor.objects.first()
source_extractor.process_and_save(asynch=False)
