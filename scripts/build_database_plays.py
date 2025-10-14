import json
import pandas as pd
from pathlib import Path

# Define paths

base_dir = Path.cwd()
raw_dir = base_dir / "data" / "rawdata"
output_file = base_dir / "data" / "plays.csv"

# Helper: parse a single file
def parse_streaming_file(file_path, content_type):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["type"] = content_type
    return df

# Collect only music streaming history
dfs = []

for file in raw_dir.glob("StreamingHistory_music_*.json"):
    dfs.append(parse_streaming_file(file, "music"))

if not dfs:
    raise FileNotFoundError("No music streaming history files found in rawdata/")

df_all = pd.concat(dfs, ignore_index=True)


# Basic cleaning
df_all = df_all.rename(columns={
    "endTime": "timestamp",
    "artistName": "artist",
    "trackName": "track",
    "msPlayed": "ms_played"
})

# Convert timestamps
df_all["timestamp"] = pd.to_datetime(df_all["timestamp"])

# Sort by time
df_all = df_all.sort_values("timestamp")

# Save
output_file.parent.mkdir(parents=True, exist_ok=True)
df_all.to_csv(output_file, index=False)

print(f"✅ Saved {len(df_all):,} plays to {output_file}")