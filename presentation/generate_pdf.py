"""
WorkHere PDF Presentation — Final Professional Version
- SVG icons instead of emojis
- Proper spacing
- Clean design
"""

from weasyprint import HTML
from pathlib import Path
import base64

# ═══════════════════════════════════════════════════════════════
# LOAD LOGO AS BASE64
# ═══════════════════════════════════════════════════════════════

LOGO_PATH = Path(__file__).parent.parent / "bot" / "assets" / "logo.png"
if LOGO_PATH.exists():
    LOGO_B64 = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    LOGO_SRC = f"data:image/png;base64,{LOGO_B64}"
else:
    LOGO_SRC = ""

# ═══════════════════════════════════════════════════════════════
# SVG ICONS
# ═══════════════════════════════════════════════════════════════

ICONS = {
    'database': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="8" y="10" width="32" height="28" rx="4" stroke="currentColor" stroke-width="2.5"/>
        <line x1="8" y1="20" x2="40" y2="20" stroke="currentColor" stroke-width="2.5"/>
        <line x1="8" y1="30" x2="40" y2="30" stroke="currentColor" stroke-width="2.5"/>
        <circle cx="14" cy="15" r="2" fill="currentColor"/>
        <circle cx="14" cy="25" r="2" fill="currentColor"/>
        <circle cx="14" cy="35" r="2" fill="currentColor"/>
    </svg>''',
    
    'chart': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 40V16L16 24L24 12L32 20L40 8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="40" cy="8" r="3" fill="currentColor"/>
    </svg>''',
    
    'clock': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="24" r="18" stroke="currentColor" stroke-width="2.5"/>
        <path d="M24 14V24L30 30" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </svg>''',
    
    'users': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="16" r="8" stroke="currentColor" stroke-width="2.5"/>
        <path d="M8 42C8 34 14 28 24 28C34 28 40 34 40 42" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </svg>''',
    
    'shield': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M24 4L40 10V22C40 32 32 40 24 44C16 40 8 32 8 22V10L24 4Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M18 24L22 28L30 20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>''',
    
    'lock': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="20" width="28" height="22" rx="4" stroke="currentColor" stroke-width="2.5"/>
        <path d="M16 20V14C16 9.58 19.58 6 24 6C28.42 6 32 9.58 32 14V20" stroke="currentColor" stroke-width="2.5"/>
        <circle cx="24" cy="31" r="3" fill="currentColor"/>
    </svg>''',
    
    'link': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 28L28 20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M26 32L30 28C34 24 34 18 30 14C26 10 20 10 16 14L12 18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M22 16L18 20C14 24 14 30 18 34C22 38 28 38 32 34L36 30" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </svg>''',
    
    'brain': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M24 42V26" stroke="currentColor" stroke-width="2.5"/>
        <circle cx="16" cy="14" r="8" stroke="currentColor" stroke-width="2.5"/>
        <circle cx="32" cy="14" r="8" stroke="currentColor" stroke-width="2.5"/>
        <path d="M16 22C16 26 20 30 24 30C28 30 32 26 32 22" stroke="currentColor" stroke-width="2.5"/>
    </svg>''',
    
    'target': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="24" r="18" stroke="currentColor" stroke-width="2.5"/>
        <circle cx="24" cy="24" r="10" stroke="currentColor" stroke-width="2.5"/>
        <circle cx="24" cy="24" r="3" fill="currentColor"/>
    </svg>''',
    
    'search': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="20" r="12" stroke="currentColor" stroke-width="2.5"/>
        <path d="M30 30L40 40" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </svg>''',
    
    'list': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="8" y="10" width="32" height="28" rx="4" stroke="currentColor" stroke-width="2.5"/>
        <path d="M14 18H34M14 24H34M14 30H26" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </svg>''',
    
    'document': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 8H28L36 16V40C36 41.1 35.1 42 34 42H12C10.9 42 10 41.1 10 40V10C10 8.9 10.9 8 12 8Z" stroke="currentColor" stroke-width="2.5"/>
        <path d="M28 8V16H36" stroke="currentColor" stroke-width="2.5"/>
        <path d="M16 24H32M16 30H32M16 36H24" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </svg>''',
    
    'message': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 12H40V34H26L18 42V34H8V12Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M16 20H32M16 26H26" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </svg>''',
    
    'rocket': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M24 6C24 6 36 12 36 28L24 38L12 28C12 12 24 6 24 6Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
        <circle cx="24" cy="20" r="4" stroke="currentColor" stroke-width="2.5"/>
        <path d="M12 28L6 34M36 28L42 34" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
    </svg>''',
    
    'check': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="24" r="18" stroke="currentColor" stroke-width="2.5"/>
        <path d="M16 24L22 30L32 18" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>''',
    
    'globe': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="24" r="18" stroke="currentColor" stroke-width="2.5"/>
        <ellipse cx="24" cy="24" rx="8" ry="18" stroke="currentColor" stroke-width="2.5"/>
        <path d="M6 24H42" stroke="currentColor" stroke-width="2.5"/>
    </svg>''',
    
    'mail': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="6" y="12" width="36" height="24" rx="4" stroke="currentColor" stroke-width="2.5"/>
        <path d="M6 16L24 28L42 16" stroke="currentColor" stroke-width="2.5"/>
    </svg>''',
    
    'phone': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 6H18L22 14L17 18C19 24 24 29 30 31L34 26L42 30V36C42 39 39 42 36 42C20 41 7 28 6 12C6 9 9 6 12 6Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
    </svg>''',
    
    'telegram': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 24L18 28L22 38L28 30L40 38L44 8L6 24Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
        <path d="M18 28L36 14" stroke="currentColor" stroke-width="2.5"/>
    </svg>''',
    
    'star': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M24 6L29 18H42L32 27L36 40L24 32L12 40L16 27L6 18H19L24 6Z" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/>
    </svg>''',
    
    'speed': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 34C8 22 14 12 24 12C34 12 40 22 40 34" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M24 34L32 20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="24" cy="34" r="4" fill="currentColor"/>
    </svg>''',
    
    'audit': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="10" y="6" width="28" height="36" rx="4" stroke="currentColor" stroke-width="2.5"/>
        <path d="M16 16H32M16 24H32M16 32H24" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="36" cy="36" r="8" fill="white" stroke="currentColor" stroke-width="2.5"/>
        <path d="M34 36L36 38L40 34" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>''',
    
    'russia': '''<svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="6" y="12" width="36" height="8" fill="#FFFFFF" stroke="currentColor" stroke-width="1"/>
        <rect x="6" y="20" width="36" height="8" fill="#0039A6" stroke="currentColor" stroke-width="1"/>
        <rect x="6" y="28" width="36" height="8" fill="#D52B1E" stroke="currentColor" stroke-width="1"/>
    </svg>''',
}

def icon(name, size=48, color="#4F6AF5"):
    svg = ICONS.get(name, ICONS['check'])
    svg = svg.replace('width="48"', f'width="{size}"')
    svg = svg.replace('height="48"', f'height="{size}"')
    svg = svg.replace('currentColor', color)
    return svg

# ═══════════════════════════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════════════════════════

C = {
    'primary': '#4F6AF5',
    'primary_light': '#EEF1FE',
    'accent': '#10B981',
    'accent_light': '#ECFDF5',
    'warning': '#F59E0B',
    'dark': '#111827',
    'text': '#374151',
    'muted': '#6B7280',
    'light': '#9CA3AF',
    'border': '#E5E7EB',
    'bg': '#F9FAFB',
    'white': '#FFFFFF',
}

# ═══════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════

CSS = f"""
@page {{
    size: 297mm 210mm;
    margin: 0;
}}

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: {C['text']};
}}

/* ═══════════════════════════════════════════════════════════════
   SLIDE
   ═══════════════════════════════════════════════════════════════ */

.slide {{
    width: 297mm;
    height: 210mm;
    padding: 20mm 25mm 18mm 25mm;
    page-break-after: always;
    position: relative;
    background: {C['white']};
}}

.slide:last-child {{
    page-break-after: avoid;
}}

.slide-dark {{
    background: {C['dark']};
    color: {C['white']};
}}

.slide-primary {{
    background: {C['primary']};
    color: {C['white']};
}}

.slide-gradient {{
    background: linear-gradient(135deg, {C['primary']} 0%, #6366F1 100%);
    color: {C['white']};
}}

/* ═══════════════════════════════════════════════════════════════
   TYPOGRAPHY
   ═══════════════════════════════════════════════════════════════ */

.tag {{
    display: inline-block;
    font-size: 8pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {C['primary']};
    margin-bottom: 5mm;
}}

.tag-light {{
    color: rgba(255,255,255,0.7);
}}

h1 {{
    font-size: 44pt;
    font-weight: 700;
    line-height: 1.1;
    letter-spacing: -1px;
    margin-bottom: 8mm;
}}

h2 {{
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: -0.5px;
    margin-bottom: 12mm;
    color: {C['dark']};
}}

.slide-dark h2,
.slide-primary h2,
.slide-gradient h2 {{
    color: {C['white']};
}}

h3 {{
    font-size: 13pt;
    font-weight: 600;
    margin-bottom: 4mm;
    color: {C['dark']};
}}

h4 {{
    font-size: 11pt;
    font-weight: 600;
    margin-bottom: 3mm;
    color: {C['dark']};
}}

p {{
    font-size: 10pt;
    line-height: 1.6;
    color: {C['muted']};
}}

.text-sm {{ font-size: 9pt; }}
.text-xs {{ font-size: 8pt; }}
.text-lg {{ font-size: 12pt; }}
.text-muted {{ color: {C['muted']}; }}
.text-light {{ color: {C['light']}; }}
.text-primary {{ color: {C['primary']}; }}
.text-accent {{ color: {C['accent']}; }}
.text-white {{ color: {C['white']}; }}
.text-center {{ text-align: center; }}

/* ═══════════════════════════════════════════════════════════════
   LAYOUT
   ═══════════════════════════════════════════════════════════════ */

.row {{
    display: table;
    width: 100%;
    table-layout: fixed;
}}

.col {{
    display: table-cell;
    vertical-align: top;
}}

.col-2 {{ width: 50%; }}
.col-3 {{ width: 33.333%; }}
.col-4 {{ width: 25%; }}

.gap-sm > .col {{ padding-right: 4mm; }}
.gap-md > .col {{ padding-right: 6mm; }}
.gap-lg > .col {{ padding-right: 10mm; }}
.gap-sm > .col:last-child,
.gap-md > .col:last-child,
.gap-lg > .col:last-child {{ padding-right: 0; }}

.valign-middle {{ vertical-align: middle; }}

/* ═══════════════════════════════════════════════════════════════
   SPACING
   ═══════════════════════════════════════════════════════════════ */

.mb-0 {{ margin-bottom: 0; }}
.mb-1 {{ margin-bottom: 2mm; }}
.mb-2 {{ margin-bottom: 4mm; }}
.mb-3 {{ margin-bottom: 6mm; }}
.mb-4 {{ margin-bottom: 10mm; }}
.mb-5 {{ margin-bottom: 15mm; }}

.mt-1 {{ margin-top: 2mm; }}
.mt-2 {{ margin-top: 4mm; }}
.mt-3 {{ margin-top: 6mm; }}
.mt-4 {{ margin-top: 10mm; }}
.mt-5 {{ margin-top: 15mm; }}

.pt-4 {{ padding-top: 10mm; }}
.pt-5 {{ padding-top: 15mm; }}

/* ═══════════════════════════════════════════════════════════════
   CARDS
   ═══════════════════════════════════════════════════════════════ */

.card {{
    background: {C['white']};
    border: 1px solid {C['border']};
    border-radius: 3mm;
    padding: 5mm;
    margin-bottom: 4mm;
}}

.card-filled {{
    background: {C['bg']};
    border: none;
}}

.card-primary {{
    background: {C['primary_light']};
    border: 1px solid {C['primary']};
}}

.card-dark {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
}}

.card-accent {{
    background: {C['primary']};
    color: {C['white']};
    border: none;
}}

.card-accent h3,
.card-accent h4 {{
    color: {C['white']};
}}

.card-accent p {{
    color: rgba(255,255,255,0.85);
}}

/* ═══════════════════════════════════════════════════════════════
   ICON BOX
   ═══════════════════════════════════════════════════════════════ */

.icon-box {{
    display: inline-block;
    margin-bottom: 4mm;
}}

.icon-box svg {{
    display: block;
}}

/* ═══════════════════════════════════════════════════════════════
   LISTS
   ═══════════════════════════════════════════════════════════════ */

ul {{
    list-style: none;
    margin: 0;
    padding: 0;
}}

li {{
    padding: 2mm 0 2mm 5mm;
    position: relative;
    font-size: 10pt;
    line-height: 1.5;
    color: {C['text']};
}}

li::before {{
    content: '';
    position: absolute;
    left: 0;
    top: 4mm;
    width: 1.5mm;
    height: 1.5mm;
    background: {C['primary']};
    border-radius: 50%;
}}

.list-check li::before {{
    content: '✓';
    width: auto;
    height: auto;
    background: none;
    color: {C['accent']};
    font-size: 9pt;
    font-weight: 700;
    top: 2mm;
    left: 0;
}}

.list-check li {{
    padding-left: 5mm;
}}

/* ═══════════════════════════════════════════════════════════════
   STEPS
   ═══════════════════════════════════════════════════════════════ */

.steps {{
    display: table;
    width: 100%;
    table-layout: fixed;
    border-collapse: separate;
    border-spacing: 2mm 0;
}}

.step {{
    display: table-cell;
    text-align: center;
    padding: 5mm 2mm;
    background: {C['bg']};
    border-radius: 2mm;
    vertical-align: top;
}}

.step-active {{
    background: {C['primary_light']};
    border: 1px solid {C['primary']};
}}

.step-num {{
    font-size: 18pt;
    font-weight: 700;
    color: {C['primary']};
    margin-bottom: 2mm;
}}

.step-title {{
    font-size: 9pt;
    font-weight: 600;
    color: {C['dark']};
    margin-bottom: 1mm;
}}

.step-desc {{
    font-size: 8pt;
    color: {C['muted']};
}}

/* ═══════════════════════════════════════════════════════════════
   STATS
   ═══════════════════════════════════════════════════════════════ */

.stat {{
    text-align: center;
    padding: 4mm 0;
}}

.stat-value {{
    font-size: 32pt;
    font-weight: 700;
    color: {C['primary']};
    line-height: 1;
    margin-bottom: 2mm;
}}

.stat-label {{
    font-size: 9pt;
    color: {C['muted']};
}}

/* ═══════════════════════════════════════════════════════════════
   PRICING
   ═══════════════════════════════════════════════════════════════ */

.pricing {{
    text-align: center;
    padding: 6mm 4mm;
    border: 1px solid {C['border']};
    border-radius: 3mm;
}}

.pricing-featured {{
    border: 2px solid {C['primary']};
    background: {C['primary_light']};
}}

.pricing-accent {{
    border-color: {C['accent']};
}}

.price {{
    font-size: 24pt;
    font-weight: 700;
    color: {C['primary']};
    margin-bottom: 1mm;
}}

.price-period {{
    font-size: 9pt;
    color: {C['muted']};
    margin-bottom: 4mm;
}}

/* ═══════════════════════════════════════════════════════════════
   BADGES
   ═══════════════════════════════════════════════════════════════ */

.badge {{
    display: inline-block;
    padding: 1mm 3mm;
    border-radius: 1.5mm;
    font-size: 8pt;
    font-weight: 600;
    margin: 0.5mm;
}}

.badge-primary {{
    background: {C['primary']};
    color: {C['white']};
}}

.badge-accent {{
    background: {C['accent']};
    color: {C['white']};
}}

/* ═══════════════════════════════════════════════════════════════
   FOOTER
   ═══════════════════════════════════════════════════════════════ */

.footer {{
    position: absolute;
    bottom: 8mm;
    left: 25mm;
    right: 25mm;
}}

.footer-inner {{
    display: table;
    width: 100%;
}}

.footer-left {{
    display: table-cell;
    text-align: left;
    vertical-align: middle;
}}

.footer-right {{
    display: table-cell;
    text-align: right;
    vertical-align: middle;
    font-size: 9pt;
    color: {C['light']};
}}

.logo {{
    height: 6mm;
}}

/* ═══════════════════════════════════════════════════════════════
   INTEGRATION BADGES
   ═══════════════════════════════════════════════════════════════ */

.int-badge {{
    display: inline-block;
    padding: 2mm 4mm;
    border-radius: 2mm;
    font-size: 9pt;
    font-weight: 600;
    color: {C['white']};
    margin: 1mm;
}}

/* ═══════════════════════════════════════════════════════════════
   FUNNEL
   ═══════════════════════════════════════════════════════════════ */

.funnel-row {{
    margin-bottom: 2mm;
}}

.funnel-bar {{
    height: 7mm;
    background: linear-gradient(90deg, {C['primary']} 0%, #6366F1 100%);
    border-radius: 1mm;
    color: {C['white']};
    font-size: 8pt;
    font-weight: 500;
    line-height: 7mm;
    padding: 0 3mm;
}}

/* ═══════════════════════════════════════════════════════════════
   MOCKUP
   ═══════════════════════════════════════════════════════════════ */

.mockup {{
    background: {C['dark']};
    border-radius: 3mm;
    padding: 4mm;
    overflow: hidden;
}}

.mockup-dots {{
    margin-bottom: 3mm;
}}

.mockup-dot {{
    display: inline-block;
    width: 2.5mm;
    height: 2.5mm;
    border-radius: 50%;
    margin-right: 1.5mm;
}}

.mockup-card {{
    background: rgba(255,255,255,0.08);
    padding: 3mm;
    border-radius: 2mm;
    margin-bottom: 2mm;
}}

.mockup-card:last-child {{
    margin-bottom: 0;
}}

.mockup-avatar {{
    display: inline-block;
    width: 8mm;
    height: 8mm;
    background: {C['primary']};
    border-radius: 2mm;
    color: {C['white']};
    text-align: center;
    line-height: 8mm;
    font-size: 8pt;
    font-weight: 700;
    margin-right: 3mm;
    vertical-align: middle;
}}

.mockup-info {{
    display: inline-block;
    vertical-align: middle;
}}

.mockup-name {{
    font-size: 9pt;
    font-weight: 600;
    color: {C['white']};
}}

.mockup-role {{
    font-size: 7pt;
    color: rgba(255,255,255,0.5);
}}

.mockup-status {{
    float: right;
    padding: 1mm 2mm;
    border-radius: 1mm;
    font-size: 7pt;
    font-weight: 600;
}}

.status-green {{ background: rgba(16,185,129,0.2); color: #10B981; }}
.status-yellow {{ background: rgba(245,158,11,0.2); color: #F59E0B; }}
.status-blue {{ background: rgba(79,106,245,0.2); color: #4F6AF5; }}
"""

# ═══════════════════════════════════════════════════════════════
# HTML
# ═══════════════════════════════════════════════════════════════

HTML_CONTENT = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>WorkHere — Презентация</title>
<style>{CSS}</style>
</head>
<body>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 1: TITLE
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-dark">
    <div class="pt-5">
        <p class="tag tag-light">ATS + CRM для рекрутинга</p>
        <h1>WorkHere</h1>
        <p class="text-lg mb-5" style="color: rgba(255,255,255,0.7); max-width: 180mm;">
            Система управления наймом, которая закрывает вакансии быстрее
        </p>
        
        <div class="row gap-lg" style="max-width: 160mm;">
            <div class="col col-3">
                <div class="stat-value" style="color: #fff;">8 500+</div>
                <p class="text-sm" style="color: rgba(255,255,255,0.5);">компаний</p>
            </div>
            <div class="col col-3">
                <div class="stat-value" style="color: #fff;">350+</div>
                <p class="text-sm" style="color: rgba(255,255,255,0.5);">городов России</p>
            </div>
            <div class="col col-3">
                <div class="stat-value" style="color: #fff;">3</div>
                <p class="text-sm" style="color: rgba(255,255,255,0.5);">года на рынке</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">
                <img src="{LOGO_SRC}" class="logo" style="filter: brightness(0) invert(1);">
            </div>
            <div class="footer-right" style="color: rgba(255,255,255,0.4);">1</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 2: PROBLEM
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Проблема</p>
    <h2>С чем сталкиваются HR-команды</h2>
    
    <div class="row gap-md">
        <div class="col col-3">
            <div class="card card-filled">
                <div class="icon-box">{icon('database', 36)}</div>
                <h4>Хаос в данных</h4>
                <p class="text-sm">Кандидаты разбросаны по Excel, почте, мессенджерам. Дубли, потери, путаница.</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled">
                <div class="icon-box">{icon('clock', 36)}</div>
                <h4>Долгое закрытие</h4>
                <p class="text-sm">Нет контроля сроков и SLA. Кандидаты уходят к конкурентам.</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled">
                <div class="icon-box">{icon('chart', 36)}</div>
                <h4>Нет аналитики</h4>
                <p class="text-sm">Непонятно, какие источники работают и где теряются кандидаты.</p>
            </div>
        </div>
    </div>
    
    <div class="row gap-md mt-3">
        <div class="col col-3">
            <div class="card card-filled">
                <div class="icon-box">{icon('lock', 36)}</div>
                <h4>Риски ПДн</h4>
                <p class="text-sm">Согласия не собираются, нет контроля доступа, 152-ФЗ под вопросом.</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled">
                <div class="icon-box">{icon('list', 36)}</div>
                <h4>Рутина</h4>
                <p class="text-sm">80% времени уходит на ручные операции вместо работы с людьми.</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled">
                <div class="icon-box">{icon('link', 36)}</div>
                <h4>Разрозненные инструменты</h4>
                <p class="text-sm">CRM, почта, мессенджеры — всё отдельно, нет единой картины.</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">2</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 3: SOLUTION
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-gradient text-center">
    <div class="pt-5">
        <p class="tag tag-light">Решение</p>
        <h2 style="font-size: 32pt; margin-bottom: 15mm;">
            Одна система для всего<br>процесса найма
        </h2>
        
        <div style="background: rgba(255,255,255,0.15); padding: 8mm 15mm; border-radius: 4mm; display: inline-block; margin-bottom: 12mm;">
            <img src="{LOGO_SRC}" style="height: 12mm; filter: brightness(0) invert(1);">
        </div>
        
        <p style="color: rgba(255,255,255,0.8); font-size: 12pt; max-width: 160mm; margin: 0 auto;">
            От заявки на подбор до выхода сотрудника —<br>
            всё в одном месте, под контролем, с аналитикой
        </p>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo" style="filter: brightness(0) invert(1);"></div>
            <div class="footer-right" style="color: rgba(255,255,255,0.4);">3</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 4: AUDIENCE
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Аудитория</p>
    <h2>Для всех участников найма</h2>
    
    <div class="row gap-md">
        <div class="col col-4">
            <div class="card" style="min-height: 48mm;">
                <div class="icon-box">{icon('users', 32)}</div>
                <h4>Рекрутер</h4>
                <ul class="list-check text-sm">
                    <li>Единая база кандидатов</li>
                    <li>Автоматизация рутины</li>
                    <li>Шаблоны сообщений</li>
                </ul>
            </div>
        </div>
        <div class="col col-4">
            <div class="card card-accent" style="min-height: 48mm;">
                <div class="icon-box">{icon('target', 32, '#fff')}</div>
                <h4>Руководитель подбора</h4>
                <ul class="list-check text-sm">
                    <li style="color: rgba(255,255,255,0.9);">Контроль SLA и сроков</li>
                    <li style="color: rgba(255,255,255,0.9);">Аналитика команды</li>
                    <li style="color: rgba(255,255,255,0.9);">Отчёты для топов</li>
                </ul>
            </div>
        </div>
        <div class="col col-4">
            <div class="card" style="min-height: 48mm;">
                <div class="icon-box">{icon('message', 32)}</div>
                <h4>Нанимающий менеджер</h4>
                <ul class="list-check text-sm">
                    <li>Просмотр кандидатов</li>
                    <li>Быстрый фидбек</li>
                    <li>Уведомления</li>
                </ul>
            </div>
        </div>
        <div class="col col-4">
            <div class="card" style="min-height: 48mm;">
                <div class="icon-box">{icon('chart', 32)}</div>
                <h4>HRD / Бизнес</h4>
                <ul class="list-check text-sm">
                    <li>Стоимость найма</li>
                    <li>Прогнозирование</li>
                    <li>Unit-экономика</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">4</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 5: FUNNEL
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Процесс</p>
    <h2>Полный цикл найма</h2>
    
    <div class="steps">
        <div class="step">
            <div class="step-num">01</div>
            <div class="step-title">Заявка</div>
            <div class="step-desc">От менеджера</div>
        </div>
        <div class="step">
            <div class="step-num">02</div>
            <div class="step-title">Публикация</div>
            <div class="step-desc">На job-сайтах</div>
        </div>
        <div class="step">
            <div class="step-num">03</div>
            <div class="step-title">Отклики</div>
            <div class="step-desc">Единый поток</div>
        </div>
        <div class="step">
            <div class="step-num">04</div>
            <div class="step-title">Скрининг</div>
            <div class="step-desc">Отбор + AI</div>
        </div>
        <div class="step">
            <div class="step-num">05</div>
            <div class="step-title">Интервью</div>
            <div class="step-desc">Оценка</div>
        </div>
        <div class="step step-active">
            <div class="step-num">06</div>
            <div class="step-title">Оффер</div>
            <div class="step-desc">Выход</div>
        </div>
    </div>
    
    <div class="card card-primary mt-4" style="padding: 4mm 6mm;">
        <p class="text-sm mb-0"><strong>Ключевое:</strong> контроль на каждом этапе с SLA и автоматическими напоминаниями</p>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">5</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 6: DATABASE
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Возможности</p>
    <h2>Единая база кандидатов</h2>
    
    <div class="row gap-lg">
        <div class="col col-2">
            <ul class="list-check">
                <li>Все резюме в одном месте</li>
                <li>Полная история взаимодействий</li>
                <li>Комментарии и теги</li>
                <li>Умный поиск по тексту</li>
                <li>Защита от дублей</li>
                <li>Слияние карточек</li>
            </ul>
            
            <div class="card card-primary mt-4" style="padding: 4mm 5mm;">
                <p class="text-sm mb-0"><strong>Результат:</strong> ни один кандидат не теряется</p>
            </div>
        </div>
        <div class="col col-2">
            <div class="mockup">
                <div class="mockup-dots">
                    <span class="mockup-dot" style="background: #ff5f57;"></span>
                    <span class="mockup-dot" style="background: #febc2e;"></span>
                    <span class="mockup-dot" style="background: #28c840;"></span>
                </div>
                <div class="mockup-card">
                    <span class="mockup-avatar">АИ</span>
                    <span class="mockup-info">
                        <span class="mockup-name">Алексей Иванов</span><br>
                        <span class="mockup-role">Senior Developer</span>
                    </span>
                    <span class="mockup-status status-green">Оффер</span>
                </div>
                <div class="mockup-card">
                    <span class="mockup-avatar">МП</span>
                    <span class="mockup-info">
                        <span class="mockup-name">Мария Петрова</span><br>
                        <span class="mockup-role">Product Manager</span>
                    </span>
                    <span class="mockup-status status-yellow">Интервью</span>
                </div>
                <div class="mockup-card">
                    <span class="mockup-avatar">ДС</span>
                    <span class="mockup-info">
                        <span class="mockup-name">Дмитрий Сидоров</span><br>
                        <span class="mockup-role">UX Designer</span>
                    </span>
                    <span class="mockup-status status-blue">Скрининг</span>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">6</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 7: INTEGRATIONS
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Интеграции</p>
    <h2>Подключено к экосистеме</h2>
    
    <div class="row gap-lg">
        <div class="col col-2">
            <h4 class="mb-2">Job-сайты</h4>
            <div class="mb-4">
                <span class="int-badge" style="background: #d6001c;">HeadHunter</span>
                <span class="int-badge" style="background: #00a859;">Авито</span>
                <span class="int-badge" style="background: #ff6600;">SuperJob</span>
                <span class="int-badge" style="background: #0066cc;">Работа.ру</span>
            </div>
            
            <h4 class="mb-2">Мессенджеры</h4>
            <div class="mb-4">
                <span class="int-badge" style="background: #0088cc;">Telegram</span>
                <span class="int-badge" style="background: #25d366;">WhatsApp</span>
                <span class="int-badge" style="background: #7360f2;">Viber</span>
            </div>
        </div>
        <div class="col col-2">
            <h4 class="mb-2">Видеозвонки</h4>
            <div class="mb-4">
                <span class="int-badge" style="background: #fc3f1d;">Яндекс.Телемост</span>
            </div>
            
            <h4 class="mb-2">Корпоративные</h4>
            <div class="mb-4">
                <span class="int-badge" style="background: #ffcc00; color: #000;">1С:Предприятие</span>
                <span class="int-badge" style="background: #333;">Open API</span>
            </div>
            
            <div class="card card-filled mt-2" style="padding: 4mm;">
                <p class="text-sm mb-0">Чаты HH и Авито прямо в системе</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">7</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 8: AI
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-dark">
    <p class="tag tag-light">AI-модуль</p>
    <h2>Искусственный интеллект в найме</h2>
    
    <div class="row gap-md">
        <div class="col col-4">
            <div class="card-dark" style="padding: 5mm;">
                <div class="icon-box">{icon('search', 32, '#fff')}</div>
                <h4 style="color: #fff;">Умный поиск</h4>
                <p class="text-sm" style="color: rgba(255,255,255,0.6);">Семантический поиск по базе, синонимы</p>
            </div>
        </div>
        <div class="col col-4">
            <div class="card-dark" style="padding: 5mm;">
                <div class="icon-box">{icon('target', 32, '#fff')}</div>
                <h4 style="color: #fff;">Матчинг</h4>
                <p class="text-sm" style="color: rgba(255,255,255,0.6);">Оценка соответствия кандидата</p>
            </div>
        </div>
        <div class="col col-4">
            <div class="card-dark" style="padding: 5mm;">
                <div class="icon-box">{icon('chart', 32, '#fff')}</div>
                <h4 style="color: #fff;">Ранжирование</h4>
                <p class="text-sm" style="color: rgba(255,255,255,0.6);">Автоматическая сортировка</p>
            </div>
        </div>
        <div class="col col-4">
            <div class="card-dark" style="padding: 5mm;">
                <div class="icon-box">{icon('document', 32, '#fff')}</div>
                <h4 style="color: #fff;">Саммари</h4>
                <p class="text-sm" style="color: rgba(255,255,255,0.6);">Краткое резюме за 20 сек</p>
            </div>
        </div>
    </div>
    
    <div style="background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); padding: 4mm 6mm; border-radius: 2mm; margin-top: 8mm;">
        <p class="text-sm mb-0" style="color: #F59E0B;">AI ускоряет рутину, но решение всегда за человеком</p>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo" style="filter: brightness(0) invert(1);"></div>
            <div class="footer-right" style="color: rgba(255,255,255,0.4);">8</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 9: ANALYTICS
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Аналитика</p>
    <h2>Данные вместо догадок</h2>
    
    <div class="row gap-lg">
        <div class="col col-2">
            <h4 class="mb-2">Воронка конверсий</h4>
            <div class="funnel-row"><div class="funnel-bar" style="width: 100%;">Отклики — 1000</div></div>
            <div class="funnel-row"><div class="funnel-bar" style="width: 60%;">Скрининг — 600</div></div>
            <div class="funnel-row"><div class="funnel-bar" style="width: 30%;">Интервью — 300</div></div>
            <div class="funnel-row"><div class="funnel-bar" style="width: 15%;">Оффер — 150</div></div>
            <div class="funnel-row"><div class="funnel-bar" style="width: 10%;">Выход — 100</div></div>
        </div>
        <div class="col col-2">
            <div class="row gap-md mb-3">
                <div class="col col-2">
                    <div class="card card-filled text-center">
                        <div class="stat-value">14</div>
                        <p class="text-sm text-muted">дней до найма</p>
                        <p class="text-sm text-accent mt-1"><strong>↓ 40%</strong></p>
                    </div>
                </div>
                <div class="col col-2">
                    <div class="card card-filled text-center">
                        <div class="stat-value">12K</div>
                        <p class="text-sm text-muted">₽ за найм</p>
                        <p class="text-sm text-accent mt-1"><strong>↓ 35%</strong></p>
                    </div>
                </div>
            </div>
            
            <div class="card card-filled">
                <h4 class="mb-2">Источники</h4>
                <p class="text-sm mb-0">
                    <span style="color: #d6001c;">●</span> HH.ru — 45%<br>
                    <span style="color: #00a859;">●</span> Авито — 30%<br>
                    <span style="color: {C['primary']};">●</span> Реферал — 25%
                </p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">9</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 10: SECURITY
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Безопасность</p>
    <h2>Защита данных</h2>
    
    <div class="row gap-md">
        <div class="col col-3">
            <div class="card card-filled text-center" style="min-height: 38mm;">
                <div class="icon-box">{icon('document', 32)}</div>
                <h4>ФЗ-152</h4>
                <p class="text-sm">Полное соответствие закону</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled text-center" style="min-height: 38mm;">
                <div class="icon-box">{icon('check', 32)}</div>
                <h4>Согласия</h4>
                <p class="text-sm">Автосбор и хранение</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled text-center" style="min-height: 38mm;">
                <div class="icon-box">{icon('users', 32)}</div>
                <h4>Роли</h4>
                <p class="text-sm">Разграничение доступа</p>
            </div>
        </div>
    </div>
    
    <div class="row gap-md mt-3">
        <div class="col col-3">
            <div class="card card-filled text-center" style="min-height: 38mm;">
                <div class="icon-box">{icon('audit', 32)}</div>
                <h4>Аудит</h4>
                <p class="text-sm">Логирование действий</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled text-center" style="min-height: 38mm;">
                <div class="icon-box">{icon('lock', 32)}</div>
                <h4>Шифрование</h4>
                <p class="text-sm">Защита данных</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card card-filled text-center" style="min-height: 38mm;">
                <div class="icon-box">{icon('shield', 32)}</div>
                <h4>Реестр ПО</h4>
                <p class="text-sm">Российское ПО</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">10</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 11: RESULTS
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-gradient">
    <p class="tag tag-light">Результаты</p>
    <h2>Что получите</h2>
    
    <div class="row gap-md">
        <div class="col col-3">
            <div class="card text-center" style="padding: 6mm;">
                <div class="stat-value" style="font-size: 36pt;">−40%</div>
                <p class="text-sm text-muted">расходы на найм</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card text-center" style="padding: 6mm;">
                <div class="stat-value" style="font-size: 36pt;">×4</div>
                <p class="text-sm text-muted">производительность</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card text-center" style="padding: 6mm;">
                <div class="stat-value" style="font-size: 36pt;">−60%</div>
                <p class="text-sm text-muted">время закрытия</p>
            </div>
        </div>
    </div>
    
    <div class="row gap-md mt-3">
        <div class="col col-3">
            <div class="card text-center" style="padding: 6mm;">
                <div class="stat-value" style="font-size: 36pt;">×3</div>
                <p class="text-sm text-muted">конверсия</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card text-center" style="padding: 6mm;">
                <div class="stat-value" style="font-size: 36pt;">0</div>
                <p class="text-sm text-muted">потерянных кандидатов</p>
            </div>
        </div>
        <div class="col col-3">
            <div class="card text-center" style="padding: 6mm;">
                <div class="stat-value" style="font-size: 36pt;">100%</div>
                <p class="text-sm text-muted">прозрачность</p>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo" style="filter: brightness(0) invert(1);"></div>
            <div class="footer-right" style="color: rgba(255,255,255,0.4);">11</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 12: PRICING
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Тарифы</p>
    <h2>Прозрачное ценообразование</h2>
    
    <div class="row gap-md">
        <div class="col col-3">
            <div class="pricing">
                <h4>Стандартный</h4>
                <div class="price">20 000 ₽</div>
                <div class="price-period">за лицензию / год</div>
                <ul class="list-check text-sm" style="text-align: left;">
                    <li>Единая база</li>
                    <li>Все интеграции</li>
                    <li>Воронки и этапы</li>
                    <li>Аналитика</li>
                    <li>Поддержка 24/7</li>
                </ul>
            </div>
        </div>
        <div class="col col-3">
            <div class="pricing pricing-featured">
                <span class="badge badge-primary mb-2">Популярный</span>
                <h4>Премиум</h4>
                <div class="price">42 000 ₽</div>
                <div class="price-period">за лицензию / год</div>
                <ul class="list-check text-sm" style="text-align: left;">
                    <li>Всё из Стандартного</li>
                    <li><strong>AI-модуль</strong></li>
                    <li>Умный поиск</li>
                    <li>Матчинг</li>
                    <li>Приоритетная поддержка</li>
                </ul>
            </div>
        </div>
        <div class="col col-3">
            <div class="pricing pricing-accent">
                <h4>Руководители</h4>
                <div class="price" style="color: {C['accent']};">Бесплатно</div>
                <div class="price-period">без ограничений</div>
                <ul class="list-check text-sm" style="text-align: left;">
                    <li>Просмотр кандидатов</li>
                    <li>Согласования</li>
                    <li>Фидбек</li>
                    <li>Отчёты</li>
                </ul>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">12</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 13: ONBOARDING
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Внедрение</p>
    <h2>Запуск за 1 день</h2>
    
    <div class="steps mt-4">
        <div class="step">
            <div class="step-num" style="font-size: 24pt;">30</div>
            <div class="step-desc">минут</div>
            <div class="step-title mt-2">Демо</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 24pt;">1</div>
            <div class="step-desc">день</div>
            <div class="step-title mt-2">Договор</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 24pt;">2–3</div>
            <div class="step-desc">дня</div>
            <div class="step-title mt-2">Настройка</div>
        </div>
        <div class="step">
            <div class="step-num" style="font-size: 24pt;">1</div>
            <div class="step-desc">час</div>
            <div class="step-title mt-2">Обучение</div>
        </div>
        <div class="step step-active">
            <div class="step-num" style="font-size: 24pt;">∞</div>
            <div class="step-desc">&nbsp;</div>
            <div class="step-title mt-2">Поддержка 24/7</div>
        </div>
    </div>
    
    <div class="card card-filled mt-4" style="padding: 5mm 6mm;">
        <p class="mb-0">Персональный менеджер на всех этапах внедрения и работы с системой</p>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">13</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 14: CONTACT
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide text-center">
    <p class="tag">Контакты</p>
    <h2>Начните сегодня</h2>
    
    <div class="row gap-md mt-4" style="max-width: 180mm; margin-left: auto; margin-right: auto;">
        <div class="col col-4">
            <div class="card card-filled text-center" style="padding: 5mm;">
                <div class="icon-box">{icon('globe', 28)}</div>
                <p class="text-sm mb-0"><strong class="text-primary">workhere.ru</strong></p>
            </div>
        </div>
        <div class="col col-4">
            <div class="card card-filled text-center" style="padding: 5mm;">
                <div class="icon-box">{icon('mail', 28)}</div>
                <p class="text-sm mb-0"><strong class="text-primary">info@workhere.ru</strong></p>
            </div>
        </div>
        <div class="col col-4">
            <div class="card card-filled text-center" style="padding: 5mm;">
                <div class="icon-box">{icon('phone', 28)}</div>
                <p class="text-sm mb-0"><strong class="text-primary">8 (800) 123-45-67</strong></p>
            </div>
        </div>
        <div class="col col-4">
            <div class="card card-filled text-center" style="padding: 5mm;">
                <div class="icon-box">{icon('telegram', 28)}</div>
                <p class="text-sm mb-0"><strong class="text-primary">@workhere</strong></p>
            </div>
        </div>
    </div>
    
    <div style="margin-top: 12mm;">
        <span style="display: inline-block; background: {C['primary']}; color: #fff; padding: 4mm 12mm; border-radius: 2mm; font-size: 12pt; font-weight: 600;">
            Записаться на демо →
        </span>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left"><img src="{LOGO_SRC}" class="logo"></div>
            <div class="footer-right">14</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 15: FINAL
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-dark text-center">
    <div class="pt-5">
        <h2 style="font-size: 28pt; font-weight: 400; line-height: 1.5;">
            ATS-систем много,<br>
            но вершину найма покоряет<br>
            <strong style="font-size: 36pt;">лишь одна</strong>
        </h2>
        
        <div style="margin-top: 15mm;">
            <img src="{LOGO_SRC}" style="height: 15mm; filter: brightness(0) invert(1);">
        </div>
        
        <p style="color: rgba(255,255,255,0.5); margin-top: 10mm; font-size: 12pt;">
            Ваши кандидаты уже ждут
        </p>
    </div>
</div>

</body>
</html>
"""

# ═══════════════════════════════════════════════════════════════
# GENERATE
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Генерация PDF...")
    
    html = HTML(string=HTML_CONTENT)
    output_path = Path("WorkHere_Presentation.pdf")
    html.write_pdf(str(output_path))
    
    size_kb = output_path.stat().st_size / 1024
    print(f"✅ PDF создан: {output_path}")
    print(f"   Размер: {size_kb:.0f} KB")
    
    import subprocess
    result = subprocess.run(['pdfinfo', str(output_path)], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if 'Pages' in line:
            print(f"   {line.strip()}")
