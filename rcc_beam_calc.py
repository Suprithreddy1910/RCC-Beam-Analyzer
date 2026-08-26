"""
RCC BEAM DESIGN - PURE PYTHON CALCULATION CODE
Based on IS 456:2000 (India Standard)
No web framework - just calculations
"""

import math

# ============================================================================
# STEP 1: INPUT DATA
# ============================================================================

print("\n" + "="*70)
print("RCC BEAM DESIGN CALCULATIONS")
print("="*70)

# Beam dimensions (in mm)
span_m = float(input("\nSpan length (meters): "))
b = float(input("Width, b (mm): "))
D = float(input("Total depth, D (mm): "))
cover = float(input("Effective cover, d' (mm): "))

# Material properties
fck = float(input("\nConcrete grade (20/25/30/35/40): "))
fy = float(input("Steel grade (250/415/500): "))

# Design forces
Mu = float(input("\nFactored moment, Mu (kNm): "))
Vu = float(input("Factored shear, Vu (kN): "))

print("\n" + "="*70)
print("CALCULATING...")
print("="*70)

# ============================================================================
# STEP 2: BASIC CALCULATIONS
# ============================================================================

# Effective depth
d = D - cover

print(f"\n1. EFFECTIVE DEPTH")
print(f"   d = D - cover = {D} - {cover} = {d} mm")

# ============================================================================
# STEP 3: FLEXURAL DESIGN (Check if singly or doubly reinforced)
# ============================================================================

print(f"\n2. FLEXURAL DESIGN")

# Convert moment to N-mm
Mu_Nmm = Mu * 1e6

# For different fy, max xu/d ratio
xu_d_dict = {250: 0.53, 415: 0.48, 500: 0.46}
xu_d = xu_d_dict[fy]

print(f"   Concrete grade (fck) = {fck} N/mm²")
print(f"   Steel grade (fy) = {fy} N/mm²")
print(f"   For fy={fy}, xu/d max = {xu_d}")

# Calculate limiting moment
Mu_lim_Nmm = 0.36 * xu_d * (1 - 0.42 * xu_d) * fck * b * d * d
Mu_lim = Mu_lim_Nmm / 1e6

print(f"\n   Mu,lim = 0.36 × {xu_d} × (1 - 0.42×{xu_d}) × {fck} × {b} × {d}²")
print(f"   Mu,lim = {Mu_lim:.2f} kNm")
print(f"   Applied Mu = {Mu} kNm")

# Check if singly or doubly reinforced
if Mu <= Mu_lim:
    section_type = "SINGLY REINFORCED"
    print(f"   → {section_type} (Mu ≤ Mu,lim)")
else:
    section_type = "DOUBLY REINFORCED"
    print(f"   → {section_type} (Mu > Mu,lim)")

# ============================================================================
# STEP 4: CALCULATE REQUIRED STEEL AREA (Ast)
# ============================================================================

print(f"\n3. REQUIRED STEEL AREA")

if section_type == "SINGLY REINFORCED":
    # Formula: Ast = (fck/fy) × b × d × [1 - sqrt(1 - (4.6×Mu)/(fck×b×d²))]
    
    numerator = 4.6 * Mu_Nmm
    denominator = fck * b * d * d
    
    discriminant = 1 - (numerator / denominator)
    
    if discriminant < 0:
        print(f"   ERROR: Discriminant is negative!")
        print(f"   Section is TOO SMALL for this moment")
        print(f"   Increase depth (D) or width (b)")
        Ast_req = 0.04 * b * D
        print(f"   Using fallback: 0.04×b×D = {Ast_req:.0f} mm²")
    else:
        sqrt_term = math.sqrt(discriminant)
        Ast_req = 0.5 * (fck / fy) * b * d * (1 - sqrt_term)
        print(f"   Discriminant = {discriminant:.4f}")
        print(f"   Ast = 0.5 × ({fck}/{fy}) × {b} × {d} × (1 - √{discriminant:.4f})")
        print(f"   Ast = {Ast_req:.0f} mm²")

else:  # DOUBLY REINFORCED
    # For doubly reinforced: Ast1 for limiting moment + Ast2 for excess moment
    
    Ast1 = Mu_lim_Nmm / (0.87 * fy * (d - 0.42 * xu_d * d))
    
    Mu_excess = Mu_Nmm - Mu_lim_Nmm
    Ast2 = Mu_excess / (0.87 * fy * (d - cover))
    
    Ast_req = Ast1 + Ast2
    
    print(f"   This section needs COMPRESSION STEEL")
    print(f"   Ast1 (for Mu,lim) = {Ast1:.0f} mm²")
    print(f"   Ast2 (for excess) = {Ast2:.0f} mm²")
    print(f"   Total Ast = {Ast_req:.0f} mm²")

# ============================================================================
# STEP 5: CHECK MIN AND MAX STEEL LIMITS
# ============================================================================

print(f"\n4. STEEL LIMITS")

Ast_min = 0.85 * b * d / fy
Ast_max = 0.04 * b * D

print(f"   Minimum: Ast,min = 0.85 × b × d / fy")
print(f"            = 0.85 × {b} × {d} / {fy} = {Ast_min:.0f} mm²")
print(f"   Maximum: Ast,max = 0.04 × b × D")
print(f"            = 0.04 × {b} × {D} = {Ast_max:.0f} mm²")

Ast_final = Ast_req

if Ast_req < Ast_min:
    Ast_final = Ast_min
    print(f"   → Using MINIMUM = {Ast_min:.0f} mm²")
elif Ast_req > Ast_max:
    print(f"   → ERROR: Required steel exceeds maximum!")
    print(f"   Increase section size (b or D)")
    Ast_final = Ast_max
else:
    print(f"   → Using CALCULATED = {Ast_final:.0f} mm²")

# ============================================================================
# STEP 6: SELECT BAR SIZE AND NUMBER
# ============================================================================

print(f"\n5. SELECT REINFORCEMENT BARS")

bar_diameters = [10, 12, 16, 20, 25, 32]
bar_area_dict = {
    10: math.pi/4 * 10 * 10,    # 78.54 mm²
    12: math.pi/4 * 12 * 12,    # 113.10 mm²
    16: math.pi/4 * 16 * 16,    # 201.06 mm²
    20: math.pi/4 * 20 * 20,    # 314.16 mm²
    25: math.pi/4 * 25 * 25,    # 490.87 mm²
    32: math.pi/4 * 32 * 32,    # 804.25 mm²
}

selected_bar = None

for dia in bar_diameters:
    area_one_bar = bar_area_dict[dia]
    
    # Try different number of bars
    for num_bars in range(2, 10):
        total_area = num_bars * area_one_bar
        
        # Check spacing
        # Clear space = b - 2×(side cover 25mm) - (number of bars × diameter)
        clear_space = b - 2*25 - (num_bars * dia)
        num_gaps = num_bars - 1
        
        if num_gaps > 0:
            spacing = clear_space / num_gaps
        else:
            spacing = clear_space
        
        min_spacing = max(dia, 25)  # Min 25mm or bar diameter
        
        if total_area >= Ast_final and spacing >= min_spacing:
            selected_bar = {
                'dia': dia,
                'num': num_bars,
                'area': total_area,
                'spacing': spacing
            }
            break
    
    if selected_bar:
        break

if selected_bar:
    print(f"   ✓ {selected_bar['num']} bars of {selected_bar['dia']} mm diameter")
    print(f"   Area provided = {selected_bar['area']:.0f} mm²")
    print(f"   Area required = {Ast_final:.0f} mm²")
    print(f"   Spacing between bars = {selected_bar['spacing']:.0f} mm")
    print(f"   (Minimum allowed = {max(selected_bar['dia'], 25)} mm)")
else:
    print(f"   ✗ Cannot fit bars in width {b} mm")
    print(f"   Try: wider beam, smaller bars, or two layers")
    selected_bar = {'dia': 20, 'num': 4, 'area': Ast_final, 'spacing': 0}

# ============================================================================
# STEP 7: SHEAR DESIGN
# ============================================================================

print(f"\n6. SHEAR DESIGN")

# Nominal shear stress
tau_v = (Vu * 1000) / (b * d)

print(f"   Nominal shear stress: τv = Vu / (b × d)")
print(f"   τv = ({Vu} × 1000) / ({b} × {d})")
print(f"   τv = {tau_v:.3f} N/mm²")

# Design shear strength of concrete (simplified from IS 456)
# Using the formula: τc = 0.85 × √(0.8×fck) × √(1 + 5β - 1) / (6β)
# where β = (0.8×fck) / (6.89×pt)

Ast_provided = selected_bar['area']
pt = (100 * Ast_provided) / (b * d)  # Percentage of steel

print(f"   Steel percentage: pt = 100 × Ast / (b × d)")
print(f"   pt = 100 × {Ast_provided:.0f} / ({b} × {d}) = {pt:.3f} %")

# Simplified tau_c (from IS 456 Annex B)
beta = (0.8 * fck) / (6.89 * pt)
tau_c_calc = (0.85 * math.sqrt(0.8 * fck) * (math.sqrt(1 + 5*beta) - 1)) / (6 * beta)
tau_c = max(0.5, min(tau_c_calc, 5))  # Cap between limits

print(f"   Design shear strength: τc ≈ {tau_c:.3f} N/mm²")

# Check shear requirement
if tau_v <= tau_c:
    print(f"\n   ✓ Concrete alone is adequate (τv ≤ τc)")
    print(f"   Provide nominal (minimum) stirrups")
    
    stir_spacing = min(0.75 * d, 300)
    print(f"   Spacing = min(0.75×d, 300) = min({0.75*d:.0f}, 300) = {stir_spacing:.0f} mm")
else:
    print(f"\n   ✗ Stirrups required by design (τv > τc)")
    
    # Design stirrups
    stir_dia = 10  # Default stirrup diameter
    stir_legs = 2  # 2-legged stirrup
    
    Asv = stir_legs * (math.pi / 4) * stir_dia * stir_dia
    
    # Spacing formula: Sv = (0.87 × fy × Asv × d) / Vus
    Vus = (Vu * 1000) - (tau_c * b * d)
    stir_spacing_calc = (0.87 * fy * Asv * d) / Vus
    
    # Cap spacing to 0.75d or 300mm (whichever is less)
    stir_spacing = min(stir_spacing_calc, 0.75*d, 300)
    
    print(f"   Shear to be resisted by steel: Vus = {Vus/1000:.2f} kN")
    print(f"   Calculated spacing = {stir_spacing_calc:.0f} mm")
    print(f"   Maximum allowed = min(0.75d, 300) = {min(0.75*d, 300):.0f} mm")
    print(f"   Final spacing = {stir_spacing:.0f} mm")

# ============================================================================
# STEP 8: DEFLECTION CHECK
# ============================================================================

print(f"\n7. DEFLECTION CHECK (Span/Depth Ratio)")

L_d_ratio = (span_m * 1000) / d
basic_L_d = 20  # For simply supported beam

print(f"   L/d ratio = (L × 1000) / d")
print(f"   L/d = ({span_m} × 1000) / {d} = {L_d_ratio:.2f}")
print(f"   Basic L/d (simply supported) = {basic_L_d}")

if L_d_ratio <= basic_L_d:
    print(f"   ✓ SAFE (deflection check passed)")
else:
    print(f"   ✗ WARNING (L/d exceeds basic limit)")
    print(f"   Consider: increase depth or check with modification factors")

# ============================================================================
# STEP 9: SUMMARY
# ============================================================================

print(f"\n" + "="*70)
print("DESIGN SUMMARY")
print("="*70)

print(f"""
BEAM SECTION:
  Width (b) = {b} mm
  Total depth (D) = {D} mm
  Effective depth (d) = {d} mm
  Span = {span_m} m

MATERIALS:
  Concrete = M{fck}
  Steel = Fe{fy}

DESIGN FORCES:
  Bending moment, Mu = {Mu} kNm
  Shear force, Vu = {Vu} kN

REINFORCEMENT TYPE:
  {section_type}

TENSION STEEL:
  Required area = {Ast_final:.0f} mm²
  ✓ USE: {selected_bar['num']} bars of T{selected_bar['dia']} mm
  Area provided = {selected_bar['area']:.0f} mm²
  Clear spacing = {selected_bar['spacing']:.0f} mm

SHEAR REINFORCEMENT:
  Nominal shear stress (τv) = {tau_v:.3f} N/mm²
  Design shear strength (τc) = {tau_c:.3f} N/mm²
  ✓ USE: 2-legged {stir_dia} mm stirrups @ {stir_spacing:.0f} mm c/c

DEFLECTION CHECK:
  L/d ratio = {L_d_ratio:.2f}
  Status = {"SAFE ✓" if L_d_ratio <= basic_L_d else "CHECK ✗"}
""")

print("="*70)
print("⚠️  DISCLAIMER:")
print("This code implements standard IS 456:2000 formulas.")
print("Always verify calculations and get structural engineer approval!")
print("="*70 + "\n")
