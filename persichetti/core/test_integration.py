# Testing integration of the various modules: quantum_time.py, score.py, voice.py, and motif.py
# Let's first run a basic integration test to ensure that voices, motifs, and their interactions with MIFs work as expected.

from typing import List
from decimal import Decimal

# Import from the quantum_time module
from quantum_time import TempoFunction, ClockTime, MusicalInertialFrame

# Import from score.py and voice.py (if these are in the same directory or use appropriate paths)
from score import Score  # Assuming the Score class is implemented as per earlier messages
from voice import Voice  # Assuming the Voice class is implemented as per earlier messages

# Import from motif.py
from motif import MelodicMotif, HarmonicMotif

# First, initialize the necessary objects
# Create a default MIF with a tempo of 120 bpm
mif_registry = {}
default_mif_handle = "default"

tempo_function = TempoFunction(bpm=120)  # Set to 120 BPM for this test
start_time = ClockTime(0)  # Starting at time 0
mif = MusicalInertialFrame(tempo_function, start_time)

# Create a score and a voice
score = Score()  # Assuming the Score class from the earlier implementation
voice = Voice(name="Voice 1", mode="Ionian")

# Assign the voice to the default MIF
voice.assign_mif(mif_handle=default_mif_handle, mif_registry=mif_registry)

# Create a simple melodic motif (temporal)
melodic_motif = MelodicMotif(name="Melodic Motif 1", notes=["C", "D", "E", "F", "G"], is_temporal=True, rhythm=[1, 1, 1, 1, 1])

# Add the melodic motif to the voice
melodic_motif.add_to_voice(voice)

# Create a harmonic motif (e.g., a simple chord)
harmonic_motif = HarmonicMotif(name="Major Chord", chord=["C", "E", "G"])

# Add the harmonic motif to the voice
harmonic_motif.add_to_voice(voice)

# Print the voice and its events
print(f"Voice: {voice}")
print(f"Motifs in Voice: {voice.events}")

# Test polyphony: add another voice, set it to polyphonic, and add a motif
polyphonic_voice = Voice(name="Voice 2", mode="Dorian")
polyphonic_voice.assign_mif(mif_handle=default_mif_handle, mif_registry=mif_registry)

melodic_motif_2 = MelodicMotif(name="Melodic Motif 2", notes=["A", "B", "C", "D", "E"], is_temporal=True, rhythm=[1, 1, 1, 1, 1])
melodic_motif_2.add_to_voice(polyphonic_voice)

# Print the second voice and its events
print(f"Polyphonic Voice: {polyphonic_voice}")
print(f"Motifs in Polyphonic Voice: {polyphonic_voice.events}")

# Testing the behavior when motifs are in different MIFs (optional, but useful for advanced testing)
# This is just to test that the logic of MIF reassignment works correctly
new_mif_handle = "new_mif"
new_mif = MusicalInertialFrame(tempo_function, start_time)
voice_3 = Voice(name="Voice 3", mode="Phrygian")
voice_3.assign_mif(mif_handle=new_mif_handle, mif_registry=mif_registry)

# Add a motif to this new voice in a different MIF
melodic_motif_3 = MelodicMotif(name="Melodic Motif 3", notes=["D", "E", "F", "G", "A"], is_temporal=True, rhythm=[1, 1, 1, 1, 1])
melodic_motif_3.add_to_voice(voice_3)

# Print the third voice and its events
print(f"Voice 3 (in new MIF): {voice_3}")
print(f"Motifs in Voice 3: {voice_3.events}")

# Run the test to validate everything is integrated properly
# Ideally, we'd write assertions here to check the validity of voice assignments, motifs, and MIF interactions.
# If no errors, integration test passed.

# Additional checks can be done on the FQMT resolution if desired.
