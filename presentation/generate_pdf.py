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
# SVG LOGO (no artifacts)
# ═══════════════════════════════════════════════════════════════

def logo_svg(color_work="#2196F3", color_here="#111827", height="6mm"):
    """Generate clean SVG logo"""
    return f'''<svg height="{height}" viewBox="0 0 120 28" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="55" height="28" rx="4" fill="{color_work}"/>
        <text x="6" y="21" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="white">Work</text>
        <text x="58" y="21" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="{color_here}">Here</text>
    </svg>'''

def logo_svg_white(height="6mm"):
    """White version for dark backgrounds"""
    return f'''<svg height="{height}" viewBox="0 0 120 28" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="55" height="28" rx="4" fill="#2196F3"/>
        <text x="6" y="21" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="white">Work</text>
        <text x="58" y="21" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="white">Here</text>
    </svg>'''

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
    min-height: 40mm;
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
    border-radius: 3mm;
    min-height: 40mm;
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
    height: 8mm;
    background: {C['primary']};
    border-radius: 1.5mm;
    color: {C['white']};
    font-size: 9pt;
    font-weight: 600;
    line-height: 8mm;
    padding: 0 4mm;
    min-width: 45mm;
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
    <div style="padding-top: 12mm;">
        <p class="tag tag-light">ATS + CRM для рекрутинга</p>
        <h1 style="font-size: 48pt; margin-bottom: 6mm;">WorkHere</h1>
        <p style="font-size: 14pt; color: rgba(255,255,255,0.8); max-width: 200mm; margin-bottom: 12mm; line-height: 1.6;">
            Единая система управления наймом: от заявки до выхода сотрудника.<br>
            Автоматизация, AI-поиск, аналитика — всё в одном месте.
        </p>
        
        <div style="display: table; width: 100%; max-width: 240mm; margin-bottom: 10mm;">
            <div style="display: table-row;">
                <div style="display: table-cell; width: 20%; text-align: center; padding: 4mm; border-right: 1px solid rgba(255,255,255,0.1);">
                    <div class="stat-value" style="color: #fff; font-size: 32pt;">1 500+</div>
                    <p class="text-sm" style="color: rgba(255,255,255,0.5);">компаний</p>
                </div>
                <div style="display: table-cell; width: 20%; text-align: center; padding: 4mm; border-right: 1px solid rgba(255,255,255,0.1);">
                    <div class="stat-value" style="color: #fff; font-size: 32pt;">AI</div>
                    <p class="text-sm" style="color: rgba(255,255,255,0.5);">умный поиск</p>
                </div>
                <div style="display: table-cell; width: 20%; text-align: center; padding: 4mm; border-right: 1px solid rgba(255,255,255,0.1);">
                    <div class="stat-value" style="color: #fff; font-size: 32pt;">−60%</div>
                    <p class="text-sm" style="color: rgba(255,255,255,0.5);">время найма</p>
                </div>
                <div style="display: table-cell; width: 20%; text-align: center; padding: 4mm; border-right: 1px solid rgba(255,255,255,0.1);">
                    <div class="stat-value" style="color: #fff; font-size: 32pt;">10+</div>
                    <p class="text-sm" style="color: rgba(255,255,255,0.5);">интеграций</p>
                </div>
                <div style="display: table-cell; width: 20%; text-align: center; padding: 4mm;">
                    <div class="stat-value" style="color: #fff; font-size: 32pt;">24/7</div>
                    <p class="text-sm" style="color: rgba(255,255,255,0.5);">поддержка</p>
                </div>
            </div>
        </div>
        
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">
                {logo_svg_white()}
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
            <div class="footer-left">{logo_svg()}</div>
            <div class="footer-right">2</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 3: SOLUTION
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-gradient">
    <div style="padding-top: 8mm;">
        <p class="tag tag-light">Решение</p>
        <h2 style="font-size: 26pt; margin-bottom: 8mm;">
            Одна система для всего процесса найма
        </h2>
        
        <div style="display: table; width: 100%; max-width: 245mm; margin-bottom: 4mm;">
            <div style="display: table-row;">
                <div style="display: table-cell; width: 25%; padding: 3mm;">
                    <div style="background: rgba(255,255,255,0.12); border-radius: 3mm; padding: 4mm; min-height: 32mm;">
                        {icon('database', 24, '#fff')}
                        <p style="color: #fff; font-weight: 600; margin: 2mm 0 1mm 0; font-size: 10pt;">Единая база</p>
                        <p style="color: rgba(255,255,255,0.7); font-size: 8pt; margin: 0; line-height: 1.4;">Все кандидаты, история, комментарии, теги — в одном месте</p>
                    </div>
                </div>
                <div style="display: table-cell; width: 25%; padding: 3mm;">
                    <div style="background: rgba(255,255,255,0.12); border-radius: 3mm; padding: 4mm; min-height: 32mm;">
                        {icon('rocket', 24, '#fff')}
                        <p style="color: #fff; font-weight: 600; margin: 2mm 0 1mm 0; font-size: 10pt;">Мультипостинг</p>
                        <p style="color: rgba(255,255,255,0.7); font-size: 8pt; margin: 0; line-height: 1.4;">Публикация вакансии на 10+ job-сайтах в 1 клик</p>
                    </div>
                </div>
                <div style="display: table-cell; width: 25%; padding: 3mm;">
                    <div style="background: rgba(255,255,255,0.12); border-radius: 3mm; padding: 4mm; min-height: 32mm;">
                        {icon('brain', 24, '#fff')}
                        <p style="color: #fff; font-weight: 600; margin: 2mm 0 1mm 0; font-size: 10pt;">AI-поиск</p>
                        <p style="color: rgba(255,255,255,0.7); font-size: 8pt; margin: 0; line-height: 1.4;">Умный поиск, матчинг, ранжирование кандидатов</p>
                    </div>
                </div>
                <div style="display: table-cell; width: 25%; padding: 3mm;">
                    <div style="background: rgba(255,255,255,0.12); border-radius: 3mm; padding: 4mm; min-height: 32mm;">
                        {icon('chart', 24, '#fff')}
                        <p style="color: #fff; font-weight: 600; margin: 2mm 0 1mm 0; font-size: 10pt;">Аналитика</p>
                        <p style="color: rgba(255,255,255,0.7); font-size: 8pt; margin: 0; line-height: 1.4;">Воронка, конверсии, источники, стоимость найма</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div style="display: table; width: 100%; max-width: 245mm;">
            <div style="display: table-row;">
                <div style="display: table-cell; width: 25%; padding: 3mm;">
                    <div style="background: rgba(255,255,255,0.12); border-radius: 3mm; padding: 4mm; min-height: 32mm;">
                        {icon('message', 24, '#fff')}
                        <p style="color: #fff; font-weight: 600; margin: 2mm 0 1mm 0; font-size: 10pt;">Коммуникации</p>
                        <p style="color: rgba(255,255,255,0.7); font-size: 8pt; margin: 0; line-height: 1.4;">Чаты HH, Авито, WhatsApp, Telegram — в одном окне</p>
                    </div>
                </div>
                <div style="display: table-cell; width: 25%; padding: 3mm;">
                    <div style="background: rgba(255,255,255,0.12); border-radius: 3mm; padding: 4mm; min-height: 32mm;">
                        {icon('clock', 24, '#fff')}
                        <p style="color: #fff; font-weight: 600; margin: 2mm 0 1mm 0; font-size: 10pt;">Автоматизация</p>
                        <p style="color: rgba(255,255,255,0.7); font-size: 8pt; margin: 0; line-height: 1.4;">Триггеры, шаблоны писем, напоминания, авто-отказы</p>
                    </div>
                </div>
                <div style="display: table-cell; width: 25%; padding: 3mm;">
                    <div style="background: rgba(255,255,255,0.12); border-radius: 3mm; padding: 4mm; min-height: 32mm;">
                        {icon('users', 24, '#fff')}
                        <p style="color: #fff; font-weight: 600; margin: 2mm 0 1mm 0; font-size: 10pt;">Командная работа</p>
                        <p style="color: rgba(255,255,255,0.7); font-size: 8pt; margin: 0; line-height: 1.4;">Роли, доступы, согласования, комментарии</p>
                    </div>
                </div>
                <div style="display: table-cell; width: 25%; padding: 3mm;">
                    <div style="background: rgba(255,255,255,0.12); border-radius: 3mm; padding: 4mm; min-height: 32mm;">
                        {icon('shield', 24, '#fff')}
                        <p style="color: #fff; font-weight: 600; margin: 2mm 0 1mm 0; font-size: 10pt;">Безопасность</p>
                        <p style="color: rgba(255,255,255,0.7); font-size: 8pt; margin: 0; line-height: 1.4;">152-ФЗ, согласия ПДн, аудит действий</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div style="background: rgba(255,255,255,0.15); border-radius: 2mm; padding: 4mm 6mm; margin-top: 6mm; max-width: 245mm;">
            <p style="color: #fff; font-size: 10pt; margin: 0; text-align: center;">
                <strong>Результат:</strong> рекрутер тратит время на людей, а не на рутину
            </p>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg_white()}</div>
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
    
    <div style="display: table; width: 100%; margin-top: 6mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 25%; padding: 3mm; vertical-align: top;">
                <div class="card" style="height: 65mm; padding: 5mm;">
                    <div class="icon-box">{icon('users', 28)}</div>
                    <h4 style="font-size: 11pt; margin: 3mm 0;">Рекрутер</h4>
                    <ul class="list-check text-sm">
                        <li>Единая база кандидатов</li>
                        <li>Автоматизация рутины</li>
                        <li>Шаблоны сообщений</li>
                        <li>Календарь интервью</li>
                    </ul>
                </div>
            </div>
            <div style="display: table-cell; width: 25%; padding: 3mm; vertical-align: top;">
                <div class="card card-accent" style="height: 65mm; padding: 5mm;">
                    <div class="icon-box">{icon('target', 28, '#fff')}</div>
                    <h4 style="font-size: 11pt; margin: 3mm 0; color: #fff;">Руководитель подбора</h4>
                    <ul class="list-check text-sm" style="color: rgba(255,255,255,0.9);">
                        <li>Контроль SLA и сроков</li>
                        <li>Аналитика команды</li>
                        <li>Отчёты для топов</li>
                        <li>Распределение нагрузки</li>
                    </ul>
                </div>
            </div>
            <div style="display: table-cell; width: 25%; padding: 3mm; vertical-align: top;">
                <div class="card" style="height: 65mm; padding: 5mm;">
                    <div class="icon-box">{icon('message', 28)}</div>
                    <h4 style="font-size: 11pt; margin: 3mm 0;">Нанимающий менеджер</h4>
                    <ul class="list-check text-sm">
                        <li>Просмотр кандидатов</li>
                        <li>Быстрый фидбек</li>
                        <li>Уведомления</li>
                        <li>Согласование оффера</li>
                    </ul>
                </div>
            </div>
            <div style="display: table-cell; width: 25%; padding: 3mm; vertical-align: top;">
                <div class="card" style="height: 65mm; padding: 5mm;">
                    <div class="icon-box">{icon('chart', 28)}</div>
                    <h4 style="font-size: 11pt; margin: 3mm 0;">HRD / Бизнес</h4>
                    <ul class="list-check text-sm">
                        <li>Стоимость найма</li>
                        <li>Прогнозирование</li>
                        <li>Unit-экономика</li>
                        <li>Дашборды и отчёты</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg()}</div>
            <div class="footer-right">4</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 5: FUNNEL
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Процесс</p>
    <h2>Полный цикл найма под контролем</h2>
    
    <div style="display: table; width: 100%; margin-top: 6mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 16.6%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['primary_light']}; border: 2px solid {C['primary']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 24pt; font-weight: 700; color: {C['primary']};">01</div>
                    <div style="font-weight: 600; font-size: 10pt; margin: 2mm 0;">Заявка</div>
                    <div style="font-size: 8pt; color: {C['muted']}; line-height: 1.3;">Менеджер создаёт заявку с требованиями и сроками</div>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['bg']}; border: 1px solid {C['border']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 24pt; font-weight: 700; color: {C['text']};">02</div>
                    <div style="font-weight: 600; font-size: 10pt; margin: 2mm 0;">Публикация</div>
                    <div style="font-size: 8pt; color: {C['muted']}; line-height: 1.3;">Мультипостинг на HH, Авито, SuperJob за 1 клик</div>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['bg']}; border: 1px solid {C['border']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 24pt; font-weight: 700; color: {C['text']};">03</div>
                    <div style="font-weight: 600; font-size: 10pt; margin: 2mm 0;">Отклики</div>
                    <div style="font-size: 8pt; color: {C['muted']}; line-height: 1.3;">Все резюме в едином потоке, автопарсинг данных</div>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['bg']}; border: 1px solid {C['border']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 24pt; font-weight: 700; color: {C['text']};">04</div>
                    <div style="font-weight: 600; font-size: 10pt; margin: 2mm 0;">Скрининг</div>
                    <div style="font-size: 8pt; color: {C['muted']}; line-height: 1.3;">AI-ранжирование, фильтры, быстрый отбор лучших</div>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['bg']}; border: 1px solid {C['border']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 24pt; font-weight: 700; color: {C['text']};">05</div>
                    <div style="font-weight: 600; font-size: 10pt; margin: 2mm 0;">Интервью</div>
                    <div style="font-size: 8pt; color: {C['muted']}; line-height: 1.3;">Календарь, напоминания, оценочные листы</div>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['accent_light']}; border: 2px solid {C['accent']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 24pt; font-weight: 700; color: {C['accent']};">06</div>
                    <div style="font-weight: 600; font-size: 10pt; margin: 2mm 0;">Оффер</div>
                    <div style="font-size: 8pt; color: {C['muted']}; line-height: 1.3;">Согласование, оффер, онбординг нового сотрудника</div>
                </div>
            </div>
        </div>
    </div>
    
    <div style="display: table; width: 100%; margin-top: 8mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 33%; padding: 3mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 28mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 12mm; vertical-align: top;">{icon('clock', 24, C['primary'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <p style="font-weight: 600; margin: 0 0 1mm 0; font-size: 10pt;">SLA и дедлайны</p>
                            <p class="text-sm" style="margin: 0; color: {C['muted']};">Автоматический контроль сроков на каждом этапе воронки</p>
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 3mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 28mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 12mm; vertical-align: top;">{icon('message', 24, C['primary'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <p style="font-weight: 600; margin: 0 0 1mm 0; font-size: 10pt;">Уведомления</p>
                            <p class="text-sm" style="margin: 0; color: {C['muted']};">Push, email, Telegram — никто не забудет про кандидата</p>
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 3mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 28mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 12mm; vertical-align: top;">{icon('chart', 24, C['primary'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <p style="font-weight: 600; margin: 0 0 1mm 0; font-size: 10pt;">Прозрачность</p>
                            <p class="text-sm" style="margin: 0; color: {C['muted']};">Видно, где кандидат и кто за него отвечает</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg()}</div>
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
    
    <div style="display: table; width: 100%;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 50%; vertical-align: top; padding-right: 6mm;">
                <div style="display: table; width: 100%; margin-bottom: 4mm;">
                    <div style="display: table-row;">
                        <div style="display: table-cell; width: 50%; padding: 2mm;">
                            <div class="card card-filled" style="padding: 4mm; min-height: 24mm;">
                                {icon('database', 20, C['primary'])}
                                <p style="font-weight: 600; font-size: 9pt; margin: 2mm 0 1mm 0;">Все резюме</p>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 0;">В одном месте, без дублей</p>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 50%; padding: 2mm;">
                            <div class="card card-filled" style="padding: 4mm; min-height: 24mm;">
                                {icon('clock', 20, C['primary'])}
                                <p style="font-weight: 600; font-size: 9pt; margin: 2mm 0 1mm 0;">История</p>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 0;">Все взаимодействия и этапы</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="display: table; width: 100%; margin-bottom: 4mm;">
                    <div style="display: table-row;">
                        <div style="display: table-cell; width: 50%; padding: 2mm;">
                            <div class="card card-filled" style="padding: 4mm; min-height: 24mm;">
                                {icon('search', 20, C['primary'])}
                                <p style="font-weight: 600; font-size: 9pt; margin: 2mm 0 1mm 0;">Умный поиск</p>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 0;">По навыкам, опыту, городу</p>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 50%; padding: 2mm;">
                            <div class="card card-filled" style="padding: 4mm; min-height: 24mm;">
                                {icon('list', 20, C['primary'])}
                                <p style="font-weight: 600; font-size: 9pt; margin: 2mm 0 1mm 0;">Теги и фильтры</p>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 0;">Сегментация базы</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div style="display: table; width: 100%;">
                    <div style="display: table-row;">
                        <div style="display: table-cell; width: 50%; padding: 2mm;">
                            <div class="card card-filled" style="padding: 4mm; min-height: 24mm;">
                                {icon('link', 20, C['primary'])}
                                <p style="font-weight: 600; font-size: 9pt; margin: 2mm 0 1mm 0;">Слияние</p>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 0;">Объединение карточек</p>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 50%; padding: 2mm;">
                            <div class="card card-filled" style="padding: 4mm; min-height: 24mm;">
                                {icon('message', 20, C['primary'])}
                                <p style="font-weight: 600; font-size: 9pt; margin: 2mm 0 1mm 0;">Комментарии</p>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 0;">Заметки от команды</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: table-cell; width: 50%; vertical-align: top;">
                <div class="mockup" style="min-height: 95mm;">
                    <div class="mockup-dots">
                        <span class="mockup-dot" style="background: #ff5f57;"></span>
                        <span class="mockup-dot" style="background: #febc2e;"></span>
                        <span class="mockup-dot" style="background: #28c840;"></span>
                        <span style="float: right; font-size: 7pt; color: rgba(255,255,255,0.4);">База кандидатов: 12 847</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.05); border-radius: 2mm; padding: 2mm 3mm; margin-bottom: 3mm;">
                        <span style="color: rgba(255,255,255,0.4); font-size: 8pt;">{icon('search', 12, 'rgba(255,255,255,0.4)')}</span>
                        <span style="color: rgba(255,255,255,0.4); font-size: 8pt; margin-left: 2mm;">Python developer Москва 3+ года...</span>
                    </div>
                    <div class="mockup-card">
                        <span class="mockup-avatar" style="background: #4F6AF5;">АИ</span>
                        <span class="mockup-info">
                            <span class="mockup-name">Алексей Иванов</span><br>
                            <span class="mockup-role">Senior Python Developer • 5 лет • Москва</span>
                        </span>
                        <span class="mockup-status status-green">Оффер</span>
                    </div>
                    <div class="mockup-card">
                        <span class="mockup-avatar" style="background: #10B981;">МП</span>
                        <span class="mockup-info">
                            <span class="mockup-name">Мария Петрова</span><br>
                            <span class="mockup-role">Product Manager • 4 года • СПб</span>
                        </span>
                        <span class="mockup-status status-yellow">Интервью</span>
                    </div>
                    <div class="mockup-card">
                        <span class="mockup-avatar" style="background: #F59E0B;">ДС</span>
                        <span class="mockup-info">
                            <span class="mockup-name">Дмитрий Сидоров</span><br>
                            <span class="mockup-role">UX/UI Designer • 3 года • Удалённо</span>
                        </span>
                        <span class="mockup-status status-blue">Скрининг</span>
                    </div>
                    <div class="mockup-card">
                        <span class="mockup-avatar" style="background: #6B7280;">ЕК</span>
                        <span class="mockup-info">
                            <span class="mockup-name">Елена Козлова</span><br>
                            <span class="mockup-role">Data Analyst • 2 года • Казань</span>
                        </span>
                        <span class="mockup-status status-blue">Новый</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg()}</div>
            <div class="footer-right">6</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 7: INTEGRATIONS
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Интеграции</p>
    <h2>Подключено к экосистеме рекрутинга</h2>
    
    <div style="display: table; width: 100%; margin-top: 4mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 33%; vertical-align: top; padding-right: 4mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 75mm;">
                    <h4 style="margin-bottom: 3mm; font-size: 11pt;">{icon('globe', 18, C['primary'])} Job-сайты</h4>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #d6001c;">HeadHunter</span>
                        <span class="int-badge" style="background: #00a859;">Авито</span>
                    </div>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #ff6600;">SuperJob</span>
                        <span class="int-badge" style="background: #0066cc;">Работа.ру</span>
                    </div>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #0077b5;">LinkedIn</span>
                        <span class="int-badge" style="background: #6b4fbb;">Хабр Карьера</span>
                    </div>
                    <div>
                        <span class="int-badge" style="background: #1a1a1a;">Зарплата.ру</span>
                        <span class="int-badge" style="background: #ff4444;">Rabota.by</span>
                    </div>
                    <p style="font-size: 8pt; color: {C['muted']}; margin-top: 3mm;">Мультипостинг + парсинг откликов + чаты</p>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; vertical-align: top; padding: 0 2mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 75mm;">
                    <h4 style="margin-bottom: 3mm; font-size: 11pt;">{icon('message', 18, C['primary'])} Коммуникации</h4>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #0088cc;">Telegram</span>
                        <span class="int-badge" style="background: #25d366;">WhatsApp</span>
                    </div>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #7360f2;">Viber</span>
                        <span class="int-badge" style="background: #0078d4;">Email SMTP</span>
                    </div>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #ea4335;">Gmail</span>
                        <span class="int-badge" style="background: #0072c6;">Outlook</span>
                    </div>
                    <div>
                        <span class="int-badge" style="background: #333;">SMS-шлюзы</span>
                    </div>
                    <p style="font-size: 8pt; color: {C['muted']}; margin-top: 3mm;">Все переписки в карточке кандидата</p>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; vertical-align: top; padding-left: 4mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 75mm;">
                    <h4 style="margin-bottom: 3mm; font-size: 11pt;">{icon('link', 18, C['primary'])} Сервисы</h4>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #fc3f1d;">Яндекс.Телемост</span>
                    </div>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #ffcc00; color: #000;">1С:ЗУП</span>
                        <span class="int-badge" style="background: #ffcc00; color: #000;">1С:Предприятие</span>
                    </div>
                    <div style="margin-bottom: 2mm;">
                        <span class="int-badge" style="background: #333;">REST API</span>
                        <span class="int-badge" style="background: #6b46c1;">Webhooks</span>
                    </div>
                    <div>
                        <span class="int-badge" style="background: #0077ff;">VK HR</span>
                    </div>
                    <p style="font-size: 8pt; color: {C['muted']}; margin-top: 3mm;">Открытое API для любых интеграций</p>
                </div>
            </div>
        </div>
    </div>
    
    <div style="background: {C['primary_light']}; border: 1px solid {C['primary']}; border-radius: 2mm; padding: 4mm 6mm; margin-top: 5mm;">
        <p style="font-size: 10pt; margin: 0; color: {C['primary']};">
            <strong>Бесшовная интеграция:</strong> кандидат откликается на HH → резюме автоматически в системе → переписка в едином чате → статус обновляется в реальном времени
        </p>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg()}</div>
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
    
    <div style="display: table; width: 100%; margin-top: 6mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 25%; padding: 3mm; vertical-align: top;">
                <div class="card-dark" style="padding: 5mm; height: 55mm;">
                    <div class="icon-box">{icon('search', 28, '#fff')}</div>
                    <h4 style="color: #fff; font-size: 11pt; margin: 3mm 0;">Умный поиск</h4>
                    <p style="font-size: 9pt; color: rgba(255,255,255,0.7); margin: 0; line-height: 1.4;">Семантический поиск по базе. Понимает синонимы, опечатки и контекст.</p>
                </div>
            </div>
            <div style="display: table-cell; width: 25%; padding: 3mm; vertical-align: top;">
                <div class="card-dark" style="padding: 5mm; height: 55mm;">
                    <div class="icon-box">{icon('target', 28, '#fff')}</div>
                    <h4 style="color: #fff; font-size: 11pt; margin: 3mm 0;">Матчинг</h4>
                    <p style="font-size: 9pt; color: rgba(255,255,255,0.7); margin: 0; line-height: 1.4;">Оценка соответствия кандидата требованиям вакансии в %.</p>
                </div>
            </div>
            <div style="display: table-cell; width: 25%; padding: 3mm; vertical-align: top;">
                <div class="card-dark" style="padding: 5mm; height: 55mm;">
                    <div class="icon-box">{icon('chart', 28, '#fff')}</div>
                    <h4 style="color: #fff; font-size: 11pt; margin: 3mm 0;">Ранжирование</h4>
                    <p style="font-size: 9pt; color: rgba(255,255,255,0.7); margin: 0; line-height: 1.4;">Сортировка откликов. Лучшие кандидаты — всегда в топе.</p>
                </div>
            </div>
            <div style="display: table-cell; width: 25%; padding: 3mm; vertical-align: top;">
                <div class="card-dark" style="padding: 5mm; height: 55mm;">
                    <div class="icon-box">{icon('document', 28, '#fff')}</div>
                    <h4 style="color: #fff; font-size: 11pt; margin: 3mm 0;">Саммари резюме</h4>
                    <p style="font-size: 9pt; color: rgba(255,255,255,0.7); margin: 0; line-height: 1.4;">Краткая выжимка навыков и опыта за 20 секунд.</p>
                </div>
            </div>
        </div>
    </div>
    
    <div style="background: rgba(79,106,245,0.2); border: 1px solid rgba(79,106,245,0.4); padding: 4mm 6mm; border-radius: 2mm; margin-top: 8mm;">
        <p style="font-size: 10pt; margin: 0; color: #7B8CFF;"><strong style="color: #fff;">AI — ваш помощник, не замена.</strong> Финальное решение о найме всегда за рекрутером.</p>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg_white()}</div>
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
    
    <div style="display: table; width: 100%;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 40%; vertical-align: top; padding-right: 5mm;">
                <h4 style="margin-bottom: 3mm; font-size: 11pt;">Воронка найма</h4>
                <div class="funnel-row"><div class="funnel-bar" style="width: 100%;">Отклики — 1 247 <span style="float: right; opacity: 0.7;">100%</span></div></div>
                <div class="funnel-row"><div class="funnel-bar" style="width: 65%;">Скрининг — 811 <span style="float: right; opacity: 0.7;">65%</span></div></div>
                <div class="funnel-row"><div class="funnel-bar" style="width: 35%;">Интервью — 437 <span style="float: right; opacity: 0.7;">35%</span></div></div>
                <div class="funnel-row"><div class="funnel-bar" style="width: 18%;">Финал — 224 <span style="float: right; opacity: 0.7;">18%</span></div></div>
                <div class="funnel-row"><div class="funnel-bar" style="width: 12%; background: {C['accent']};">Оффер — 150 <span style="float: right; opacity: 0.7;">12%</span></div></div>
                <div class="funnel-row"><div class="funnel-bar" style="width: 9%; background: {C['accent']};">Выход — 112 <span style="float: right; opacity: 0.7;">9%</span></div></div>
                
                <p style="font-size: 8pt; color: {C['muted']}; margin-top: 3mm;">Видно, где теряются кандидаты и почему</p>
            </div>
            <div style="display: table-cell; width: 60%; vertical-align: top;">
                <div style="display: table; width: 100%; margin-bottom: 4mm;">
                    <div style="display: table-row;">
                        <div style="display: table-cell; width: 25%; padding: 2mm;">
                            <div class="card card-filled text-center" style="padding: 4mm;">
                                <div class="stat-value" style="font-size: 24pt;">14</div>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 1mm 0;">дней до найма</p>
                                <p style="font-size: 9pt; color: {C['accent']}; margin: 0; font-weight: 600;">↓ 40%</p>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 25%; padding: 2mm;">
                            <div class="card card-filled text-center" style="padding: 4mm;">
                                <div class="stat-value" style="font-size: 24pt;">12K</div>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 1mm 0;">₽ за найм</p>
                                <p style="font-size: 9pt; color: {C['accent']}; margin: 0; font-weight: 600;">↓ 35%</p>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 25%; padding: 2mm;">
                            <div class="card card-filled text-center" style="padding: 4mm;">
                                <div class="stat-value" style="font-size: 24pt;">87%</div>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 1mm 0;">retention 1 год</p>
                                <p style="font-size: 9pt; color: {C['accent']}; margin: 0; font-weight: 600;">↑ 15%</p>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 25%; padding: 2mm;">
                            <div class="card card-filled text-center" style="padding: 4mm;">
                                <div class="stat-value" style="font-size: 24pt;">4.2</div>
                                <p style="font-size: 8pt; color: {C['muted']}; margin: 1mm 0;">NPS кандидатов</p>
                                <p style="font-size: 9pt; color: {C['accent']}; margin: 0; font-weight: 600;">↑ 0.8</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div style="display: table; width: 100%;">
                    <div style="display: table-row;">
                        <div style="display: table-cell; width: 50%; padding: 2mm;">
                            <div class="card card-filled" style="padding: 4mm;">
                                <h4 style="font-size: 10pt; margin-bottom: 2mm;">Источники найма</h4>
                                <div style="margin-bottom: 2mm;">
                                    <span style="display: inline-block; width: 8mm; height: 3mm; background: #d6001c; border-radius: 1mm; vertical-align: middle;"></span>
                                    <span style="font-size: 9pt; margin-left: 2mm;">HeadHunter — 42%</span>
                                </div>
                                <div style="margin-bottom: 2mm;">
                                    <span style="display: inline-block; width: 8mm; height: 3mm; background: #00a859; border-radius: 1mm; vertical-align: middle;"></span>
                                    <span style="font-size: 9pt; margin-left: 2mm;">Авито — 28%</span>
                                </div>
                                <div style="margin-bottom: 2mm;">
                                    <span style="display: inline-block; width: 8mm; height: 3mm; background: {C['primary']}; border-radius: 1mm; vertical-align: middle;"></span>
                                    <span style="font-size: 9pt; margin-left: 2mm;">Рефералы — 18%</span>
                                </div>
                                <div>
                                    <span style="display: inline-block; width: 8mm; height: 3mm; background: #ff6600; border-radius: 1mm; vertical-align: middle;"></span>
                                    <span style="font-size: 9pt; margin-left: 2mm;">Другие — 12%</span>
                                </div>
                            </div>
                        </div>
                        <div style="display: table-cell; width: 50%; padding: 2mm;">
                            <div class="card card-filled" style="padding: 4mm;">
                                <h4 style="font-size: 10pt; margin-bottom: 2mm;">Эффективность рекрутеров</h4>
                                <div style="margin-bottom: 2mm;">
                                    <span style="font-size: 9pt;">Анна К.</span>
                                    <span style="float: right; font-size: 9pt; color: {C['accent']}; font-weight: 600;">24 найма</span>
                                </div>
                                <div style="margin-bottom: 2mm;">
                                    <span style="font-size: 9pt;">Михаил С.</span>
                                    <span style="float: right; font-size: 9pt; color: {C['accent']}; font-weight: 600;">21 найм</span>
                                </div>
                                <div style="margin-bottom: 2mm;">
                                    <span style="font-size: 9pt;">Елена П.</span>
                                    <span style="float: right; font-size: 9pt; font-weight: 600;">18 наймов</span>
                                </div>
                                <div>
                                    <span style="font-size: 9pt;">Дмитрий В.</span>
                                    <span style="float: right; font-size: 9pt; font-weight: 600;">15 наймов</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg()}</div>
            <div class="footer-right">9</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 10: SECURITY
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Безопасность</p>
    <h2>Защита персональных данных</h2>
    
    <div style="display: table; width: 100%; margin-top: 4mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; height: 38mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 14mm; vertical-align: top;">{icon('document', 28, C['primary'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <h4 style="font-size: 11pt; margin: 0 0 2mm 0;">ФЗ-152</h4>
                            <p style="font-size: 9pt; color: {C['muted']}; margin: 0; line-height: 1.4;">Полное соответствие закону о персональных данных. Готовые политики и документы.</p>
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; height: 38mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 14mm; vertical-align: top;">{icon('check', 28, C['accent'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <h4 style="font-size: 11pt; margin: 0 0 2mm 0;">Согласия ПДн</h4>
                            <p style="font-size: 9pt; color: {C['muted']}; margin: 0; line-height: 1.4;">Автоматический сбор и хранение согласий. Отзыв по запросу за 1 клик.</p>
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; height: 38mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 14mm; vertical-align: top;">{icon('users', 28, C['primary'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <h4 style="font-size: 11pt; margin: 0 0 2mm 0;">Роли и доступы</h4>
                            <p style="font-size: 9pt; color: {C['muted']}; margin: 0; line-height: 1.4;">Гибкая система прав. Видит только то, что нужно для работы.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div style="display: table; width: 100%; margin-top: 2mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; height: 38mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 14mm; vertical-align: top;">{icon('audit', 28, C['primary'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <h4 style="font-size: 11pt; margin: 0 0 2mm 0;">Аудит действий</h4>
                            <p style="font-size: 9pt; color: {C['muted']}; margin: 0; line-height: 1.4;">Полный лог: кто, когда и что делал. Для проверок и расследований.</p>
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; height: 38mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 14mm; vertical-align: top;">{icon('lock', 28, C['primary'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <h4 style="font-size: 11pt; margin: 0 0 2mm 0;">Шифрование</h4>
                            <p style="font-size: 9pt; color: {C['muted']}; margin: 0; line-height: 1.4;">TLS 1.3, шифрование данных в покое. Безопасная передача резюме.</p>
                        </div>
                    </div>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; height: 38mm;">
                    <div style="display: table; width: 100%;">
                        <div style="display: table-cell; width: 14mm; vertical-align: top;">{icon('shield', 28, C['accent'])}</div>
                        <div style="display: table-cell; vertical-align: top;">
                            <h4 style="font-size: 11pt; margin: 0 0 2mm 0;">Реестр ПО</h4>
                            <p style="font-size: 9pt; color: {C['muted']}; margin: 0; line-height: 1.4;">Включены в реестр российского ПО. Подходит для госзакупок.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div style="display: table; width: 100%; margin-top: 4mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 50%; padding: 2mm;">
                <div style="background: {C['accent_light']}; border: 1px solid {C['accent']}; border-radius: 2mm; padding: 4mm;">
                    <p style="font-size: 10pt; margin: 0; color: {C['accent']};">
                        <strong>Хранение:</strong> данные на серверах в России (Tier III дата-центры)
                    </p>
                </div>
            </div>
            <div style="display: table-cell; width: 50%; padding: 2mm;">
                <div style="background: {C['primary_light']}; border: 1px solid {C['primary']}; border-radius: 2mm; padding: 4mm;">
                    <p style="font-size: 10pt; margin: 0; color: {C['primary']};">
                        <strong>Бэкапы:</strong> ежедневное резервное копирование, хранение 30 дней
                    </p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg()}</div>
            <div class="footer-right">10</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 11: RESULTS
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide slide-gradient">
    <p class="tag tag-light">Результаты</p>
    <h2>Что получите с WorkHere</h2>
    
    <div style="display: table; width: 100%; margin-top: 4mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 16.6%; padding: 2mm;">
                <div class="card text-center" style="padding: 4mm;">
                    <div class="stat-value" style="font-size: 28pt;">−40%</div>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 2mm 0 0 0;">расходы на найм</p>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm;">
                <div class="card text-center" style="padding: 4mm;">
                    <div class="stat-value" style="font-size: 28pt;">×4</div>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 2mm 0 0 0;">производительность</p>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm;">
                <div class="card text-center" style="padding: 4mm;">
                    <div class="stat-value" style="font-size: 28pt;">−60%</div>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 2mm 0 0 0;">время закрытия</p>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm;">
                <div class="card text-center" style="padding: 4mm;">
                    <div class="stat-value" style="font-size: 28pt;">×3</div>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 2mm 0 0 0;">конверсия</p>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm;">
                <div class="card text-center" style="padding: 4mm;">
                    <div class="stat-value" style="font-size: 28pt;">0</div>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 2mm 0 0 0;">потерь</p>
                </div>
            </div>
            <div style="display: table-cell; width: 16.6%; padding: 2mm;">
                <div class="card text-center" style="padding: 4mm;">
                    <div class="stat-value" style="font-size: 28pt;">100%</div>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 2mm 0 0 0;">прозрачность</p>
                </div>
            </div>
        </div>
    </div>
    
    <div style="display: table; width: 100%; margin-top: 6mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card" style="padding: 5mm; min-height: 48mm;">
                    <p style="font-size: 9pt; color: {C['primary']}; margin: 0 0 2mm 0; font-weight: 600;">Кейс: Ритейл</p>
                    <p style="font-size: 10pt; font-weight: 600; margin: 0 0 2mm 0;">X5 Group</p>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 0 0 3mm 0; line-height: 1.4;">Массовый подбор 500+ вакансий в месяц</p>
                    <p style="font-size: 9pt; margin: 0;"><strong style="color: {C['accent']};">Результат:</strong> время закрытия −55%, рутина рекрутеров −70%</p>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card" style="padding: 5mm; min-height: 48mm;">
                    <p style="font-size: 9pt; color: {C['primary']}; margin: 0 0 2mm 0; font-weight: 600;">Кейс: IT</p>
                    <p style="font-size: 10pt; font-weight: 600; margin: 0 0 2mm 0;">СберТех</p>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 0 0 3mm 0; line-height: 1.4;">IT-подбор разработчиков и DevOps</p>
                    <p style="font-size: 9pt; margin: 0;"><strong style="color: {C['accent']};">Результат:</strong> конверсия воронки ×2.5, экономия 1.2 млн ₽/год</p>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card" style="padding: 5mm; min-height: 48mm;">
                    <p style="font-size: 9pt; color: {C['primary']}; margin: 0 0 2mm 0; font-weight: 600;">Кейс: Производство</p>
                    <p style="font-size: 10pt; font-weight: 600; margin: 0 0 2mm 0;">Северсталь</p>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 0 0 3mm 0; line-height: 1.4;">Региональный подбор на заводы</p>
                    <p style="font-size: 9pt; margin: 0;"><strong style="color: {C['accent']};">Результат:</strong> единая база 50K+ кандидатов, отказ от Excel</p>
                </div>
            </div>
        </div>
    </div>
    
    <div style="background: rgba(255,255,255,0.1); border-radius: 2mm; padding: 4mm 6mm; margin-top: 5mm;">
        <p style="font-size: 10pt; margin: 0; color: rgba(255,255,255,0.9); text-align: center;">
            <strong>ROI в первый год:</strong> экономия от 500 000 ₽ на команду из 5 рекрутеров
        </p>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg_white()}</div>
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
            <div class="footer-left">{logo_svg()}</div>
            <div class="footer-right">12</div>
        </div>
    </div>
</div>

<!-- ═══════════════════════════════════════════════════════════════
     SLIDE 13: ONBOARDING
     ═══════════════════════════════════════════════════════════════ -->
<div class="slide">
    <p class="tag">Внедрение</p>
    <h2>Запуск системы — быстро и безболезненно</h2>
    
    <div style="display: table; width: 100%; margin-top: 5mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 20%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['primary_light']}; border: 2px solid {C['primary']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 28pt; font-weight: 700; color: {C['primary']};">30</div>
                    <div style="font-size: 9pt; color: {C['muted']};">минут</div>
                    <div style="font-weight: 600; font-size: 10pt; margin-top: 2mm;">Демо</div>
                    <div style="font-size: 8pt; color: {C['muted']}; margin-top: 1mm;">Покажем систему под ваши задачи</div>
                </div>
            </div>
            <div style="display: table-cell; width: 20%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['bg']}; border: 1px solid {C['border']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 28pt; font-weight: 700; color: {C['text']};">1</div>
                    <div style="font-size: 9pt; color: {C['muted']};">день</div>
                    <div style="font-weight: 600; font-size: 10pt; margin-top: 2mm;">Договор</div>
                    <div style="font-size: 8pt; color: {C['muted']}; margin-top: 1mm;">Быстрое согласование условий</div>
                </div>
            </div>
            <div style="display: table-cell; width: 20%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['bg']}; border: 1px solid {C['border']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 28pt; font-weight: 700; color: {C['text']};">2–3</div>
                    <div style="font-size: 9pt; color: {C['muted']};">дня</div>
                    <div style="font-weight: 600; font-size: 10pt; margin-top: 2mm;">Настройка</div>
                    <div style="font-size: 8pt; color: {C['muted']}; margin-top: 1mm;">Воронки, роли, интеграции</div>
                </div>
            </div>
            <div style="display: table-cell; width: 20%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['bg']}; border: 1px solid {C['border']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 28pt; font-weight: 700; color: {C['text']};">1</div>
                    <div style="font-size: 9pt; color: {C['muted']};">час</div>
                    <div style="font-weight: 600; font-size: 10pt; margin-top: 2mm;">Обучение</div>
                    <div style="font-size: 8pt; color: {C['muted']}; margin-top: 1mm;">Онлайн-сессия для команды</div>
                </div>
            </div>
            <div style="display: table-cell; width: 20%; padding: 2mm; text-align: center; vertical-align: top;">
                <div style="background: {C['accent_light']}; border: 2px solid {C['accent']}; border-radius: 3mm; padding: 4mm;">
                    <div style="font-size: 28pt; font-weight: 700; color: {C['accent']};">∞</div>
                    <div style="font-size: 9pt; color: {C['muted']};">&nbsp;</div>
                    <div style="font-weight: 600; font-size: 10pt; margin-top: 2mm;">Поддержка</div>
                    <div style="font-size: 8pt; color: {C['muted']}; margin-top: 1mm;">24/7 чат, звонок, почта</div>
                </div>
            </div>
        </div>
    </div>
    
    <div style="display: table; width: 100%; margin-top: 6mm;">
        <div style="display: table-row;">
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 32mm;">
                    {icon('users', 24, C['primary'])}
                    <p style="font-weight: 600; font-size: 10pt; margin: 2mm 0 1mm 0;">Персональный менеджер</p>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 0;">Один контакт на все вопросы. Знает вашу компанию и задачи.</p>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 32mm;">
                    {icon('document', 24, C['primary'])}
                    <p style="font-weight: 600; font-size: 10pt; margin: 2mm 0 1mm 0;">База знаний</p>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 0;">Видеоуроки, статьи, FAQ. Ответы на 90% вопросов уже есть.</p>
                </div>
            </div>
            <div style="display: table-cell; width: 33%; padding: 2mm;">
                <div class="card card-filled" style="padding: 4mm; min-height: 32mm;">
                    {icon('rocket', 24, C['primary'])}
                    <p style="font-weight: 600; font-size: 10pt; margin: 2mm 0 1mm 0;">Миграция данных</p>
                    <p style="font-size: 9pt; color: {C['muted']}; margin: 0;">Перенесём базу из Excel, другой ATS или почты. Бесплатно.</p>
                </div>
            </div>
        </div>
    </div>
    
    <div style="background: {C['primary_light']}; border: 1px solid {C['primary']}; border-radius: 2mm; padding: 4mm 6mm; margin-top: 4mm;">
        <p style="font-size: 10pt; margin: 0; color: {C['primary']}; text-align: center;">
            <strong>SLA поддержки:</strong> ответ в чате — до 5 минут, решение критичных багов — до 4 часов
        </p>
    </div>
    
    <div class="footer">
        <div class="footer-inner">
            <div class="footer-left">{logo_svg()}</div>
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
            <div class="footer-left">{logo_svg()}</div>
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
            {logo_svg_white("15mm")}
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
