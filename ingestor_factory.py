from pathlib import Path
from ingestors.edgar_ingestor import EDGARIngestor


class IngestorFactory():
    def __init__(self, root_path, embeddings):
        self.root_path = root_path
        self.embeddings = embeddings

    def parse_props(self, file_path, root_path):
        props = file_path.relative_to(root_path).parts[:-1]  # Exclude filename
        data = {}
        data["file_path"] = file_path
        data["props"] = {}
        for i, prop in enumerate(props, start=1):
            data["props"][f"prop_{i}"] = prop
        data["props"]["file_name"] = file_path.parts[-1]
        return data

    def build_files_info(self):
        files_info = []
        root_path = Path(self.root_path)
        for file_path in root_path.glob('**/*'):
            if file_path.is_file():
                files_info.append(self.parse_props(file_path, root_path))
        return files_info

    def get_ingestors(self):
        files_info = self.build_files_info()
        print(files_info)
        ingestors = []
        for file_info in files_info:
            if file_info["props"]["prop_1"] == "EDGAR":
                ingestors.append(EDGARIngestor(
                    file_info["file_path"], file_info["props"], self.embeddings))
            # Add other ingestors here
            else:
                raise ValueError(
                    f"Unsupported db type: {file_info['props']['prop_1']}")
        return ingestors
