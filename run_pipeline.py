import subprocess
import sys
import os

def run_script(script_name):
    print(f"\n[Pipeline] Running {script_name}...")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[Success] {script_name} executed successfully!")
        print(result.stdout)
    else:
        print(f"[Error] Failed to execute {script_name}.")
        print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    print("==========================================")
    print("  Starting Automated ETL Pipeline Orchestration ")
    print("==========================================")
    
    # Step 1: Run the main ETL script
    run_script("real data.py")
    
    # Step 2: Run the data validation script
    if os.path.exists("validate_data.py"):
        run_script("validate_data.py")
    else:
        print("[Warning] validate_data.py not found, skipping validation step.")
        
    print("==========================================")
    print("  ETL Pipeline & Validation Completed!    ")
    print("==========================================")
