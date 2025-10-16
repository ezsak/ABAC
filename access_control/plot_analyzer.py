# import os
# import json
# import io
# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load .env file
# load_dotenv()
# # ==== CONFIGURE GEMINI ====
# # Replace with your Gemini API key
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# # === Utility: extract bar data from plot ===
# def extract_histogram_from_plot(image_path):
#     """
#     Extracts approximate (x, y) values from a bar chart image
#     by using Gemini vision model to analyze the bars.
#     """
#     model = genai.GenerativeModel("gemini-2.5-flash")

#     prompt = (
#         "You are given a histogram-like bar chart image. "
#         "Identify the number of bars (n) and return an array of bar heights "
#         "corresponding to each bar (y-values). Return as valid JSON: "
#         "{'n': <int>, 'heights': [list of integers]}."
#     )

#     img = Image.open(image_path)
#     response = model.generate_content([prompt, img])
#     try:
#         text = response.text.strip()
#         data = json.loads(text)
#         return data
#     except Exception:
#         print("Gemini output could not be parsed. Response:")
#         print(response.text)
#         return None

# # === Distribution detection logic ===
# def detect_distribution(heights):
#     heights = np.array(heights)
#     n = len(heights)
#     x = np.arange(1, n + 1)

#     # Normalize
#     probs = heights / np.sum(heights)

#     # --- Check for Uniform ---
#     if np.std(probs) < 0.05 * np.mean(probs):
#         return {"distribution": "Uniform", "n": n}

#     # --- Try Poisson fit ---
#     mean_est = np.sum(x * probs)
#     var_est = np.sum((x - mean_est) ** 2 * probs)
#     if abs(var_est - mean_est) / mean_est < 0.3:  # variance ≈ mean
#         lam = round(mean_est, 2)
#         return {"distribution": "Poisson", "lambda": lam, "n": n}

#     # --- Otherwise, Normal ---
#     return {"distribution": "Normal", "mean": 0.5, "variance": 0.01, "n": n}

# # === Main analysis function ===
# def analyze_plot(image_path, output_path="plot_analysis.json"):
#     extracted = extract_histogram_from_plot(image_path)
#     if not extracted:
#         print("Failed to extract histogram data from image.")
#         return

#     result = detect_distribution(extracted["heights"])

#     with open(output_path, "w") as f:
#         json.dump(result, f, indent=4)

#     print(f"✅ Analysis complete. Saved to {output_path}")
#     print(json.dumps(result, indent=4))

# # === Run standalone ===
# if __name__ == "__main__":
#     image_path = os.path.join(os.path.dirname(__file__), "../plots/SA_2.png")
#     analyze_plot(image_path)


# import os
# import json
# import numpy as np
# import matplotlib.pyplot as plt
# from PIL import Image
# import google.generativeai as genai
# from dotenv import load_dotenv
# import re

# # --- Load .env file ---
# load_dotenv()

# # --- Configure Gemini ---
# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# # === Utility: extract histogram data from plot ===
# def extract_histogram_from_plot(image_path):
#     """
#     Uses Gemini Vision model to extract both expected (blue) and actual (orange)
#     bar heights from the given plot image.
#     Returns JSON with {'n': int, 'expected': [...], 'actual': [...]}.
#     """
#     model = genai.GenerativeModel("gemini-2.5-flash")

#     prompt = (
#         "You are analyzing a bar chart with two sets of bars for each category:\n"
#         "- Blue bars: Expected counts\n"
#         "- Orange bars: Actual counts\n\n"
#         "Identify how many paired bars (n) exist, and return **valid JSON** in this format:\n"
#         "{'n': <int>, 'expected': [list of blue bar heights], 'actual': [list of orange bar heights]}.\n"
#         "Do NOT include explanations or markdown — only the JSON output."
#     )

#     img = Image.open(image_path)

#     response = model.generate_content([prompt, img])

#     # --- Extract clean JSON from model output ---
#     raw_text = response.text.strip()
#     match = re.search(r"\{[\s\S]*\}", raw_text)
#     if not match:
#         print("⚠️ Gemini did not return valid JSON. Raw output:")
#         print(raw_text)
#         return None

#     try:
#         data = json.loads(match.group(0).replace("'", '"'))
#         return data
#     except Exception as e:
#         print("⚠️ Failed to parse Gemini response:", e)
#         print("Raw text:", raw_text)
#         return None

# # === Distribution detection logic ===
# def detect_distribution(heights):
#     """
#     Detects whether the given bar heights follow a Uniform, Poisson, or Normal-like distribution.
#     """
#     heights = np.array(heights, dtype=float)
#     n = len(heights)
#     x = np.arange(1, n + 1)

#     # Normalize to probabilities
#     probs = heights / np.sum(heights)

#     # --- Uniform check ---
#     if np.std(probs) < 0.05 * np.mean(probs):
#         return {"distribution": "Uniform", "n": n}

#     # --- Poisson check ---
#     mean_est = np.sum(x * probs)
#     var_est = np.sum((x - mean_est) ** 2 * probs)
#     if abs(var_est - mean_est) / mean_est < 0.3:
#         lam = round(mean_est, 2)
#         return {"distribution": "Poisson", "lambda": lam, "n": n}

#     # --- Otherwise Normal ---
#     return {"distribution": "Normal", "mean": 0.5, "variance": 0.01, "n": n}

# # === Main analysis function ===
# def analyze_plot(image_path, output_path="plot_analysis.json"):
#     extracted = extract_histogram_from_plot(image_path)
#     if not extracted:
#         print("❌ Failed to extract histogram data from image.")
#         return

#     print(f" Extracted data from Gemini:\n{json.dumps(extracted, indent=4)}")

#     # Analyze expected vs actual separately
#     result = {
#         "expected": detect_distribution(extracted.get("expected", [])),
#         "actual": detect_distribution(extracted.get("actual", [])),
#     }

#     with open(output_path, "w") as f:
#         json.dump(result, f, indent=4)

#     print(f"\n Analysis complete. Saved to {output_path}")
#     print(json.dumps(result, indent=4))

# # === Run standalone ===
# if __name__ == "__main__":
#     image_path = os.path.join(os.path.dirname(__file__), "../plots/OA_4.png")
#     analyze_plot(image_path)



import os
import json
import numpy as np
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import re

# --- Load .env file ---
load_dotenv()

# --- Configure Gemini ---
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# === Utility: extract histogram data from plot ===
def extract_histogram_from_plot(image_path):
    """
    Uses Gemini Vision model to extract both expected (blue) and actual (orange)
    bar heights from the given plot image.
    Returns JSON with {'attribute': <str>, 'n': <int>, 'data_points': [...]}.
    """
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = (
        "You are analyzing a bar chart with two sets of bars for each category:\n"
        "- Blue bars: Expected counts\n"
        "- Orange bars: Actual counts\n\n"
        "Identify the attribute name (e.g., SA_1), the number of values (n), "
        "and return **valid JSON** in this format:\n"
        "{\"attribute\": \"<str>\", \"n\": <int>, \"data_points\": [list of bar heights]}.\n"
        "Do NOT include explanations or markdown — only the JSON output."
    )

    try:
        img = Image.open(image_path)
        response = model.generate_content([prompt, img])

        raw_text = response.text.strip()
        match = re.search(r"\{[\s\S]*\}", raw_text)
        if not match:
            print(f"⚠️ Gemini did not return valid JSON for {image_path}. Raw output:")
            print(raw_text)
            return None

        # Clean up single quotes → double quotes
        json_str = match.group(0).replace("'", '"')

        data = json.loads(json_str)
        # Basic validation
        if "attribute" not in data or "data_points" not in data:
            print(f"⚠️ Incomplete data returned for {image_path}: {data}")
            return None

        return data

    except Exception as e:
        print(f"❌ Exception during Gemini extraction for {image_path}: {e}")
        return None

# === Distribution detection logic ===
def detect_distribution(data_points):
    """
    Detects whether the given bar heights follow a Uniform, Poisson, or Normal-like distribution.
    """
    heights = np.array(data_points, dtype=float)
    n = len(heights)
    x = np.arange(1, n + 1)

    # Normalize to probabilities
    probs = heights / np.sum(heights)

    # --- Uniform check ---
    if np.std(probs) < 0.05 * np.mean(probs):
        return {"distribution": "Uniform", "n": n}

    # --- Poisson check ---
    mean_est = np.sum(x * probs)
    var_est = np.sum((x - mean_est) ** 2 * probs)
    if abs(var_est - mean_est) / mean_est < 0.3:
        lam = round(mean_est, 2)
        return {"distribution": "Poisson", "lambda": lam, "n": n}

    # --- Otherwise Normal ---
    return {
        "distribution": "Normal",
        "mean": 0.5,
        "variance": 0.01,
        "n": n
    }

# === Main analysis function ===
def analyze_plot(image_path, preprocessing_data, final_output_data):
    extracted = extract_histogram_from_plot(image_path)
    if not extracted:
        print(f"❌ Failed to extract histogram data from {image_path}. Skipping.")
        return

    attribute = extracted.get("attribute")
    data_points = extracted.get("data_points", [])
    n = extracted.get("n")

    # Add to preprocessing JSON
    preprocessing_data[attribute] = {
        "n": n,
        "data_points": data_points
    }

    # Detect distribution and add to final output JSON
    final_output_data[attribute] = detect_distribution(data_points)

    # Print processing details to the terminal
    print(f"\n✅ Processed Image: {image_path}")
    print(f"   Attribute: {attribute}")
    print(f"   Data Points: {data_points}")
    print(f"   Detected Distribution: {final_output_data[attribute]}")
