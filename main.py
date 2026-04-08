import os
import tomllib
import json
from src.batch_runner import process_directory

def load_config():
    config_path = "config.toml"
    if os.path.exists(config_path):
        with open(config_path, "rb") as f:
            return tomllib.load(f)
    return {}

def main():
    config = load_config()
    
    paths_conf = config.get("paths", {})
    input_folder = paths_conf.get("input_folder", ".")
    output_file = paths_conf.get("output_file", "output.jsonl")
    
    llm_conf = config.get("llm", {})
    if "base_url" in llm_conf:
        os.environ["OPENAI_BASE_URL"] = llm_conf["base_url"]
    if "api_key" in llm_conf:
        os.environ["OPENAI_API_KEY"] = llm_conf["api_key"]
    if "model" in llm_conf:
        os.environ["LLM_MODEL"] = llm_conf["model"]

    processing_conf = config.get("processing", {})
    page_settings = processing_conf.get("pages", None)

    print(f"Starting PDF OCR batch extraction on folder: '{input_folder}'...")
    results = process_directory(input_folder, page_settings)
    
    if results:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        with open(output_file, "w", encoding="utf-8") as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"Done. Processed {len(results)} items. Saved to {output_file}.")

if __name__ == "__main__":
    main()
