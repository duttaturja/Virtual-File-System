import os
import time


class MetadataManager:
    def __init__(self, root_directory="C:\\Users\\Turja Dutta\\OneDrive\\Desktop\\Virtual File System\\root_file_dir"):
        self.root_directory = root_directory
        self.metadata_cache = self.index_files()

    def index_files(self):
        """Indexes all files in the root directory and caches metadata."""
        metadata = {}
        for root, _, files in os.walk(self.root_directory):
            for file in files:
                file_path = os.path.join(root, file)
                metadata[file_path] = self.get_metadata(file_path)
        return metadata

    def get_metadata(self, file_path):
        """Gets metadata for a single file."""
        try:
            stats = os.stat(file_path)
            return {
                "size": stats.st_size,
                "creation_time": time.ctime(stats.st_ctime),
                "modification_time": time.ctime(stats.st_mtime),
            }
        except Exception as e:
            return {"error": str(e)}

    def search_files(self, query, attribute="name"):
        """Searches files based on a query and attribute."""
        results = []
        for file_path, meta in self.metadata_cache.items():
            if attribute == "name" and query.lower() in os.path.basename(file_path).lower():
                results.append((file_path, meta))
            elif attribute in meta and query.lower() in str(meta[attribute]).lower():
                results.append((file_path, meta))
        return results
