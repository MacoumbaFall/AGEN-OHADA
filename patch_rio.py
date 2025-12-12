import os
import sys

target_file = r"C:\Users\Macoumba\AppData\Local\Programs\Python\Python314\Lib\site-packages\rio\dataclass.py"

if not os.path.exists(target_file):
    print(f"File not found: {target_file}")
    # Try to find it via site-packages of current python
    import rio.dataclass
    target_file = rio.dataclass.__file__
    print(f"Found via import: {target_file}")

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# We need to add 'doc=None' to super().__init__ call in RioField
# The code looks like:
#         super().__init__(
#             default=default,
#             default_factory=default_factory,
#             init=init,
#             repr=repr,
#             hash=hash,
#             compare=compare,
#             metadata=metadata,
#             kw_only=kw_only,  # type: ignore
#         )

search_str = "kw_only=kw_only,  # type: ignore"
replace_str = "kw_only=kw_only, doc=None, # type: ignore"

if search_str in content:
    new_content = content.replace(search_str, replace_str)
    
    # Also verify if 'doc' is already there to avoid double patching
    if "doc=None" not in content:
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully patched rio/dataclass.py")
    else:
        print("Patch already applied.")
else:
    print("Could not find the target string to patch.")
