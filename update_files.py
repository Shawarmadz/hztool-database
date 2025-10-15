import os
import json

# --- الإعدادات ---
# ==============================================================================
# المسار الذي سيبدأ منه السكريبت البحث (النقطة تعني المجلد الحالي)
ROOT_DIRECTORY = "." 

# قائمة بالامتدادات التي تريد تضمينها في ملف الـ JSON
# يمكنك إضافة أي امتدادات أخرى هنا
ALLOWED_EXTENSIONS = [
    ".bin", ".auth", ".txt", ".link", ".img", ".xml", ".zip", ".rar"
]

# قائمة بأسماء الملفات أو المجلدات التي تريد تجاهلها
# تجاهل السكريبت نفسه وملف الإخراج وملفات Git
EXCLUDE_ITEMS = [
    ".git", 
    ".github",
    "update_files.py", 
    "files.json",
    "README.md"
]

# اسم ملف الإخراج النهائي
OUTPUT_JSON_FILE = "files.json"
# ==============================================================================


# --- الكود ---
all_files_info = []

print(f"Starting scan in '{os.path.abspath(ROOT_DIRECTORY)}'...")
print(f"Looking for file types: {', '.join(ALLOWED_EXTENSIONS)}")

# os.walk يقوم بالمرور على كل المجلدات والملفات بشكل متكرر
for root, dirs, files in os.walk(ROOT_DIRECTORY):
    # إزالة المجلدات غير المرغوب فيها من البحث لتسريع العملية
    dirs[:] = [d for d in dirs if d not in EXCLUDE_ITEMS]
    
    for filename in files:
        # التحقق إذا كان الملف أو المجلد الذي ينتمي إليه ضمن قائمة التجاهل
        if filename in EXCLUDE_ITEMS:
            continue
            
        # التحقق مما إذا كان امتداد الملف ضمن الامتدادات المسموح بها
        # نستخدم lower() لضمان تطابق الامتدادات بغض النظر عن حالتها (Bin أو bin)
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in ALLOWED_EXTENSIONS:
            
            # بناء المسار الكامل والنسبي
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, start=ROOT_DIRECTORY).replace("\\", "/")
            
            # الحصول على حجم الملف بالكيلوبايت
            try:
                file_size_kb = round(os.path.getsize(full_path) / 1024, 2)
            except FileNotFoundError:
                print(f"Warning: Could not find file {full_path} to get size. Skipping.")
                continue

            # استخراج اسم المجلد الأب (اسم الهاتف أو الموديل)
            parent_folder = os.path.basename(os.path.dirname(full_path))
            
            # إضافة المعلومات إلى القائمة
            file_info = {
                "path": relative_path,
                "filename": filename,
                "model_folder": parent_folder,
                "size_kb": file_size_kb,
                "extension": file_ext
            }
            all_files_info.append(file_info)
            print(f"Added: {relative_path}")

# فرز القائمة أبجديًا حسب المسار لتكون منظمة
all_files_info.sort(key=lambda x: x['path'])

# كتابة البيانات المجمعة في ملف JSON
try:
    with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(all_files_info, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Success! Updated '{OUTPUT_JSON_FILE}' with {len(all_files_info)} files.")
except Exception as e:
    print(f"\n❌ Error! Failed to write to '{OUTPUT_JSON_FILE}': {e}")