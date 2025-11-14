# How to Add Your Knowledge Base

## Quick Start

1. **Copy your PDF files** to the `data/knowledge/` folder
2. **Restart the application**
3. **Done!** Your knowledge is now available to the AI

## Detailed Instructions

### Step 1: Prepare Your Files

Supported formats:
- ✅ PDF files (`.pdf`) - **Recommended**
- ✅ Text files (`.txt`)
- ✅ Markdown files (`.md`)

### Step 2: Copy Files to Knowledge Folder

Navigate to:
```
soya-copilot/data/knowledge/
```

Copy your files here:
```
data/knowledge/
├── soybean_guide.pdf
├── farming_manual.pdf
└── disease_handbook.pdf
```

Or organize in subfolders:
```
data/knowledge/
├── farming/
│   ├── planting.pdf
│   └── harvesting.pdf
├── diseases/
│   └── disease_guide.pdf
└── climate/
    └── weather_info.pdf
```

### Step 3: Install PDF Support (if needed)

If you haven't already:
```bash
pip install pypdf2
```

### Step 4: Restart the Application

Stop the running application (Ctrl+C) and restart:
```bash
python main.py
```

Or use the startup script:
```bash
start_all.bat
```

### Step 5: Verify Loading

When the app starts, you should see:
```
✅ Loaded 150 knowledge items from files
   📄 Loaded PDF: soybean_guide.pdf (45 pages)
   📄 Loaded PDF: farming_manual.pdf (32 pages)
```

## Tips

### For Best Results:

1. **Use clear, well-formatted PDFs**
   - Avoid scanned images (use OCR first)
   - Text-based PDFs work best

2. **Break large documents into sections**
   - Smaller files load faster
   - Better retrieval accuracy

3. **Name files descriptively**
   - `soybean_planting_guide.pdf` ✅
   - `document1.pdf` ❌

4. **Remove unnecessary files**
   - Only include relevant agricultural content
   - Remove duplicates

### File Size Recommendations:

- ✅ Small files (< 5 MB): Fast loading
- ⚠️ Medium files (5-20 MB): May take a minute
- ❌ Large files (> 20 MB): Consider splitting

## Troubleshooting

### PDFs Not Loading?

**Problem**: "PyPDF2 not installed"
```bash
pip install pypdf2
```

**Problem**: "Error loading PDF"
- Check if PDF is password-protected
- Try converting to text first
- Ensure PDF is not corrupted

### Knowledge Not Being Used?

1. Check the startup logs for "Loaded X knowledge items"
2. Verify files are in `data/knowledge/` folder
3. Restart the application
4. Check file permissions

### Slow Loading?

- Reduce number of files
- Split large PDFs into smaller ones
- Remove unnecessary content

## Advanced: Custom Knowledge Format

### Text Files (.txt)

Create simple text files:
```
Soybean Planting Guide

Best time to plant: November-December
Soil temperature: At least 15°C
Spacing: 5-7 cm between plants
```

### Markdown Files (.md)

Use markdown formatting:
```markdown
# Soybean Diseases

## Bacterial Blight
- Symptoms: Brown spots with yellow halos
- Treatment: Copper-based fungicides
```

## Testing Your Knowledge

After adding files, test if the AI can access them:

1. Start the application
2. Ask: "What does my knowledge base say about planting?"
3. The AI should reference your uploaded content

## Need Help?

- Check `data/knowledge/README.md` for more details
- Review the startup logs for errors
- Ensure all dependencies are installed

---

**Remember**: The more relevant knowledge you add, the better the AI's responses will be!
