import os
import pandas as pd
from sentinelhub import (
    SHConfig, SentinelHubRequest, DataCollection,
    MimeType, bbox_to_dimensions, BBox, CRS
)

# ============================
# CONFIG
# ============================

config = SHConfig()
config.sh_client_id = "a907b120-6c94-411e-bf47-c6600342b16a"
config.sh_client_secret = "vDtb6GRlfOwEc5EvOuYxDfcTa5T1feNX"

BASE_DIR = r"C:\Users\Sathwika\OneDrive\Desktop\Satellite_property_valuation"
TRAIN_CSV = rf"{BASE_DIR}\Data\processed\train_processed.csv"
TEST_CSV  = rf"{BASE_DIR}\Data\processed\test_processed.csv"
IMAGE_DIR = rf"{BASE_DIR}\images"

os.makedirs(IMAGE_DIR, exist_ok=True)

# ============================
# REQUEST FUNCTION
# ============================

def fetch_image(lat, lon, save_path, size=64):
    bbox = BBox(
        bbox=[lon-0.001, lat-0.001, lon+0.001, lat+0.001],
        crs=CRS.WGS84
    )
    resolution = 10
    size = bbox_to_dimensions(bbox, resolution)

    request = SentinelHubRequest(
        evalscript="""
        //VERSION=3
        function setup() {
          return {
            input: ["B04", "B03", "B02"],
            output: { bands: 3 }
          };
        }
        function evaluatePixel(sample) {
          return [sample.B04, sample.B03, sample.B02];
        }
        """,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=("2022-01-01", "2023-01-01"),
            )
        ],
        responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
        bbox=bbox,
        size=size,
        config=config,
    )

    image = request.get_data()[0]
    from PIL import Image
    Image.fromarray(image).save(save_path)

# ============================
# MAIN
# ============================

def download(df, split):
    folder = os.path.join(IMAGE_DIR, split)
    os.makedirs(folder, exist_ok=True)

    for _, row in df.iterrows():
        path = os.path.join(folder, f"{row['id']}.png")
        if os.path.exists(path):
            continue
        fetch_image(row["lat"], row["long"], path)

if __name__ == "__main__":
    train = pd.read_csv(TRAIN_CSV).head(5000)
    test  = pd.read_csv(TEST_CSV).head(1000)

    print("Downloading Sentinel images...")
    download(train, "train")
    download(test, "test")
    print("Done.")
