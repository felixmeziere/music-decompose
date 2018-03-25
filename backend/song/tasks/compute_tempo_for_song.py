"""
compute_tempo from Song data and store results in Song.
"""

from song.sp_functions import compute_tempo

def compute_tempo_for_song(song):
    """
    Manipulations to do on the Song instance to store result of tempo computation
    """
    ### Detect segment limits
    tempo = compute_tempo(song.original_file.file.name)

    ### Save data
    song.tempo = tempo
    song.save()
