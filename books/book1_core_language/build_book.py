import os
import subprocess
import glob

def build_book():
    print("Building Book 1 with 100% accurate codebase details...")
    
    # Get all markdown parts in order
    md_files = sorted(glob.glob("part*.md"))
    
    if not md_files:
        print("No markdown files found!")
        return
        
    master_md = "book1_master.md"
    
    # Concatenate all parts
    with open(master_md, "w", encoding="utf-8") as outfile:
        for f in md_files:
            with open(f, "r", encoding="utf-8") as infile:
                outfile.write(infile.read())
                outfile.write("\n\n---\n\n")  # Page break separator
                
    print(f"Combined {len(md_files)} files into {master_md}")
    
    # Run md-to-pdf
    print("Generating PDF via md-to-pdf...")
    pdf_out = "book1_enlang_core_language.pdf"
    
    cmd = f'cmd /c "npx md-to-pdf {master_md}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"Successfully generated {pdf_out}!")
        if os.path.exists("book1_master.pdf"):
            os.rename("book1_master.pdf", pdf_out)
    else:
        print("Failed to generate PDF.")
        print(result.stdout)
        print(result.stderr)

if __name__ == "__main__":
    build_book()
