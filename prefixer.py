import os
import re

def rename_drum_samples(directory):
    # Define keyword mappings
    drum_mappings = {
        'kick': ['kick', 'bd', 'bassdrum'],
        'snare': ['snare', 'sd'],
        'clap': ['clap', 'cp'],
        'cym': ['ohat', 'open hat', 'oh', 'openhihat', 'cym', 'ride', 'crash', 'cx', 'cy'],
        'hh': ['hh', 'hat', 'chat', 'closed hat', 'ch', 'closedhihat'],
        'tom': ['tom', 'lt', 'mt', 'ht'],
        'perc': ['perc', 'percussion', 'clave', 'claves', 'cl', 'maracas', 'ma', 'shaker', 'cowbell', 'cb', 'bongo', 'conga', 'timbale', 'woodblock', 'triangle', 'guiro', 'vibraslap', 'agogô', 'hc'],
        'rim': ['rim', 'rimshot', 'rs'],
    }
    
    # Supported audio file extensions
    audio_extensions = {'.wav', '.mp3', '.flac', '.aiff', '.ogg', '.m4a'}

    # Function to determine drum type
    def get_prefix(filename):
        lowercase_name = filename.lower()
        for prefix, keywords in drum_mappings.items():
            for kw in keywords:
                if re.search(rf'(?<![a-zA-Z0-9]){kw}(?![a-zA-Z0-9])', lowercase_name):
                    return f"{prefix}_"
        return None
    
    # Recursively process files in directory and subdirectories
    def process_directory(directory):
        for root, _, files in os.walk(directory):
            folder_name = os.path.basename(root).replace('.', '')  # Strip periods from folder name
            append_folder = input(f"Would you like to append the folder name '{folder_name}' to each file? (y/N): ").strip().lower() == 'y'
            
            for filename in files:
                if not any(filename.lower().endswith(ext) for ext in audio_extensions):
                    continue  # Skip non-audio files
                
                filepath = os.path.join(root, filename)
                prefix = get_prefix(filename)
                
                name, ext = os.path.splitext(filename)
                name = name.replace('.', '')  # Strip periods from name before the extension
                
                if prefix and not filename.lower().startswith(tuple(p + "_" for p in drum_mappings.keys())):
                    new_filename = prefix + name
                elif not prefix:  # Ask to prepend 'other_' if no match is found
                    user_input = input(f"No drum mapping match for '{filename}'. Do you want to prefix it with 'other_'? (y/N): ").strip().lower()
                    if user_input == 'y':
                        new_filename = "other_" + name
                    else:
                        new_filename = name
                else:
                    new_filename = name
                
                if append_folder and not name.endswith(f"_{folder_name}"):
                    new_filename += f"_{folder_name}"
                
                new_filename += ext
                new_filepath = os.path.join(root, new_filename)
                
                # Only rename if the filename has changed
                if new_filename != filename:
                    os.rename(filepath, new_filepath)
                    print(f"Renamed: {filename} -> {new_filename}")
    
    process_directory(directory)

if __name__ == "__main__":
    directory = input("Enter the directory path: ").strip()
    if os.path.isdir(directory):
        rename_drum_samples(directory)
    else:
        print("Invalid directory path.")

