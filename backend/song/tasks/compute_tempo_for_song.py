"""
compute_tempo from Song data and store results in Song.
"""

from song.sp_functions import compute_tempo
from song.models import Song

def compute_tempo_for_song(song_uuid):
    """
    The function
    """
    ### Initialise
    song = Song.objects.get(pk=song_uuid)
    song.tempo_estimation_status = 'pending'
    song.save()

    try:
        ### Detect segment limits
        tempo = compute_tempo(song.original_file.file.name)

        ### Save data
        song.tempo = tempo

        ### End
        song.tempo_estimation_status = 'done'
        song.save()
    except Exception as error:
        song.tempo_estimation_status = 'failed'
        song.save()
        raise error
