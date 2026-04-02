import os
import requests
import zipfile
import time
from duckduckgo_search import DDGS
from duckduckgo_search.exceptions import RatelimitException

def generate_image_dataset(topic: str, n: int = 10, timeout_limit: int = 180) -> tuple:
    """
    Generate image dataset for a given topic
    and return (ZIP file path, timeout_occurred boolean)
    """

    # 🔹 Clean topic name
    clean_topic = topic.replace(" ", "_").lower()

    # 🔹 Create folder
    folder_path = f"data/{clean_topic}_images"
    os.makedirs(folder_path, exist_ok=True)

    image_paths = []

    print(f"\n🔍 Generating high-quality images for: {topic}\n")

    start_time = time.time()
    timeout_occurred = False

    with DDGS() as ddgs:
        # Generate DDGS image results with retry mechanism
        results = []
        for attempt in range(3):
            try:
                results = ddgs.images(
                    keywords=topic,
                    max_results=n
                )
                break
            except RatelimitException:
                if attempt < 2:
                    time.sleep(2)
                else:
                    results = []
            except Exception:
                results = []
                break

        for i, result in enumerate(results):
            
            # Check overall timeout limit
            if time.time() - start_time > timeout_limit:
                print("Stopped early due to timeout")
                timeout_occurred = True
                break

            try:
                image_url = result["image"]

                headers = {"User-Agent": "Mozilla/5.0"}
                
                # Each individual image attempt can take up to 30s as requested
                img_data = requests.get(image_url, headers=headers, timeout=30).content

                # 🔹 Validate response
                if len(img_data) > 5000:
                    file_path = os.path.join(folder_path, f"{clean_topic}_{i+1}.jpg")

                    with open(file_path, "wb") as f:
                        f.write(img_data)

                    image_paths.append(file_path)
                    print(f"✅ Image {i+1} saved")
                else:
                    print(f"⚠️ Skipped Image {i+1} (Invalid data)")

            except Exception as e:
                print(f"❌ Error Image {i+1}: {e}")

    # 🔹 If no images found
    if not image_paths:
        print("\n❌ No images downloaded. Try another topic.\n")
        return None, timeout_occurred

    # 🔹 Create ZIP
    zip_path = f"{folder_path}.zip"

    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in image_paths:
            zipf.write(file, arcname=os.path.basename(file))

    print(f"\n🎉 Dataset Ready: {zip_path}\n")

    return zip_path, timeout_occurred