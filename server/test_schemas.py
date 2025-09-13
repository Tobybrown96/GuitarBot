from schemas import Song

test_song = {
  "title": "Test Song",
  "key": "G major",
  "bpm": 110,
  "time_signature": "4/4",
  "tuning": "EADGBE",
  "capo": 2,
  "progression": ["G", "D", "Em", "C"],
  "strum_pattern": "D-DU-UDU",
  "recommended_shapes": {
    "G": {"fingering": [3, 2, 0, 0, 0, 3], "suggested": True}
  },
  "ascii_tabs": {
    "G": "e|-3-|\nB|-0-|\nG|-0-|\nD|-0-|\nA|-2-|\nE|-3-|"
  }
}

song = Song(**test_song)
print(song)