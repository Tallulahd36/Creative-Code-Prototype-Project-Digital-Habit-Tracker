# ---------------------------------------------------------
# 52685 Working with Data and Code A2 
# Creative Coding Prototype Project
# Tallulah Dawe 24961587
# Monthly Habit Tracker | ADHD & Neurodivergent Children and Young Adults-Friendly Prototype
# Tabs: [Daily Habit Tracker Calendar | Tracked Monthly Habits Data Visualisation]
# ==============================================================

import calendar
from datetime import datetime

# ------------------ CONTENT 
# Automated habits (user can delete / add habits of own choice)
STANDARD_HABITS = [
  "Drink water", "Eat 3 good meals", "Sleep 8+ hours", "30+ mins hobby",
  "Go outside", "Tidy room 10 mins", "Read 10 mins", "Exercise / stretch"
]

# ASCII-only monthly quotes (motivational quote cards for each month);
MONTH_QUOTES = [
  "",
  "Strength does not come from winning. Your struggles develop your strengths. When you go through hardships and decide not to surrender, that is strength.",
  "Don't let what you cannot do interfere with what you can do. - John Wooden",
  "Small deeds done are better than great deeds planned. - Peter Marshall",
  "Persistence can change failure into extraordinary achievement. - Matt Biondi",
  "Perfection is boring. Constant improvement is beautiful. - Misty Copeland",
  "Challenges are what make life interesting and overcoming them is what makes life meaningful. - Joshua J. Marine",
  "Believe you can and you're halfway there. - Theodore Roosevelt",
  "You are never too old to set another goal or to dream a new dream. - C. S. Lewis",
  "You are the hero of your own story. - Joseph Campbell",
  "Your success will largely depend on your belief in yourself and your determination to overcome every obstacle. - John Di Lemme",
  "It always seems impossible until it's done. - Nelson Mandela",
  "You are braver than you believe, stronger than you seem, and smarter than you think. - A. A. Milne",
]

# ------------------ STATE 
max_days = 31
habits = list(STANDARD_HABITS)
habit_data = [[False for _ in range(max_days)] for _ in range(len(habits))]

month = datetime.now().month
year  = datetime.now().year
days_in_month = calendar.monthrange(year, month)[1]

selected = [0, 0]   # [row, col]

# notes/reward
reward_text = ""
focus_reward = False

# add-habit modal
adding_habit = False
habit_input  = ""

# files
gridfile  = ""
notesfile = ""

# tabs
view_mode = "tracker"   # 'tracker' or 'visuals'

# ------------------ LAYOUT  
# window that fits on Mac screens 
WIN_W, WIN_H = 1150, 760

# Base design size 
_BASE_W, _BASE_H = 1280.0, 920.0
SF = min(WIN_W/_BASE_W, WIN_H/_BASE_H)   # global scale factor
def S(v): return int(round(v * SF))      # helper to scale all constants

SHEET_MARGIN = S(36)
SHEET_X, SHEET_Y = SHEET_MARGIN, SHEET_MARGIN
SHEET_W, SHEET_H = WIN_W - 2*SHEET_MARGIN, WIN_H - 2*SHEET_MARGIN

TITLE_Y = SHEET_Y + S(54)

# Month selector (right aligned)
MONTH_W, MONTH_H = S(300), S(36)
MONTH_X = SHEET_X + SHEET_W - MONTH_W - S(140)
MONTH_Y = TITLE_Y - S(2)
PREV_X, PREV_Y = MONTH_X - S(56), MONTH_Y
NEXT_X, NEXT_Y = MONTH_X + MONTH_W + S(12), MONTH_Y

# Action buttons (month nav)
BTN_W, BTN_H = S(132), S(32)

# Tabs under the title
TAB_H = S(34)
TAB_TRK_W, TAB_VIS_W = S(150), S(180)
TAB_TRK_X, TAB_TRK_Y = SHEET_X + S(24), TITLE_Y + S(22)
TAB_VIS_X, TAB_VIS_Y = TAB_TRK_X + TAB_TRK_W + S(10), TAB_TRK_Y

# Action buttons (tracker tab)
ADD_X, ADD_Y = SHEET_X + S(24), TAB_TRK_Y + TAB_H + S(10)
DEL_X, DEL_Y = ADD_X + BTN_W + S(12), ADD_Y

# Header baseline
HEADER_BOTTOM = max(TAB_TRK_Y + TAB_H, ADD_Y + BTN_H) + S(16)

# Tracker grid & side panel
GRID_X, GRID_Y = SHEET_X + S(72), HEADER_BOTTOM + S(28)
GRID_W, GRID_H = S(820), S(440)
LEFT_W = S(230)

PANEL_X, PANEL_Y = GRID_X + GRID_W + S(18), GRID_Y
PANEL_W, PANEL_H = SHEET_X + SHEET_W - PANEL_X - S(24), GRID_H

# Quote card
QUOTE_X, QUOTE_Y = PANEL_X + S(14), PANEL_Y + PANEL_H - S(122)
QUOTE_W, QUOTE_H = PANEL_W - S(28), S(108)

# Progress bar + reward
PROG_X, PROG_Y, PROG_W, PROG_H = GRID_X, GRID_Y + GRID_H + S(16), (PANEL_X + PANEL_W) - GRID_X, S(22)
REWARD_X, REWARD_Y = GRID_X, PROG_Y + PROG_H + S(18)
REWARD_W, REWARD_H = PROG_W, S(150)

# Visualisation canvas and Save button
VIS_X, VIS_Y = SHEET_X + S(60), HEADER_BOTTOM + S(34)
VIS_W, VIS_H = SHEET_W - S(120), SHEET_H - (VIS_Y - SHEET_Y) - S(40)
SAVE_X, SAVE_Y, SAVE_W, SAVE_H = SHEET_X + SHEET_W - S(140), TAB_TRK_Y, S(116), TAB_H

# ------------------ COLOURS 
def C(r,g,b,a=255): return color(r,g,b,a)
BG        = C(225,235,240)
PAPER     = C(255,255,253)
INK       = C(36,52,72)
GREEN     = C(36,168,88)
GRID      = C(210,215,220)
GRID_BOLD = C(180,185,190)
HEAD_GREY = C(235,239,242)
# stronger week bands
PASTELS   = [ C(255,200,170,90), C(255,230,170,90), C(175,225,215,90), C(180,205,235,90) ]
QUOTE_BG  = C(230,210,255) 

# ring colour palette 
RING_COLS = [
  C(70,130,180),  # steel blue
  C(46,139,87),   # sea green
  C(218,112,214), # orchid
  C(255,140,0),   # dark orange
  C(100,149,237), # cornflower
  C(199,21,133),  # medium violet red
  C(72,61,139),   # dark slate blue
  C(50,205,50)    # lime green
]

# ------------------ FONTS 
# ADHD & Neurodivergent-Friendly fonts (NationalAutisticSociety, 2022)
TITLE_FONT = None   # page title
UI_FONT    = None   # general UI text
QUOTE_FONT = None   # quote card (in italic)

def init_fonts():
    """
    Use system fonts only (no .ttf files in /data).
    Preference:
      - Title: EuphemiaUCAS-Italic (if present), else TrebuchetMS-Bold → Verdana-Bold → Arial-Bold → SansSerif
      - UI:    TrebuchetMS → Verdana → Arial → SansSerif
      - Quote: Georgia-Italic → Times-Italic → EuphemiaUCAS-Italic → SansSerif
    """
    global TITLE_FONT, UI_FONT, QUOTE_FONT

    # --- Title font (prefer EuphemiaUCAS-Italic) 
    tried_title = False
    try:
        TITLE_FONT = createFont("EuphemiaUCAS-Italic", 36)  # macOS often has this
        tried_title = True
    except:
        pass
    if not tried_title or TITLE_FONT is None:
        # Bold fallbacks
        for fam in ["TrebuchetMS-Bold", "Verdana-Bold", "Arial-Bold", "SansSerif"]:
            try:
                TITLE_FONT = createFont(fam, 36)
                break
            except:
                continue
    if TITLE_FONT is None:
        TITLE_FONT = createFont("SansSerif", 36)

    # --- UI font 
    for fam in ["TrebuchetMS", "Verdana", "Arial", "SansSerif"]:
        try:
            UI_FONT = createFont(fam, 16)
            break
        except:
            continue
    if UI_FONT is None:
        UI_FONT = createFont("SansSerif", 16)

    # --- Quote font (italic where possible) 
    for famQ in ["Georgia-Italic", "Times-Italic", "EuphemiaUCAS-Italic", "SansSerif"]:
        try:
            QUOTE_FONT = createFont(famQ, 16)
            break
        except:
            continue
    if QUOTE_FONT is None:
        QUOTE_FONT = UI_FONT

# ------------------ PROCESSING 
def settings(): size(WIN_W, WIN_H)
def setup():
    init_fonts()
    textFont(UI_FONT)
    update_filenames()
    load_grid()
    load_notes()

def draw():
    background(BG)
    draw_sheet()
    draw_header()
    draw_tabs()
    if view_mode == "tracker":
        draw_top_buttons()
        draw_grid()
        draw_points_and_quote()
        draw_progress()
        draw_reward()
    else:
        draw_visual_panel()
    if adding_habit:
        draw_add_popup()

# ------------------ COMMON UI 
def draw_sheet():
    noStroke(); fill(PAPER); rect(SHEET_X, SHEET_Y, SHEET_W, SHEET_H, 12)

def draw_header():
    fill(INK); textAlign(LEFT, CENTER)
    textFont(TITLE_FONT)
    title_txt = "MONTHLY HABIT TRACKER" if view_mode=="tracker" else "Visualising Your Monthly Habit Progress"
    text(title_txt, SHEET_X+24, TITLE_Y)

    # Month nav field 
    noFill(); stroke(GRID_BOLD); rect(MONTH_X, MONTH_Y, MONTH_W, MONTH_H, 8)
    noStroke(); fill(INK); textAlign(LEFT, CENTER); textSize(18); textFont(UI_FONT)
    text(calendar.month_name[month] + " " + str(year), MONTH_X+12, MONTH_Y + MONTH_H/2)

    # nav buttons
    draw_button(PREV_X, PREV_Y, 44, 30, "<")
    draw_button(NEXT_X, NEXT_Y, 44, 30, ">")

def draw_tabs():
    draw_tab(TAB_TRK_X, TAB_TRK_Y, TAB_TRK_W, "Tracker", active=(view_mode=="tracker"))
    draw_tab(TAB_VIS_X, TAB_VIS_Y, TAB_VIS_W, "Visualisation", active=(view_mode=="visuals"))
    if view_mode=="visuals":
        draw_button(SAVE_X, SAVE_Y, SAVE_W, SAVE_H, "Save PNG")

def draw_tab(x,y,w,label,active=False):
    noStroke()
    fill(245 if active else 232)
    rect(x,y,w,TAB_H, 10,10,0,0)
    fill(INK); textAlign(CENTER, CENTER); textSize(15); textFont(UI_FONT)
    text(label, x+w/2, y+TAB_H/2)

def draw_button(x,y,w,h,label):
    noStroke(); fill(240); rect(x,y,w,h,8)
    fill(INK); textAlign(CENTER, CENTER); textSize(14); textFont(UI_FONT)
    text(label, x+w/2, y+h/2)
    
def draw_button_outlined(x, y, w, h, label, stroke_col):
    stroke(stroke_col); strokeWeight(2)
    fill(240); rect(x, y, w, h, 8)
    noStroke(); fill(INK); textAlign(CENTER, CENTER); textSize(14); textFont(UI_FONT)
    text(label, x+w/2, y+h/2)

# ------------------ TRACKER VIEW 
def week_tint(c): return PASTELS[(c//7) % len(PASTELS)]

def draw_tick(cx, cy):
    stroke(GREEN); strokeWeight(3); noFill()
    line(cx-6, cy,   cx-2, cy+6); line(cx-2, cy+6, cx+7, cy-5)
    strokeWeight(1)

def draw_top_buttons():
    # Add and delete habit buttons
    pastel_green = color(176, 230, 200)
    pastel_red   = color(255, 200, 200)

    draw_button_outlined(ADD_X, ADD_Y, BTN_W, BTN_H, "+ New Habit", pastel_green)
    draw_button_outlined(DEL_X, DEL_Y, BTN_W, BTN_H, "- Delete Habit", pastel_red)

def draw_grid():
    #calendar month
    global GRID_GEO
    rows = len(habits) + 1
    cols = days_in_month
    row_h = GRID_H / rows
    col_w = (GRID_W - LEFT_W) / float(cols)

    stroke(GRID_BOLD); noFill(); rect(GRID_X, GRID_Y, GRID_W, GRID_H)
    noStroke(); fill(HEAD_GREY); rect(GRID_X, GRID_Y, LEFT_W, row_h)

    for c in range(cols):
        x = GRID_X + LEFT_W + c*col_w
        fill(week_tint(c)); rect(x, GRID_Y, col_w, row_h)

    # header labels
    fill(INK); textSize(16); textAlign(LEFT, CENTER); textFont(UI_FONT)
    text("HABIT", GRID_X+10, GRID_Y + row_h/2)
    textAlign(CENTER, CENTER)
    for c in range(cols):
        x = GRID_X + LEFT_W + c*col_w
        text(str(c+1), x + col_w/2, GRID_Y + row_h/2)

    # grid lines
    stroke(GRID)
    for r in range(1, rows+1):
        y = GRID_Y + r*row_h; line(GRID_X, y, GRID_X + GRID_W, y)
    for c in range(cols+1):
        x = GRID_X + LEFT_W + c*col_w; line(x, GRID_Y, x, GRID_Y + GRID_H)

    # rows
    textAlign(LEFT, CENTER); fill(INK); textSize(16)
    for r, h in enumerate(habits):
        ymid = GRID_Y + (r+1)*row_h + row_h/2
        if r == selected[0]:
            noStroke(); fill(250,252,255); rect(GRID_X+1, ymid-row_h/2, LEFT_W-2, row_h)
        fill(INK); text(h, GRID_X+10, ymid)
        for c in range(cols):
            x = GRID_X + LEFT_W + c*col_w
            y = GRID_Y + (r+1)*row_h
            noStroke(); fill(week_tint(c)); rect(x, y, col_w, row_h)
            if habit_data[r][c]: draw_tick(x + col_w/2, y + row_h/2)

    # selection outline
    if 0 <= selected[0] < len(habits) and 0 <= selected[1] < cols:
        sr, sc = selected
        noFill(); stroke(60,130,230); strokeWeight(2)
        rect(GRID_X + LEFT_W + sc*col_w, GRID_Y + (sr+1)*row_h, col_w, row_h)
        strokeWeight(1)

    GRID_GEO = (row_h, col_w, cols)

def draw_points_and_quote():
    # right panel
    noStroke(); fill(247,249,252); rect(PANEL_X, PANEL_Y, PANEL_W, PANEL_H, 12)

    # totals
    fill(INK); textAlign(LEFT, TOP); textSize(16); textFont(UI_FONT)
    text("Total Points (days completed)", PANEL_X+14, PANEL_Y+12)
    textSize(14); y = PANEL_Y + 44
    for i,h in enumerate(habits):
        pts = sum(1 for v in habit_data[i][:days_in_month] if v)
        text("{}: {}".format(h, pts), PANEL_X+16, y); y += 24

    # motivational quote card 
    q = MONTH_QUOTES[month]
    fill(QUOTE_BG); stroke(GRID_BOLD); rect(QUOTE_X, QUOTE_Y, QUOTE_W, QUOTE_H, 10)
    noStroke(); fill(INK)
    textFont(QUOTE_FONT); textSize(16); textAlign(LEFT, TOP)
    qtxt = u"“{}”".format(q)
    draw_wrapped_text(qtxt, QUOTE_X+14, QUOTE_Y+12, QUOTE_W-28, line_h=20)
    textFont(UI_FONT)

def draw_progress():
    # progress bar 
    total = len(habits) * days_in_month
    done  = sum(sum(1 for v in row[:days_in_month] if v) for row in habit_data)
    pct   = 0 if total==0 else float(done)/total
    noStroke(); fill(240); rect(PROG_X, PROG_Y, PROG_W, PROG_H, 9)
    fill(GREEN); rect(PROG_X, PROG_Y, PROG_W*pct, PROG_H, 9)
    fill(INK); textAlign(CENTER, CENTER); textSize(13)
    text("{}% complete".format(int(pct*100)), PROG_X + PROG_W/2, PROG_Y + PROG_H/2)

def draw_reward():
    # interactive reward box (user writes end of month reward)
    fill(255); stroke(GRID_BOLD); rect(REWARD_X, REWARD_Y, REWARD_W, REWARD_H, 8)
    noStroke(); fill(245,248,252); rect(REWARD_X, REWARD_Y, REWARD_W, 34, 8,8,0,0)
    fill(INK); textAlign(LEFT, CENTER); textSize(18)
    text("End of Month Reward:", REWARD_X+12, REWARD_Y+17)
    global REWARD_BOUNDS
    REWARD_BOUNDS = (REWARD_X+12, REWARD_Y+40, REWARD_W-24, REWARD_H-50)
    x,y,w,h = REWARD_BOUNDS
    if focus_reward:
        noFill(); stroke(60,130,230); rect(x-4, y-4, w+8, h+8, 6)
    fill(INK); noStroke(); textSize(16); textLeading(20)
    draw_wrapped_text(reward_text, x, y, w, line_h=20, max_h=h)

# ------------------ VISUALISATION VIEW 
# Users monthly habit data tracked and visualised in a "Radial Ring Bloom'; Anaïs Nin 'habit wheel journaling'
def draw_visual_panel():
    noStroke(); fill(247,249,252); rect(VIS_X, VIS_Y, VIS_W, VIS_H, 14)
    fill(INK); textAlign(LEFT, TOP); textSize(18); textFont(UI_FONT)
    text("Visualising Your Monthly Habit Progress", VIS_X+18, VIS_Y+14)

    # compute ratios
    ratios, totals = [], []
    for i in range(len(habits)):
        pts = sum(1 for v in habit_data[i][:days_in_month] if v)
        totals.append(pts)
        ratios.append(0.0 if days_in_month==0 else float(pts)/days_in_month)

    # geometry 
    cx = VIS_X + VIS_W*0.60
    cy = VIS_Y + VIS_H*0.55
    base_r  = min(VIS_W, VIS_H)*0.26
    gap     = 18
    thick   = 12

    # full circles
    stroke(GRID); noFill(); strokeWeight(1.5)
    for i in range(len(habits)):
        r = base_r + i*gap
        ellipse(cx, cy, 2*r, 2*r)

    # arcs (arc length growth)
    strokeWeight(thick); strokeCap(SQUARE); noFill()
    for i,ratio in enumerate(ratios):
        r = base_r + i*gap
        col = RING_COLS[i % len(RING_COLS)]
        stroke(col)
        a0 = -HALF_PI
        a1 = a0 + ratio*TWO_PI
        arc(cx, cy, 2*r, 2*r, a0, a1)

    # legend left column
    lx = VIS_X + 24
    ly = VIS_Y + 56
    textSize(14); fill(INK); textAlign(LEFT, TOP); textFont(UI_FONT)
    for i,hname in enumerate(habits):
        col = RING_COLS[i % len(RING_COLS)]
        noStroke(); fill(col); rect(lx, ly + i*22 + 4, 12, 12, 3)
        fill(INK)
        text("{} ({} / {})".format(hname, totals[i], days_in_month), lx+20, ly + i*22)

# ------------------ TEXT WRAP 
def draw_wrapped_text(txt, x, y, w, line_h=18, max_h=None):
    pushStyle(); textAlign(LEFT, TOP)
    words = txt.split(' '); line = ""; ty = y
    for wd in words:
        test = (line + " " + wd) if line else wd
        if textWidth(test) > w:
            text(line, x, ty); ty += line_h
            if max_h is not None and ty > y + max_h - line_h: break
            line = wd
        else:
            line = test
    if line and (max_h is None or ty <= y + max_h - line_h): text(line, x, ty)
    popStyle()

# ------------------ INPUT 
# making everything work; useability
def mousePressed():
    global focus_reward, view_mode
    if adding_habit: return
    # tabs
    if hit(TAB_TRK_X, TAB_TRK_Y, TAB_TRK_W, TAB_H): view_mode="tracker"; return
    if hit(TAB_VIS_X, TAB_VIS_Y, TAB_VIS_W, TAB_H): view_mode="visuals"; return
    if view_mode=="visuals" and hit(SAVE_X, SAVE_Y, SAVE_W, SAVE_H):
        save_visual_png(); return

    # month + nav
    if hit(PREV_X, PREV_Y, 44, 30): prev_month(); return
    if hit(NEXT_X, NEXT_Y, 44, 30): next_month(); return

    if view_mode=="tracker":
        if hit(ADD_X, ADD_Y, BTN_W, BTN_H): start_add_habit(); return
        if hit(DEL_X, DEL_Y, BTN_W, BTN_H): delete_selected_habit(); return
        if grid_click(): return
        focus_reward = inside(REWARD_X+8, REWARD_Y+36, REWARD_W-16, REWARD_H-44)

def keyPressed():
    global reward_text, focus_reward, adding_habit, habit_input, view_mode
    if key == ESC:
        # prevent Processing from closing modal on ESC when we want to use it as cancel
        try:
            import builtins; builtins.key = 0
        except: pass
        if adding_habit: adding_habit = False
        else:
            save_grid(); save_notes(); exit()
        return

    if key in ['v','V']:
        view_mode = "visuals" if view_mode=="tracker" else "tracker"
        return

    if adding_habit:
        if key == BACKSPACE and len(habit_input)>0: habit_input = habit_input[:-1]
        elif key == ENTER or key == RETURN: finish_add_habit()
        elif key != CODED and len(habit_input) < 28: habit_input += str(key)
        return

    if view_mode=="tracker":
        if focus_reward:
            if key == BACKSPACE and len(reward_text)>0: reward_text = reward_text[:-1]
            elif key == ENTER or key == RETURN: reward_text += "\n"
            elif key != CODED and len(reward_text) < 600: reward_text += str(key)
            return

        if keyCode == UP:    selected[0] = (selected[0]-1) % len(habits)
        elif keyCode == DOWN:selected[0] = (selected[0]+1) % len(habits)
        elif keyCode == LEFT:selected[1] = (selected[1]-1) % days_in_month
        elif keyCode == RIGHT:selected[1] = (selected[1]+1) % days_in_month
        elif key == ' ':
            r,c = selected
            if 0<=r<len(habits) and 0<=c<days_in_month: habit_data[r][c] = not habit_data[r][c]
        elif key in ['s','S']: save_grid(); save_notes()
        elif key == ',': prev_month()
        elif key == '.': next_month()
        elif key == '+': start_add_habit()
        elif key == '-': delete_selected_habit()

def grid_click():
    row_h, col_w, cols = GRID_GEO
    if not inside(GRID_X, GRID_Y, GRID_W, GRID_H): return False
    if mouseY < GRID_Y + row_h: return False
    if GRID_X <= mouseX <= GRID_X + LEFT_W:
        r = int((mouseY - GRID_Y) // row_h) - 1
        if 0 <= r < len(habits): selected[0] = r; return True
    r = int((mouseY - GRID_Y) // row_h) - 1
    c = int((mouseX - (GRID_X + LEFT_W)) // col_w)
    if 0 <= r < len(habits) and 0 <= c < cols:
        habit_data[r][c] = not habit_data[r][c]
        selected[:] = [r, c]; return True
    return False

def start_add_habit():
    global adding_habit, habit_input
    adding_habit = True; habit_input = ""

def finish_add_habit():
    global adding_habit, habit_input, habits, habit_data, selected
    name = habit_input.strip()
    if name:
        habits.append(name)
        habit_data.append([False for _ in range(max_days)])
        selected[0] = len(habits)-1
    adding_habit = False; habit_input = ""

def delete_selected_habit():
    if len(habits) <= 1: return
    r = max(0, min(selected[0], len(habits)-1))
    habits.pop(r); habit_data.pop(r)
    selected[0] = max(0, r-1); selected[1] = 0

# ------------------ SAVE / LOAD 
def update_filenames():
    global gridfile, notesfile, days_in_month
    gridfile  = "habit_grid_%d_%02d.csv"  % (year, month)
    notesfile = "habit_notes_%d_%02d.txt" % (year, month)
    days_in_month = calendar.monthrange(year, month)[1]

def save_grid():
    try:
        with open(gridfile, "w") as f:
            f.write("{},{},{}\n".format(month, year, days_in_month))
            for r,h in enumerate(habits):
                vals = ",".join("1" if v else "0" for v in habit_data[r][:days_in_month])
                f.write(h + "," + vals + "\n")
        print("Saved grid:", gridfile)
    except Exception as e:
        print("Save error:", e)

def load_grid():
    """Start fresh for this month; then overwrite if file exists."""
    global habits, habit_data
    habits = list(STANDARD_HABITS)
    habit_data = [[False for _ in range(max_days)] for _ in range(len(habits))]
    try:
        with open(gridfile, "r") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        if not lines: return
        rows = lines[1:]
        habits[:] = []
        habit_data[:] = []
        for line in rows:
            items = line.split(",")
            label, vals = items[0], items[1:]
            habits.append(label)
            row = [ (v=="1") for v in vals ]
            row += [False]*(max_days-len(row))
            habit_data.append(row[:max_days])
        print("Loaded grid:", gridfile)
    except:
        # if no file for this month, keep defaults
        pass

def save_notes():
    try:
        with open(notesfile, "w") as nf:
            nf.write("REWARD\n" + reward_text.strip() + "\n")
            nf.write("QUOTE\n" + MONTH_QUOTES[month] + "\n")
        print("Saved notes:", notesfile)
    except Exception as e:
        print("Notes save error:", e)

def load_notes():
    global reward_text
    reward_text = ""
    try:
        with open(notesfile, "r") as nf:
            lines = [ln.rstrip("\n") for ln in nf]
        block = None; buf=[]
        for line in lines:
            if line == "REWARD":
                if block and buf: apply_block(block, buf); buf=[]
                block="REWARD"
            elif line == "QUOTE":
                if block and buf: apply_block(block, buf); buf=[]
                block="QUOTE"
            else:
                buf.append(line)
        if block and buf: apply_block(block, buf)
    except:
        pass

def apply_block(kind, buf):
    global reward_text
    txt = "\n".join(buf).strip()
    if kind=="REWARD": reward_text = txt

def prev_month():
    global month, year
    save_grid(); save_notes()
    month -= 1
    if month < 1: month = 12; year -= 1
    update_filenames(); load_grid(); load_notes()
    selected[1] = min(selected[1], days_in_month-1)

def next_month():
    global month, year
    save_grid(); save_notes()
    month += 1
    if month > 12: month = 1; year += 1
    update_filenames(); load_grid(); load_notes()
    selected[1] = min(selected[1], days_in_month-1)

# ------------------ PNG EXPORT (visualisation tab) 
def save_visual_png():
    fname = "visual_%d_%02d.png" % (year, month)
    g = createGraphics(int(VIS_W), int(VIS_H))
    g.beginDraw()
    # background panel
    g.background(247,249,252)
    # title
    g.fill(36,52,72); g.textAlign(LEFT, TOP); g.textSize(18)
    g.text("Visualising Your Monthly Habit Progress", 18, 14)

    # compute
    ratios = []
    totals = []
    for i in range(len(habits)):
        pts = sum(1 for v in habit_data[i][:days_in_month] if v)
        totals.append(pts)
        ratios.append(0.0 if days_in_month==0 else float(pts)/days_in_month)

    cx, cy = VIS_W*0.60, VIS_H*0.55
    base_r, gap, thick = min(VIS_W, VIS_H)*0.26, 18, 12

    # faint circles
    g.stroke(210,215,220); g.noFill(); g.strokeWeight(1.5)
    for i in range(len(habits)):
        r = base_r + i*gap
        g.ellipse(cx, cy, 2*r, 2*r)

    # arcs
    g.noFill(); g.strokeWeight(thick); g.strokeCap(SQUARE)
    for i,ratio in enumerate(ratios):
        r = base_r + i*gap
        col = RING_COLS[i % len(RING_COLS)]
        g.stroke(red(col), green(col), blue(col))
        a0 = -HALF_PI
        a1 = a0 + ratio*TWO_PI
        g.arc(cx, cy, 2*r, 2*r, a0, a1)

    # legend
    g.fill(36,52,72); g.textSize(14); g.textAlign(LEFT, TOP)
    lx, ly = 24, 56
    for i,hname in enumerate(habits):
        col = RING_COLS[i % len(RING_COLS)]
        g.noStroke(); g.fill(red(col), green(col), blue(col))
        g.rect(lx, ly + i*22 + 4, 12, 12, 3)
        g.fill(36,52,72)
        g.text("{} ({} / {})".format(hname, totals[i], days_in_month), lx+20, ly + i*22)

    g.endDraw()
    g.save(fname)
    print("Saved visual:", fname)

# ------------------ UTILS 
def draw_add_popup():
    noStroke(); fill(0,0,0,80); rect(0,0,width,height)
    cx, cy, cw, ch = width/2-220, height/2-80, 440, 160
    fill(255); stroke(GRID_BOLD); rect(cx, cy, cw, ch, 10)
    fill(INK); noStroke(); textAlign(CENTER, CENTER); textSize(18)
    text("New habit name", cx+cw/2, cy+28)
    ix, iy, iw, ih = cx+20, cy+58, cw-40, 36
    noFill(); stroke(60,130,230); rect(ix, iy, iw, ih, 6)
    noStroke(); fill(INK); textAlign(LEFT, CENTER); textSize(18)
    disp = habit_input + ("|" if (frameCount//30)%2==0 else "")
    text(disp[:28], ix+10, iy+ih/2)
    textAlign(CENTER, CENTER); fill(INK); textSize(13)
    text("Enter to add  |  Esc to cancel", cx+cw/2, cy+ch-20)

def hit(x,y,w,h): return x<=mouseX<=x+w and y<=mouseY<=y+h
def inside(x,y,w,h): return x<=mouseX<=x+w and y<=mouseY<=y+h
