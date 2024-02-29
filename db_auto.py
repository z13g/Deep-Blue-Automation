import subprocess
import os

#Full path for folder that contains all the .evtx files
logs_path = r'.\Logs'
main_file  = logs_path.split('\\')[-1]
#Deep blue powershell script
deepblue_script_path = r'D:\DeepBlueCLI\DeepBlue.ps1'
output_path = fr'D:\DeepBlueCLI\{main_file}_db_output'

os.makedirs(output_path, exist_ok=True)

script_dir = os.path.dirname(deepblue_script_path)

no_events_keywords = ["No events were found that match the specified selection criteria", "Logic error"]

# Iterer over hver fil i mappen
for file in os.listdir(logs_path):
    if file.endswith(".evtx"):
        full_file_path = os.path.join(logs_path, file)
        output_file_path = os.path.join(output_path, file + "_output.txt")
        print(f"Using Deep Blue on: {file}", end='\r', flush=True)
        
        command = f'cd "{script_dir}"; & "{deepblue_script_path}" "{full_file_path}"'
        
        result = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-Command", command], capture_output=True, text=True, shell=True)
        
        if any(keyword in result.stdout for keyword in no_events_keywords):
            continue

        print(f"Found something in {file}")
        with open(output_file_path, "w") as output_file:
            output_file.write(result.stdout)
            if result.stderr:
                output_file.write("\nErrors:\n")
                output_file.write(result.stderr)

print("Analyze complete. Check output-files in:", output_path)
