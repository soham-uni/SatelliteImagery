import os
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
BASE_URL = "https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static"

def fetch_image(lat, lon, save_path, zoom=18, size=224):
    url = (
        f"{BASE_URL}/{lon},{lat},{zoom}/{size}x{size}"
        f"?access_token={MAPBOX_TOKEN}"
    )
    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        Path(save_path).write_bytes(r.content)
        return True
    return False


def fetch_images_from_csv(csv_path, image_dir, id_col="id", max_workers=16):
    df = pd.read_csv(csv_path)
    image_dir = Path(image_dir)
    image_dir.mkdir(parents=True, exist_ok=True)

    tasks = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for _, row in df.iterrows():
            img_path = image_dir / f"{row[id_col]}.png"
            if img_path.exists():
                continue
            tasks.append(
                executor.submit(
                    fetch_image,
                    row["lat"],
                    row["long"],
                    img_path
                )
            )

        for _ in tqdm(as_completed(tasks), total=len(tasks)):
            pass

