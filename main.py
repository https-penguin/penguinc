#!/usr/bin/env python3
import os
import re
import shutil
import sys
from pathlib import Path
from collections import defaultdict
import colorama
from colorama import Fore, Style
from termcolor import colored
import stat
import time

# =========================== AUTH SYSTEM ===========================
VALID_KEY = "@penguin.sh"

def loading_animation(text, duration=2):
    import itertools
    spinner = itertools.cycle(['|', '/', '-', '\\'])
    end_time = time.time() + duration
    while time.time() < end_time:
        sys.stdout.write(f"\r{text} " + next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
    print("\r" + text + " Done!      ")

def auth_screen():
    clear_screen()

    ui = """

╔═══════════════════════════════════════════════════════════════════════════════════════╗

                               __ ____  ___   _____    __
                              / //_/ / / / | / /   |  / /
                             / ,< / / / /  |/ / /| | / /
                            / /| / /_/ / /|  / ___ |/ /___
                           /_/ |_\\____/_/ |_/_/  |_/_____/

                                      @penguin

╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═════════════════════════════════════════════════════════╗
           ║                 : AUTHENTICATION REQUIRED               ║
           ║          ENTER AUTHORIZATION KEY TO CONTINUE            ║
           ╚═════════════════════════════════════════════════════════╝

# Initializing module...
# Loading secure environment...
# Verifying access permissions...

"""

    for line in ui.splitlines():
        if "# Initializing" in line or "# Loading" in line or "# Verifying" in line:
            print(Fore.BLUE + line)
        elif "@penguin" in line:
            print(Fore.BLUE + line)
        else:
            print(Fore.WHITE + line)

    key = input(Fore.CYAN + "\nENTER SECURITY KEY = ").strip()

    print()
    loading_animation("📰 vrifing key")

    if key == VALID_KEY:
        print(Fore.GREEN + "\n👁️‍🗨️📰 WELLCOM ")
        time.sleep(1)
        return True
    else:
        print(Fore.RED + "\n☢️ INVALID KEY!   [@ ask owner for key]")
        time.sleep(2)
        return False
# ================================================================

colorama.init(autoreset=True)

# =========================== DIRECTORY PATHS ===========================
BASE_DIR = os.getcwd()
MINI_ICON_DIR = os.path.join(BASE_DIR, "MINI_ICON")
INPUT_DIR = os.path.join(MINI_ICON_DIR, "INPUT")
OUTPUT_DIR = os.path.join(MINI_ICON_DIR, "OUTPUT")
TXTS_DIR = os.path.join(MINI_ICON_DIR, "TXTS")
MODSKIN_FILE = os.path.join(BASE_DIR, "modskin.txt")
CHANGELOG_PATH = os.path.join(BASE_DIR, "changelog.txt")
NULL_TXT_PATH = os.path.join(TXTS_DIR, "null.txt")
NULLED_TXT_PATH = os.path.join(BASE_DIR, "nulled.txt")
ALL_TXT_PATH = os.path.join(TXTS_DIR, "ALL.txt")
INDEX_FILE_PATH = os.path.join(TXTS_DIR, "index.txt")

# AUTO_THEME paths
AUTO_THEME_BASE = os.path.join(BASE_DIR, "AUTO_THEME")
AUTO_THEME_FILES = os.path.join(AUTO_THEME_BASE, "FILES")
AUTO_THEME_RESULT = os.path.join(AUTO_THEME_BASE, "MODIFIED")
AUTO_THEME_TXT = os.path.join(AUTO_THEME_BASE, "TXT")
LOBBY_FILE = os.path.join(AUTO_THEME_TXT, "lobby.txt")

# HIT EFFECT and LOOTCRATES paths
HIT_EFFECT_DIR = os.path.join(BASE_DIR, "HIT EFFECT")
LOOTCRATES_DIR = os.path.join(BASE_DIR, "LOOTCRATES")
HIT_ORIG = os.path.join(HIT_EFFECT_DIR, "org")
HIT_MODIFIED = os.path.join(HIT_EFFECT_DIR, "modified")
LOOT_ORIG = os.path.join(LOOTCRATES_DIR, "org")
LOOT_MODIFIED = os.path.join(LOOTCRATES_DIR, "modified")
HIT_TXT_PATH = os.path.join(BASE_DIR, "hit.txt")

# Global list to track changes
changelog_entries = []
modified_blocks_map = {} # {file_path: set(block_indices)}
BLOCK_SIZE = 65536

# =========================== HELPER FUNCTIONS ===========================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def color_cycled_text(text):
    colors = ['white', 'white', 'white', 'white', 'white', 'white']
    for i, line in enumerate(text.splitlines()):
        colored_line = "".join(colored(char, colors[j % len(colors)], attrs=['bold']) for j, char in enumerate(line))
        print(colored_line)

def display_tool_name():
    clear_screen()
    tool_name = """

╔═══════════════════════════════════════════════════════════════════════════════════════╗

                               __ ____  ___   _____    __
                              / //_/ / / / | / /   |  / /
                             / ,< / / / /  |/ / /| | / /
                            / /| / /_/ / /|  / ___ |/ /___
                           /_/ |_\____/_/ |_/_/  |_/_____/

                                      @penguin

╚═══════════════════════════════════════════════════════════════════════════════════════╝

           ╔═════════════════════════════════════════════════════════╗
           ║                 :        @penguin                       ║
           ║            4.3.0 MODDING BGMI AUTOMATED TOOL 👁️‍🗨️         ║
           ╚═════════════════════════════════════════════════════════╝
           
           ╔═══════════════════════╗      ╔═══════════════════════════════╗
           ║ 1. 👁️‍🗨️ MOD SKIN        ║      ║ 2. 👁️‍🗨️ DEATH BOX + HIT EFFECT. ║
           ╚═══════════════════════╝      ╚═══════════════════════════════╝
           
           ╔═══════════════════════╗      ╔════════════════════════════════╗
           ║ 3. 👁️‍🗨️ ADD THEME       ║      ║  4.✖️ EXIT                      ║
           ╚═══════════════════════╝      ╚════════════════════════════════╝
           
automated skin bgmi tool 📰
    """

    for line in tool_name.splitlines():
        if "║" in line:
            print(Fore.WHITE + line.replace("MOD SKIN", Fore.BLUE + "MOD SKIN" + Fore.WHITE)
                                .replace("DEATH BOX + HIT EFFECT", Fore.BLUE + "DEATH BOX + HIT EFFECT" + Fore.WHITE)
                                .replace("ADD THEME", Fore.BLUE + "ADD THEME" + Fore.WHITE)
                                .replace("EXIT", Fore.BLUE + "EXIT" + Fore.WHITE)
                                .replace("@penguin", Fore.BLUE + "@penguin" + Fore.WHITE))
        else:
            print(Fore.WHITE + line)

def find_all_occurrences(data, sub):
    """Find all occurrences of a byte sequence in a bytes object."""
    positions = []
    start = 0
    while True:
        pos = data.find(sub, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions

def mark_block_as_modified(file_path, byte_offset):
    """Mark the block containing byte_offset AND its neighbors as modified."""
    block_idx = byte_offset // BLOCK_SIZE
    if file_path not in modified_blocks_map:
        modified_blocks_map[file_path] = set()
    
    # Mark current, previous (if valid), and next
    modified_blocks_map[file_path].add(block_idx)
    if block_idx > 0:
        modified_blocks_map[file_path].add(block_idx - 1)
    # Upper bound checked during processing
    modified_blocks_map[file_path].add(block_idx + 1)

def load_all_skins_data():
    """Load all skin data from ALL.txt into a comprehensive lookup dictionary."""
    skins_by_id = {} # {id: {'hex': hex, 'name': name}}
    
    if not os.path.exists(ALL_TXT_PATH):
        print(f"{Fore.RED}🚨 ALL.txt not found at {ALL_TXT_PATH}")
        return skins_by_id
    
    with open(ALL_TXT_PATH, "r", encoding="utf-8", errors='ignore') as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 2:
                skin_id = parts[0].strip()
                hex_val = parts[1].strip().lower()
                skin_name = parts[2].strip() if len(parts) >= 3 else ""
                skins_by_id[skin_id] = {'hex': hex_val, 'name': skin_name}
    
    return skins_by_id

def load_index_data():
    """Load index data from index.txt (format: ID | HEX | NAME | INDEX_HEX)."""
    index_data = {}
    if not os.path.exists(INDEX_FILE_PATH):
        print(f"{Fore.YELLOW}⚠️ index.txt not found at {INDEX_FILE_PATH}")
        return index_data
    
    with open(INDEX_FILE_PATH, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) >= 4:
                name = parts[2].strip()  # Skin name is in 3rd column
                index_hex = parts[3].strip().lower()  # Index hex is in 4th column
                index_data.setdefault(name, []).append(index_hex)
    return index_data

def load_modskin_pairs():
    """Load ID pairs from modskin.txt."""
    pairs = []
    if not os.path.exists(MODSKIN_FILE):
        print(f"{Fore.RED}🚨 modskin.txt not found at {MODSKIN_FILE}")
        return pairs
    
    with open(MODSKIN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Expected format: ID1,ID2 or ID1 ID2 or ID1->ID2
            parts = re.split(r'[,\s\->]+', line)
            if len(parts) >= 2:
                pairs.append((parts[0].strip(), parts[1].strip()))
    return pairs

# =========================== CHANGELOG ===========================
def write_changelog():
    """Write accumulated changes to changelog.txt."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(CHANGELOG_PATH, "w", encoding="utf-8") as f:
            f.write(f"{idx}. ID PAIR: {entry['id_pair']}\n")
            f.write(f"FILE NAME: {entry['file_name']}\n")
            f.write(f"Source Item: {entry['source_item']}\n")
            f.write(f"Target Item: {entry['target_item']}\n")
            f.write(f"CHANGED HEX FROM: {entry['source_hex']} TO: {entry['target_hex']}\n")
            if entry.get('index_occurrences', 0) > 0:
                f.write(f"INDEX CHANGED FROM: {entry['source_index']} TO: {entry['target_index']} ({entry['index_occurrences']} occurrence(s))\n")
            elif entry.get('index_failure_reason'):
                f.write(f"Index replacement note: {entry['index_failure_reason']}\n")
            f.write("==============================\n\n")

# =========================== STEP 1: COPY FILES TO OUTPUT ===========================
def remove_readonly(func, path, excinfo):
    """Handler for shutil.rmtree to remove read-only files."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def copy_files_to_output():
    """Copy all files from INPUT to OUTPUT with robust retry logic."""
    print(f"\n{Fore.CYAN}📁 Step 1: Copying files from INPUT to OUTPUT...")
    
    if not os.path.exists(INPUT_DIR):
        print(f"{Fore.RED}🚨 INPUT directory not found: {INPUT_DIR}")
        return False
    
    # Clear output directory if it exists (Robust removal)
    if os.path.exists(OUTPUT_DIR):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                shutil.rmtree(OUTPUT_DIR, onerror=remove_readonly)
                break
            except PermissionError:
                if attempt < max_retries - 1:
                    print(f"{Fore.YELLOW}⚠️ OUTPUT folder is locked by another process. Retrying in 1s...")
                    time.sleep(1)
                else:
                    print(f"\n{Fore.RED}❌ ERROR: Cannot delete OUTPUT folder. It is open in another program.")
                    print(f"{Fore.RED}👉 Please close any file manager or editor opening {OUTPUT_DIR}")
                    input(f"{Fore.YELLOW}Press Enter after closing to try again...{Style.RESET_ALL}")
                    try:
                        shutil.rmtree(OUTPUT_DIR, onerror=remove_readonly)
                    except Exception as e:
                        print(f"{Fore.RED}❌ Failed to clean OUTPUT: {e}")
                        return False
            except Exception as e:
                print(f"{Fore.RED}❌ Error cleaning OUTPUT: {e}")
                return False
    
    # Copy entire directory structure
    try:
        shutil.copytree(INPUT_DIR, OUTPUT_DIR)
        file_count = sum(len(files) for _, _, files in os.walk(OUTPUT_DIR))
        print(f"{Fore.GREEN}✅ Copied {file_count} files to OUTPUT directory")
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error copying files: {e}")
        return False

# =========================== STEP 2: MOD SKIN ===========================
def process_mod_skin():
    """Process mod skin replacements using modskin.txt pairs."""
    global modified_blocks_map
    modified_blocks_map = {} # Reset
    
    print(f"\n{Fore.CYAN}🔧 Step 2: Processing Mod Skin replacements...")
    
    # Ask for mode
    print(f"{Fore.CYAN}Select Mod Skin Mode:")
    print(f"{Fore.YELLOW}1. Replace (One-Way): Apply ID1 onto ID2")
    print(f"{Fore.YELLOW}2. Swap (Two-Way): Swap ID1 and ID2 with each other")
    
    while True:
        mode_choice = input(f"{Fore.CYAN}Enter choice (1 or 2): ").strip()
        if mode_choice in ['1', '2']:
            break
        print(f"{Fore.RED}❌ Invalid choice.")
        
    is_swap = (mode_choice == '2')
    mode_str = "SWAP (Two-Way)" if is_swap else "REPLACE (One-Way)"
    print(f"{Fore.GREEN}Mode: {mode_str}")
    
    # Load data
    skins_data = load_all_skins_data()
    index_data = load_index_data()
    id_pairs = load_modskin_pairs()
    
    if not id_pairs:
        print(f"{Fore.YELLOW}⚠️ No ID pairs found in modskin.txt")
        return
    
    print(f"{Fore.GREEN}Found {len(id_pairs)} ID pairs to process")
    
    # RESOLVE ALL PAIRS ONCE (O(1) lookups)
    resolved_ops = []
    missing_ids = set()
    
    for s_id, t_id in id_pairs:
        if s_id not in skins_data:
            missing_ids.add(s_id)
            continue
        if t_id not in skins_data:
            missing_ids.add(t_id)
            continue
            
        s_hex = skins_data[s_id]['hex']
        s_name = skins_data[s_id]['name']
        t_hex = skins_data[t_id]['hex']
        t_name = skins_data[t_id]['name']
        
        # Op 1: ID1 -> ID2 (Replace ID2's hex with ID1's hex)
        resolved_ops.append({
            'search_hex': t_hex, 'replace_hex': s_hex,
            'search_name': t_name, 'replace_name': s_name,
            'label': f"{s_id} -> {t_id}",
            'op_type': "REPLACE"
        })
        
        # Op 2: ID2 -> ID1 (Only if Swap)
        if is_swap:
            resolved_ops.append({
                'search_hex': s_hex, 'replace_hex': t_hex,
                'search_name': s_name, 'replace_name': t_name,
                'label': f"{t_id} -> {s_id}",
                'op_type': "SWAP CHECK"
            })
            
    if missing_ids:
        print(f"{Fore.YELLOW}⚠️ Warning: {len(missing_ids)} IDs not found in ALL.txt: {', '.join(sorted(missing_ids))}")
        
    if not resolved_ops:
        print(f"{Fore.RED}❌ Empty operational queue. Nothing to process.")
        return

    modified_files = 0
    
    # Process each file in OUTPUT directory
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            
            if file_name.lower().endswith('.txt'):
                continue
            
            try:
                with open(file_path, 'rb') as f:
                    content_bytes = f.read()
            except Exception as e:
                print(f"{Fore.RED}❌ Error reading {file_name}: {e}")
                continue
            
            hex_data = content_bytes.hex()
            file_modified = False
            
            # Use pre-resolved operations
            for op in resolved_ops:
                s_hex = op['search_hex']
                r_hex = op['replace_hex']
                s_name = op['search_name']
                r_name = op['replace_name']
                
                # Check if search hex is even present (optimization)
                if s_hex not in hex_data:
                    continue
                
                occ = hex_data.count(s_hex)
                if occ >= 2:
                    first_pos = hex_data.find(s_hex)
                    second_pos = hex_data.find(s_hex, first_pos + len(s_hex))
                    
                    if second_pos != -1:
                        # Replace second occurrence
                        hex_data = hex_data[:second_pos] + r_hex + hex_data[second_pos+len(s_hex):]
                        file_modified = True
                        mark_block_as_modified(file_path, second_pos // 2)
                        
                        # Index replacement logic
                        idx_occ = 0
                        idx_reason = ""
                        mod_idx_from = "N/A"
                        mod_idx_to = "N/A"
                        
                        if s_name in index_data and r_name in index_data:
                            search_candidates = index_data[s_name]
                            replacement_index = index_data[r_name][0]
                            
                            window_start = max(0, first_pos - 60)
                            window = hex_data[window_start:first_pos]
                            
                            found = False
                            for candidate in search_candidates:
                                if candidate in window:
                                    mod_idx_from = candidate
                                    mod_idx_to = replacement_index
                                    
                                    window_replaced = window.replace(candidate, replacement_index, 1)
                                    local_idx = window.find(candidate)
                                    real_idx = window_start + local_idx
                                    
                                    hex_data = hex_data[:window_start] + window_replaced + hex_data[first_pos:]
                                    idx_occ = 1
                                    found = True
                                    mark_block_as_modified(file_path, real_idx // 2)
                                    break
                            if not found:
                                idx_reason = "Index hex not found in window"
                        else:
                            idx_reason = "Index names missing"
                        
                        # Log
                        rel_path = os.path.relpath(file_path, OUTPUT_DIR)
                        changelog_entries.append({
                            'id_pair': f"{op['label']} ({op['op_type']})",
                            'file_name': rel_path,
                            'source_item': f"{s_name} [Found]",
                            'target_item': f"{r_name} [Applied]",
                            'source_hex': s_hex,
                            'target_hex': r_hex,
                            'source_index': mod_idx_from,
                            'target_index': mod_idx_to,
                            'index_occurrences': idx_occ,
                            'index_failure_reason': idx_reason
                        })
            
            if file_modified:
                try:
                    with open(file_path, 'wb') as f:
                        f.write(bytes.fromhex(hex_data))
                    modified_files += 1
                except Exception as e:
                    print(f"{Fore.RED}❌ Error writing {file_name}: {e}")
    
    print(f"{Fore.GREEN}✅ Modified {modified_files} files")

# =========================== STEP 3: SIZE FIX (NULLING) ===========================
def build_pattern_groups(hex_list):
    """Group patterns by byte-length for faster scanning."""
    groups = {}
    for hx in hex_list:
        try:
            b = bytes.fromhex(hx)
        except ValueError:
            continue
        if not b:
            continue
        groups.setdefault(len(b), set()).add(b)
    return groups

def null_bytes_in_file(file_path, pattern_groups, dirty_blocks, target_counts={2}):
    """
    Replace patterns with zero-bytes based on occurrence counts.
    target_counts: a set of integers (e.g., {1, 2, 3}) representing how many 
                  times a hex must appear in a block to be nulled.
    Returns count of replacements.
    """
    try:
        data = Path(file_path).read_bytes()
    except:
        return 0
    
    ba = bytearray(data)
    total_hits = 0
    modified = False
    
    file_size = len(ba)
    
    # Process each dirty block
    for block_idx in dirty_blocks:
        start_offset = block_idx * BLOCK_SIZE
        if start_offset >= file_size:
            continue
            
        end_offset = min(start_offset + BLOCK_SIZE, file_size)
        block_len = end_offset - start_offset
        
        # Extract block data (slice creates copy, needed for finding)
        # We work on this block as a local universe
        block_view = ba[start_offset:end_offset]
        block_mv = memoryview(ba)[start_offset:end_offset]
        
        for L, patterns in pattern_groups.items():
            if L <= 0 or block_len < L:
                continue

            zero = b"\x00" * L
            occurrences = {} # pattern -> list of local_offsets
            
            # First pass: Count occurrences in this block
            i = 0
            end = block_len - L
            
            while i <= end:
                chunk = bytes(block_mv[i:i+L])
                if chunk in patterns:
                    if chunk not in occurrences:
                        occurrences[chunk] = []
                    occurrences[chunk].append(i)
                    i += L
                else:
                    i += 1
            
            # Second pass: Null based on target counts
            for pat, positions in occurrences.items():
                count = len(positions)
                
                if count in target_counts:
                    for pos in positions:
                        # Apply to main bytearray using absolute offset
                        abs_pos = start_offset + pos
                        ba[abs_pos:abs_pos+L] = zero
                    total_hits += count
                    modified = True

    if modified:
        Path(file_path).write_bytes(ba)

    return total_hits

def generate_exclude_txt():
    """Generate exclude.txt from changelog entries (hex values used in mod skin)."""
    exclude_hexes = set()
    
    for entry in changelog_entries:
        exclude_hexes.add(entry['source_hex'].lower())
        exclude_hexes.add(entry['target_hex'].lower())
        if entry['source_index'] != "N/A":
            exclude_hexes.add(entry['source_index'].lower())
        if entry['target_index'] != "N/A":
            exclude_hexes.add(entry['target_index'].lower())
    
    # Write exclude.txt
    exclude_txt_path = os.path.join(BASE_DIR, "exclude.txt")
    with open(exclude_txt_path, 'w', encoding='utf-8') as f:
        f.write("# Hex values to exclude from nulling (auto-generated from changelog)\n")
        f.write(" ".join(sorted(exclude_hexes)))
    
    print(f"{Fore.GREEN}✅ Generated exclude.txt with {len(exclude_hexes)} hex values")
    return exclude_hexes

def process_size_fix():
    """Process size fix by nulling hex values using super fast algorithm."""
    print(f"\n{Fore.CYAN}🔧 Step 3: Processing Size Fix (nulling)...")
    
    # Load all skin data once
    skins_data = load_all_skins_data()
    if not skins_data:
        print(f"{Fore.RED}❌ Skin data is empty. Cannot continue size fix.")
        return
    
    print(f"{Fore.GREEN}Loading hex values from centralized skin data...")
    
    valid_entries = [] # List of (hex, name)
    skipped_count_name = 0
    skipped_count_zeros = 0
    
    # Define exclusion keywords (case-insensitive)
    exclude_keywords = {"face", "hair", "head", "male", "female"}
    
    for skin_id, info in skins_data.items():
        hex_code = info['hex']
        skin_name = info['name'].lower()
        
        # Filter 1: Exclude by name
        if any(keyword in skin_name for keyword in exclude_keywords):
            skipped_count_name += 1
            continue
        
        # Filter 2: Exclude if hex contains "0000"
        if "0000" in hex_code:
            skipped_count_zeros += 1
            continue
        
        valid_entries.append((hex_code, skin_name))
    
    print(f"{Fore.GREEN}Loaded {len(valid_entries)} valid entries from ALL.txt")
    print(f"{Fore.YELLOW}Skipped {skipped_count_name} due to name filters (face, hair, etc.)")
    print(f"{Fore.YELLOW}Skipped {skipped_count_zeros} due to '0000' filter")
    # Generate exclude.txt from changelog
    exclude_hexes = generate_exclude_txt()

    # Ask for custom block indices
    print(f"\n{Fore.CYAN}Optional: Enter custom block indices to null globally (e.g., 4,5,6)")
    custom_blocks_input = input(f"{Fore.CYAN}Press Enter to skip: ").strip()
    custom_blocks = set()
    if custom_blocks_input:
        try:
            custom_blocks = {int(x.strip()) for x in custom_blocks_input.replace(',', ' ').split() if x.strip()}
            print(f"{Fore.GREEN}✅ Added custom blocks: {sorted(custom_blocks)}")
        except ValueError:
            print(f"{Fore.RED}⚠️ Invalid block input. Skipping custom blocks.")

    # Ask for main nulling mode
    print(f"\n{Fore.CYAN}Select Nulling Mode:")
    print(f"{Fore.YELLOW}1. Null all valid hex values (excluding skin mod hexes)")
    print(f"{Fore.YELLOW}2. Null specific count of hex values (excluding skin mod hexes)")
    
    while True:
        mode_choice = input(f"{Fore.CYAN}Enter choice (1 or 2): ").strip()
        if mode_choice in ['1', '2']:
            break
        print(f"{Fore.RED}❌ Invalid choice. Enter 1 or 2.")
    
    null_limit = None
    if mode_choice == '2':
        while True:
            try:
                null_limit = int(input(f"{Fore.CYAN}Enter how many hex values to null: ").strip())
                if null_limit > 0:
                    break
                print(f"{Fore.RED}❌ Please enter a positive number.")
            except ValueError:
                print(f"{Fore.RED}❌ Please enter a valid number.")

    # Ask for occurrence counts
    print(f"\n{Fore.CYAN}Enter occurrence counts to trigger nulling (e.g., 1,2,3 or 1,3)")
    occ_input = input(f"{Fore.CYAN}Default is 2 (Press Enter to use 2): ").strip()
    target_counts = {2} # Default
    if occ_input:
        try:
            target_counts = {int(x.strip()) for x in occ_input.replace(',', ' ').split() if x.strip()}
            print(f"{Fore.GREEN}✅ Nulled when hex appears: {sorted(target_counts)} times in a block")
        except ValueError:
            print(f"{Fore.RED}⚠️ Invalid input. Using default (exactly 2).")

    # Ask for additional name exclusions only in mode 1 (All hexes)
    extra_name_exclusions = set()
    if mode_choice == '1':
        response = input(f"{Fore.CYAN}Do you want to exclude any skins by name? (y/n): ").strip().lower()
        if response == 'y':
            exclusion_input = input("Enter skin name fragments separated by commas (e.g., camo,raven,pharaoh): ")
            extra_name_exclusions = {frag.strip().lower() for frag in exclusion_input.split(",") if frag.strip()}
    
    # Filter hexes
    final_hexes = []
    
    for hx, name in valid_entries:
        if hx in exclude_hexes:
            continue
        
        # Check extra user-provided exclusions
        if mode_choice == '1' and extra_name_exclusions:
            skip = False
            for excl in extra_name_exclusions:
                if excl in name: # substring check
                    skip = True
                    break
            if skip:
                continue
        
        final_hexes.append(hx)
        
    # Apply limit if in mode 2
    if null_limit and len(final_hexes) > null_limit:
        final_hexes = final_hexes[:null_limit]
        print(f"{Fore.YELLOW}Limited to {null_limit} hex values")
    
    print(f"{Fore.YELLOW}Excluding {len(exclude_hexes)} hex values used in mod skin")
    print(f"{Fore.GREEN}Final hex values to null: {len(final_hexes)}")
    
    # Build pattern groups for fast scanning
    pattern_groups = build_pattern_groups(final_hexes)
    total_patterns = sum(len(v) for v in pattern_groups.values())
    print(f"{Fore.CYAN}Prepared {total_patterns} patterns (lengths: {sorted(pattern_groups.keys())})")
    
    # Get list of files to process
    files_to_process = []
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for file_name in files:
            if not file_name.lower().endswith('.txt'):
                files_to_process.append(os.path.join(root, file_name))
    
    total_files = len(files_to_process)
    print(f"\n{Fore.CYAN}Processing {total_files} files...")
    print(f"{Fore.CYAN}{'='*60}")
    
    # Process files with progress bar
    total_nulled = 0
    files_modified = 0
    
    for file_idx, file_path in enumerate(files_to_process, 1):
        # Auto-detected blocks
        auto_blocks = modified_blocks_map.get(file_path, set())
        
        # ============================================================ine with custom blocks
        dirty_blocks = auto_blocks.union(custom_blocks)
        
        if not dirty_blocks:
            continue
            
        hits = null_bytes_in_file(file_path, pattern_groups, dirty_blocks, target_counts)
        if hits > 0:
                 files_modified += 1
                 total_nulled += hits
        
        # Progress bar
        progress = (file_idx / total_files) * 100
        bar_length = 40
        filled_length = int(bar_length * file_idx // total_files)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # Real-time display with immediate flush
        print(f"\r{Fore.CYAN}[{bar}] {progress:.1f}% | File: {file_idx}/{total_files} | "
              f"{Fore.GREEN}Hex Values: {len(final_hexes)}{Fore.CYAN} | "
              f"{Fore.YELLOW}Occurrences: {total_nulled}{Style.RESET_ALL}", end='', flush=True)
        sys.stdout.flush()
    
    print()  # New line after progress bar
    print(f"{Fore.CYAN}{'='*60}")
    
    # Write nulled.txt report
    with open(NULLED_TXT_PATH, 'w', encoding='utf-8') as f:
        f.write("Nulled Hex Values Report\n")
        f.write("========================\n")
        if mode_choice == '2':
            f.write(f"Mode: Null Count (limited to {len(final_hexes)} unique hex values)\n")
        else:
            f.write("Mode: Null All Hex\n")
        f.write(f"\nTotal files scanned: {total_files}\n")
        f.write(f"Files modified: {files_modified}\n")
        f.write(f"Unique hex values nulled: {len(final_hexes)}\n")
        f.write(f"Total occurrences replaced: {total_nulled}\n")
        f.write(f"\nHex values excluded: {len(exclude_hexes)}\n")
    
    print(f"\n{Fore.GREEN}✅ Processed {total_files} files")
    print(f"{Fore.GREEN}✅ Files modified: {files_modified}")
    print(f"{Fore.GREEN}✅ Unique hex values nulled: {len(final_hexes)}")
    print(f"{Fore.GREEN}✅ Total occurrences replaced: {total_nulled}")
    print(f"{Fore.GREEN}✅ Nulling report written to: {NULLED_TXT_PATH}")

# =========================== AUTO THEME TOOL ===========================
def read_lobbies():
    """Read lobbies from lobby.txt"""
    lobbies = []
    try:
        with open(LOBBY_FILE, "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    lobbies.append((parts[1].strip(), parts[2].strip()))  # Hex and Name
        return lobbies
    except FileNotFoundError:
        print(colored("lobby.txt not found.", 'red'))
        return None

def swap_indexes_in_files(default_hex, target_hex):
    """Swap indexes in AUTO_THEME files"""
    default_hex_bytes = bytes.fromhex(default_hex)
    target_hex_bytes = bytes.fromhex(target_hex)

    for filename in os.listdir(AUTO_THEME_FILES):
        file_path = os.path.join(AUTO_THEME_FILES, filename)

        with open(file_path, "rb") as file:
            file_data = file.read()

        updated_data = bytearray(file_data)
        default_index = None
        target_index = None
        default_pos = None
        target_pos = None

        # Find default hex
        for i in range(len(file_data) - len(default_hex_bytes), 7, -1):
            if file_data[i:i + len(default_hex_bytes)] == default_hex_bytes:
                default_index = file_data[i - 8]
                default_pos = i - 8
                break

        # Find target hex
        for i in range(len(file_data) - len(target_hex_bytes), 7, -1):
            if file_data[i:i + len(target_hex_bytes)] == target_hex_bytes:
                target_index = file_data[i - 8]
                target_pos = i - 8
                break

        if default_pos is not None and target_pos is not None:
            updated_data[default_pos] = target_index
            updated_data[target_pos] = default_index

            print(colored(f"Swapped in {filename}:", 'green'))
            print(colored(f"  Default HEX {default_hex} got index {target_index:02X}", 'cyan'))
            print(colored(f"  Target HEX  {target_hex} got index {default_index:02X}", 'cyan'))
        else:
            print(colored(f"Hex not found properly in {filename}", 'yellow'))

        result_path = os.path.join(AUTO_THEME_RESULT, filename)
        os.makedirs(AUTO_THEME_RESULT, exist_ok=True)
        with open(result_path, "wb") as file:
            file.write(updated_data)

def run_auto_theme():
    """Run AUTO THEME tool"""
    DEFAULT_HEX = "7480100C"  # Main Lobby HEX from lobby.txt

    while True:
        display_tool_name()
        color_cycled_text("\nCHETAN")
        print(colored("1] SWAP LOBBY INDEX", 'yellow', attrs=['bold']))
        print(colored("2] BACK TO MAIN MENU", 'green', attrs=['bold']))
        choice = input(colored("@SELECT OPTION = ", 'white', attrs=['bold']))

        if choice == "1":
            lobbies = read_lobbies()

            if not lobbies:
                print(colored("lobby.txt not found or empty.", 'red'))
                continue

            color_cycled_text("\nAvailable Lobbies:")
            for i, (_, name) in enumerate(lobbies, 1):
                print(colored(f"{i}. {name}", 'green'))

            lobby_choice = input(colored("Select a lobby theme to swap with Main Lobby: ", 'magenta', attrs=['bold']))

            try:
                lobby_choice = int(lobby_choice) - 1
                if 0 <= lobby_choice < len(lobbies):
                    target_hex, lobby_name = lobbies[lobby_choice]
                    print(colored(f"Swapping index between Main Lobby and: {lobby_name}", 'yellow'))
                    swap_indexes_in_files(DEFAULT_HEX, target_hex)
                else:
                    print(colored("Invalid selection.", 'red'))
            except ValueError:
                print(colored("Invalid input. Please enter a number.", 'red'))

        elif choice == "2":
            break
        else:
            print(colored("Invalid choice. Please try again.", 'red'))

# =========================== HIT EFFECT & LOOTCRATES TOOL ===========================
def norm_hex(s: str) -> str:
    s = str(s).lower().strip()
    s = s[2:] if s.startswith("0x") else s
    return re.sub(r'[^0-9a-f]', '', s)

def valid_hex(s: str) -> bool:
    return bool(re.fullmatch(r'[0-9a-f]+', s)) and len(s) % 2 == 0

def looks_like_explicit_hex(token: str) -> bool:
    t = token.strip().lower()
    if t.startswith("0x"): return True
    return bool(re.search(r'[a-f]', t))

LEVEL_RE = re.compile(r'\(?\s*lv\.?\s*[:.]?\s*([0-9]+)\s*\)?|level\s*[:.]?\s*([0-9]+)', re.I)

def extract_level(name: str):
    m = LEVEL_RE.search(name)
    if not m: return None
    for g in m.groups():
        if g: return int(g)
    return None

def strip_level(name: str):
    name = re.sub(r'\(?\s*lv\.?\s*[:.]?\s*[0-9]+\s*\)?', '', name, flags=re.I)
    name = re.sub(r'level\s*[:.]?\s*[0-9]+', '', name, flags=re.I)
    return re.sub(r'\s+', ' ', name).strip().lower()

def gather(path):
    out = []
    for r,_,files in os.walk(path):
        for fn in files:
            out.append(os.path.join(r,fn))
    return out

def size_fix_hitloot(from_b: bytes, target_len: int):
    if len(from_b) == target_len: return from_b, None
    if len(from_b) < target_len:
        return from_b + b'\x00'*(target_len - len(from_b)), "padded"
    return from_b[:target_len], "truncated"

def sanitize_rel(rel_path: str) -> str:
    """Remove a leading 'org' segment from rel_path"""
    parts = rel_path.split(os.sep)
    if parts and parts[0].lower() == "org":
        parts = parts[1:]
    if not parts:
        return os.path.basename(rel_path)
    return os.path.join(*parts)

def clean_modified(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except Exception as e:
            print(f"{Fore.YELLOW}Warning cleaning {path}: {e}")
    os.makedirs(path, exist_ok=True)

def run_hit_loot_tool():
    """Run HIT EFFECT & LOOTCRATES tool with modskin.txt for pairs"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}🌟 Hit Effect & Lootcrates Tool 🌟")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    # Clean previous modified outputs
    print(f"{Fore.CYAN}Preparing tool folders (cleaning previous modified outputs)")
    clean_modified(HIT_MODIFIED)
    clean_modified(LOOT_MODIFIED)
    print(f"{Fore.GREEN}Clean complete.\n")
    
    # Track modified blocks for nulling {file_path: set(block_indices)}
    hit_loot_modified_blocks = {}
    
    # Load hit.txt
    if not os.path.exists(HIT_TXT_PATH):
        print(f"{Fore.RED}ERROR: hit.txt missing at: {HIT_TXT_PATH}")
        return
    
    entries = []
    id_to_entry = {}
    hex_to_entry = {}
    by_name = {}
    
    with open(HIT_TXT_PATH, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            parts = line.strip().split(" | ")
            if len(parts) < 3: continue
            idv, hx_raw, name_raw = parts[0].strip(), parts[1].strip(), parts[2].strip()
            hx = norm_hex(hx_raw)
            if not hx: continue
            name_l = name_raw.lower()
            lvl = extract_level(name_l)
            base = strip_level(name_l)
            e = {"id": idv, "hex": hx, "name": name_raw, "base": base, "level": lvl}
            entries.append(e)
            if idv: id_to_entry[idv] = e
            hex_to_entry[hx] = e
            by_name.setdefault(base, {})[lvl if lvl is not None else 0] = hx
    
    print(f"{Fore.GREEN}Loaded {len(entries)} entries from hit.txt\n")
    
    
    # Input pairs manually
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}Input pairs (one per line) — empty line to finish")
    print(f"{Style.DIM}Format: first second  (IDs or hex). Numeric-only tokens treated as IDs.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    id_pairs = []
    import re
    SEP_RE = re.compile(r'[;:|,\s]+')
    
    while True:
        try:
            line = input(">> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
            
        if not line:
            break
            
        parts = SEP_RE.split(line, maxsplit=1)
        if len(parts) < 2:
            ws = line.split()
            if len(ws) < 2:
                continue
            a, b = ws[0], " ".join(ws[1:])
        else:
            a, b = parts[0], parts[1]
            
        id_pairs.append((a.strip(), b.strip()))
    
    if not id_pairs:
        print(f"{Fore.RED}No pairs provided. Returning to menu.")
        return
    
    print(f"{Fore.GREEN}Found {len(id_pairs)} pairs to process\n")
    
    # Resolve pairs for Hit (level 5) and Loot (max level)
    def resolve_hit_second(token: str):
        token = token.strip()
        if token in id_to_entry:
            e = id_to_entry[token]; base = e["base"]
            if 5 in by_name.get(base, {}): return by_name[base][5]
            return e["hex"]
        t = norm_hex(token)
        if t in hex_to_entry:
            e = hex_to_entry[t]; base = e["base"]
            if 5 in by_name.get(base, {}): return by_name[base][5]
            return t
        return t
    
    def resolve_loot_second(token: str):
        token = token.strip()
        if token in id_to_entry:
            e = id_to_entry[token]; base = e["base"]
            lvlmap = by_name.get(base, {})
            if lvlmap:
                maxlvl = max(k for k in lvlmap.keys() if isinstance(k, int))
                return lvlmap[maxlvl]
            return e["hex"]
        t = norm_hex(token)
        if t in hex_to_entry:
            e = hex_to_entry[t]; base = e["base"]
            lvlmap = by_name.get(base, {})
            if lvlmap:
                maxlvl = max(k for k in lvlmap.keys() if isinstance(k, int))
                return lvlmap[maxlvl]
            return t
        return t
    
    # Validate and build pairs
    pairs_hit = []
    pairs_loot = []
    protected = set()
    
    for a_raw, b_raw in id_pairs:
        first_hex = None
        if a_raw in id_to_entry:
            first_hex = id_to_entry[a_raw]["hex"]
        else:
            if looks_like_explicit_hex(a_raw):
                nh = norm_hex(a_raw)
                if valid_hex(nh):
                    first_hex = nh
        
        if not first_hex:
            print(f"{Fore.YELLOW}⚠️ Could not resolve first token: {a_raw}")
            continue
        
        hit_hex = resolve_hit_second(b_raw)
        loot_hex = resolve_loot_second(b_raw)
        
        if not hit_hex or not loot_hex:
            print(f"{Fore.YELLOW}⚠️ Could not resolve second token: {b_raw}")
            continue
        
        # Add to HIT pairs (no length constraint)
        pairs_hit.append((first_hex, hit_hex))
        protected.add(first_hex)
        protected.add(hit_hex)
        
        # Add to LOOT pairs (STRICT length constraint)
        if len(first_hex) == len(loot_hex):
            pairs_loot.append((first_hex, loot_hex))
            protected.add(loot_hex)
        else:
            print(f"{Fore.YELLOW}⚠️ Skipping Lootcrate pair {a_raw}->{b_raw} due to length mismatch ({len(first_hex)//2} vs {len(loot_hex)//2} bytes)")
    
    print(f"{Fore.GREEN}Prepared {len(pairs_hit)} pairs for HIT EFFECT")
    print(f"{Fore.GREEN}Prepared {len(pairs_loot)} pairs for LOOTCRATES (length-matched)\n")
    
    # Process HIT EFFECT files
    print(f"{Fore.CYAN}Processing HIT EFFECT files...")
    orig_hit_files = gather(HIT_ORIG) if os.path.exists(HIT_ORIG) else []
    

    
    modified_hit = []
    for src in orig_hit_files:
        try:
            with open(src, 'rb') as fh:
                data = fh.read()
        except Exception:
            continue
        
        orig = data
        changes = []
        
    modified_hit = []
    for src in orig_hit_files:
        try:
            with open(src, 'rb') as fh:
                data = fh.read()
        except Exception:
            continue
        
        orig = data
        changes = []
        
        for first_hex, second_hex in pairs_hit:
            try:
                to_b = bytes.fromhex(second_hex)
                from_raw = bytes.fromhex(first_hex)
            except Exception:
                continue
            
            cnt_norm = data.count(to_b)
            cnt_rev = data.count(to_b[::-1])
            
            if cnt_norm == 0 and cnt_rev == 0:
                continue
            
            replacement, note = size_fix_hitloot(from_raw, len(to_b))
            
            if cnt_norm:
                data = data.replace(to_b, replacement)
                
            if cnt_rev:
                data = data.replace(to_b[::-1], replacement[::-1])
            
            changes.append((second_hex, first_hex, cnt_norm, cnt_rev, note))
        
        if data != orig:
            rel = os.path.relpath(src, HIT_ORIG)
            rel = sanitize_rel(rel)
            outp = os.path.join(HIT_MODIFIED, rel)
            os.makedirs(os.path.dirname(outp), exist_ok=True)
            
            with open(outp, 'wb') as outfh:
                outfh.write(data)
            
            modified_hit.append((rel, changes))
    
    print(f"{Fore.GREEN}✅ Modified {len(modified_hit)} HIT EFFECT files\n")
    
    # Process LOOTCRATES files
    print(f"{Fore.CYAN}Processing LOOTCRATES files...")
    orig_loot_files = gather(LOOT_ORIG) if os.path.exists(LOOT_ORIG) else []
    
    copied_loot = []
    for src in orig_loot_files:
        rel = os.path.relpath(src, LOOT_ORIG)
        rel = sanitize_rel(rel)
        outp = os.path.join(LOOT_MODIFIED, rel)
        os.makedirs(os.path.dirname(outp), exist_ok=True)
        shutil.copy2(src, outp)
        copied_loot.append(outp)
    
    modified_loot = []
    for outp in copied_loot:
        try:
            with open(outp, 'rb') as fh:
                data = fh.read()
        except Exception:
            continue
        
        orig = data
        changes = []
        
        for first_hex, second_hex in pairs_loot:
            try:
                to_b = bytes.fromhex(second_hex)
                from_raw = bytes.fromhex(first_hex)
            except Exception:
                continue
            
            cnt_norm = data.count(to_b)
            cnt_rev = data.count(to_b[::-1])
            
            if cnt_norm == 0 and cnt_rev == 0:
                continue
            
            replacement, note = size_fix_hitloot(from_raw, len(to_b))
            
            if cnt_norm:
                data = data.replace(to_b, replacement)
                
            if cnt_rev:
                data = data.replace(to_b[::-1], replacement[::-1])
            
            changes.append((second_hex, first_hex, cnt_norm, cnt_rev, note))
        
        if data != orig:
            with open(outp, 'wb') as outfh:
                outfh.write(data)
            
            rel = os.path.relpath(outp, LOOT_MODIFIED)
            rel = sanitize_rel(rel)
            modified_loot.append((rel, changes))
    
    print(f"{Fore.GREEN}✅ Modified {len(modified_loot)} LOOTCRATES files\n")
    
    # Nulling step matching hitloot.py exactly
    print(f"{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}NULLING (optional)")
    print(f"{Fore.CYAN}{'='*60}\n")
    
    print("Enter integer N (e.g. 30) to null UP TO N distinct hex VALUES PER FILE.")
    print("Each selected hex will be fully nulled in that file.")
    print("Enter 0 to skip nulling.")
    choice = input(">> ").strip()
    
    # 1. Full candidate list (no filters other than protected)
    all_candidates = [e["hex"] for e in entries if e["hex"] not in protected]
    
    per_file_N = None
    if choice and choice != "0":
        try:
            N = int(choice)
            if N > 0:
                per_file_N = N
        except:
            pass
            
    if per_file_N:
        N = per_file_N
        print(f"\n{Fore.GREEN}Found {len(all_candidates)} valid hex candidates (unfiltered)")
        print(f"{Fore.CYAN}Nulling up to {N} distinct hex values per file...")

        # Build target list
        targets = []
        for base in (HIT_MODIFIED, LOOT_MODIFIED):
            for r, _, files in os.walk(base):
                for fn in files:
                    targets.append(os.path.join(r, fn))
        
        # Identify global present hexes for fallback
        global_present = set()
        for fp in targets:
            try:
                with open(fp, 'rb') as fh:
                    d = fh.read()
            except Exception:
                continue
            
            for e in entries:
                hx = e["hex"]
                if hx in protected:
                    continue
                b = bytes.fromhex(hx)
                if b in d or b[::-1] in d:
                    global_present.add(hx)
        
        global_present_list = list(global_present) if global_present else list(all_candidates)
        
        nulled_counts = defaultdict(int)
        files_modified_count = 0
        total_files = len(targets)
        
        for file_idx, fp in enumerate(targets, 1):
            try:
                with open(fp, 'rb') as fh:
                    data = fh.read()
            except Exception:
                continue
            
            # Find present hexes in this file
            present = []
            for e in entries:
                hx = e["hex"]
                if hx in protected:
                    continue
                b = bytes.fromhex(hx)
                if b in data or b[::-1] in data:
                    present.append(hx)
            
            # Select up to N hexes
            selected = []
            for hx in present:
                if len(selected) >= N:
                    break
                selected.append(hx)
            
            if len(selected) < N:
                for hx in global_present_list:
                    if hx in selected:
                        continue
                    selected.append(hx)
                    if len(selected) >= N:
                        break
            
            if len(selected) < N:
                for hx in all_candidates:
                    if hx in selected:
                        continue
                    selected.append(hx)
                    if len(selected) >= N:
                        break
            
            if not selected:
                # Update progress even if skipped
                progress = (file_idx / total_files) * 100
                bar_length = 40
                filled_length = int(bar_length * file_idx // total_files)
                bar = '█' * filled_length + '-' * (bar_length - filled_length)
                print(f"\r{Fore.CYAN}[{bar}] {progress:.1f}% | File: {file_idx}/{total_files} | "
                      f"{Fore.YELLOW}Occurrences: {sum(nulled_counts.values())}{Style.RESET_ALL}", end='', flush=True)
                continue
            
            # Nulling logic from hitloot.py (simple replace)
            changed = False
            for hx in selected:
                b = bytes.fromhex(hx)
                z = b'\x00' * len(b)
                
                cnt_norm = data.count(b)
                cnt_rev = data.count(b[::-1])
                tot = cnt_norm + cnt_rev
                
                if tot:
                    if cnt_norm:
                        data = data.replace(b, z)
                    if cnt_rev:
                        data = data.replace(b[::-1], z)
                    nulled_counts[hx] += tot
                    changed = True
            
            if changed:
                with open(fp, 'wb') as outfh:
                    outfh.write(data)
                files_modified_count += 1
                
            # Progress bar
            progress = (file_idx / total_files) * 100
            bar_length = 40
            filled_length = int(bar_length * file_idx // total_files)
            bar = '█' * filled_length + '-' * (bar_length - filled_length)
            
            print(f"\r{Fore.CYAN}[{bar}] {progress:.1f}% | File: {file_idx}/{total_files} | "
                  f"{Fore.YELLOW}Occurrences: {sum(nulled_counts.values())}{Style.RESET_ALL}", end='', flush=True)

        print() # New line
        print(f"{Fore.GREEN}✅ Nulled {len(nulled_counts)} distinct hex values")
        print(f"{Fore.GREEN}✅ Total occurrences: {sum(nulled_counts.values())}\n")
        print(f"{Fore.GREEN}✅ Modified {files_modified_count} files during nulling phase\n")

    
    print(f"{Fore.GREEN}{'='*60}")
    print(f"{Fore.GREEN}🎉 HIT EFFECT & LOOTCRATES Tool Complete!")
    print(f"{Fore.GREEN}Modified files are in:")
    print(f"{Fore.GREEN}  - {HIT_MODIFIED}")
    print(f"{Fore.GREEN}  - {LOOT_MODIFIED}")
    print(f"{Fore.GREEN}{'='*60}\n")

# =========================== MAIN MENU ===========================
def main_menu():
    """Main menu to select between tools"""
    while True:
        display_tool_name()
        
        
      
        choice = input(colored("\n@ SELECT OPTION = ", 'white', attrs=['bold']))
        
        if choice == "1":
            while True:
                display_tool_name()
                
                print(colored("1] MODSKIN + SIZEFIX", 'yellow', attrs=['bold']))
                print(colored("2] MODSKIN ONLY", 'green', attrs=['bold']))
                print(colored("3] SIZE FIX ONLY", 'cyan', attrs=['bold']))
                print(colored("4] BACK TO MAIN MENU", 'red', attrs=['bold']))
                
                sub_choice = input(colored("\n@ SELECT OPTION = ", 'white', attrs=['bold']))
                
                if sub_choice == "1":
                    # MODSKIN + SIZEFIX
                    if not copy_files_to_output():
                        input("Press Enter to continue...")
                        continue
                    process_mod_skin()
                    write_changelog()
                    print(f"{Fore.GREEN}✅ Changelog written to: {CHANGELOG_PATH}")
                    process_size_fix()
                    input("\nPress Enter to continue...")
                    break
                
                elif sub_choice == "2":
                    # MODSKIN ONLY
                    if not copy_files_to_output():
                        input("Press Enter to continue...")
                        continue
                    process_mod_skin()
                    write_changelog()
                    print(f"{Fore.GREEN}✅ Changelog written to: {CHANGELOG_PATH}")
                    input("\nPress Enter to continue...")
                    break
                
                elif sub_choice == "3":
                    # SIZE FIX ONLY
                    process_size_fix()
                    input("\nPress Enter to continue...")
                    break
                
                elif sub_choice == "4":
                    break
                else:
                    print(colored("\nInvalid choice. Please try again.", 'red'))
                    time.sleep(1)
        
        elif choice == "2":
            # Run HIT EFFECT & LOOTCRATES Tool
            run_hit_loot_tool()
            input("Press Enter to continue...")
        
        elif choice == "3":
            # Run AUTO THEME Tool
            run_auto_theme()
        
        elif choice == "4":
            print(colored("\n👁️‍🗨️ getout  ", 'red'))
            break
        
        else:
            print(colored("\nInvalid choice. Please try again.", 'red'))
            input("Press Enter to continue...")

# =========================== MAIN ENTRY POINT ===========================
if __name__ == "__main__":
    while True:
        if auth_screen():
            break
    main_menu()