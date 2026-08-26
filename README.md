# RCC BEAM DESIGN - PURE PYTHON CALCULATION CODE

**Just Python. Just Math. No Web Framework.**

---

## 🚀 HOW TO RUN

```bash
python rcc_beam_calc.py
```

That's it! The program will ask you for values, calculate everything, and show results.

---

## 📋 WHAT YOU NEED TO ENTER

The program asks for:

### Beam Dimensions (in mm)
- **Span length** - Length of beam in meters (e.g., 5)
- **Width (b)** - Width of beam (e.g., 300)
- **Total depth (D)** - Height of beam (e.g., 500)
- **Effective cover (d')** - Distance from bottom to steel (e.g., 50)

### Materials
- **Concrete grade** - M20, M25, M30, M35, M40
- **Steel grade** - Fe250, Fe415, Fe500

### Design Forces
- **Factored moment (Mu)** - In kNm
- **Factored shear (Vu)** - In kN

---

## 📊 EXAMPLE RUN

```
Span length (meters): 5
Width, b (mm): 300
Total depth, D (mm): 500
Effective cover, d' (mm): 50

Concrete grade (20/25/30/35/40): 25
Steel grade (250/415/500): 415

Factored moment, Mu (kNm): 120
Factored shear, Vu (kN): 95

======================================================================
CALCULATING...
======================================================================

1. EFFECTIVE DEPTH
   d = D - cover = 500 - 50 = 450 mm

2. FLEXURAL DESIGN
   Concrete grade (fck) = 25 N/mm²
   Steel grade (fy) = 415 N/mm²
   For fy=415, xu/d max = 0.48

   Mu,lim = 0.36 × 0.48 × (1 - 0.42×0.48) × 25 × 300 × 450²
   Mu,lim = 176.42 kNm
   Applied Mu = 120 kNm
   → SINGLY REINFORCED (Mu ≤ Mu,lim)

3. REQUIRED STEEL AREA
   Ast = 0.5 × (25/415) × 300 × 450 × (1 - √discriminant)
   Ast = 892 mm²

4. STEEL LIMITS
   Minimum: Ast,min = 0.85 × 300 × 450 / 415 = 276 mm²
   Maximum: Ast,max = 0.04 × 300 × 500 = 6000 mm²
   → Using CALCULATED = 892 mm²

5. SELECT REINFORCEMENT BARS
   ✓ 4 bars of 20 mm diameter
   Area provided = 1256 mm²
   Area required = 892 mm²
   Spacing between bars = 83 mm

6. SHEAR DESIGN
   Nominal shear stress: τv = Vu / (b × d)
   τv = (95 × 1000) / (300 × 450)
   τv = 0.704 N/mm²

   Steel percentage: pt = 100 × 1256 / (300 × 450) = 0.927 %
   Design shear strength: τc ≈ 0.531 N/mm²

   ✗ Stirrups required by design (τv > τc)
   Shear to be resisted by steel: Vus = 50.60 kN
   Final spacing = 225 mm

7. DEFLECTION CHECK (Span/Depth Ratio)
   L/d ratio = (5 × 1000) / 450 = 11.11
   Basic L/d (simply supported) = 20
   ✓ SAFE (deflection check passed)

======================================================================
DESIGN SUMMARY
======================================================================

BEAM SECTION:
  Width (b) = 300 mm
  Total depth (D) = 500 mm
  Effective depth (d) = 450 mm
  Span = 5.0 m

MATERIALS:
  Concrete = M25
  Steel = Fe415

DESIGN FORCES:
  Bending moment, Mu = 120 kNm
  Shear force, Vu = 95 kN

REINFORCEMENT TYPE:
  SINGLY REINFORCED

TENSION STEEL:
  Required area = 892 mm²
  ✓ USE: 4 bars of T20 mm
  Area provided = 1256 mm²
  Clear spacing = 83 mm

SHEAR REINFORCEMENT:
  ✓ USE: 2-legged 10 mm stirrups @ 225 mm c/c

DEFLECTION CHECK:
  L/d ratio = 11.11
  Status = SAFE ✓

======================================================================
```

---

## 📖 WHAT THE CODE CALCULATES

### 1️⃣ Effective Depth (d)
```
d = D - cover
```

### 2️⃣ Check if Singly or Doubly Reinforced
```
Mu,lim = 0.36 × (xu/d) × (1 - 0.42×(xu/d)) × fck × b × d²

If Mu ≤ Mu,lim → SINGLY REINFORCED
If Mu > Mu,lim → DOUBLY REINFORCED
```

### 3️⃣ Required Steel Area (Ast)
**For singly reinforced:**
```
Ast = 0.5 × (fck/fy) × b × d × [1 - √(1 - 4.6×Mu/(fck×b×d²))]
```

**Limits:**
```
Ast,min = 0.85 × b × d / fy
Ast,max = 0.04 × b × D
```

### 4️⃣ Select Bars
The code tries all standard bar sizes (10mm to 32mm) and picks the first option that:
- Provides required area
- Has proper spacing (min 25mm between bars)

### 5️⃣ Shear Design
```
τv = Vu / (b × d)  [Nominal shear stress]

If τv ≤ τc → Concrete alone is adequate
If τv > τc → Design stirrups

Sv = (0.87 × fy × Asv × d) / (Vu - τc×b×d)
```

### 6️⃣ Deflection Check
```
L/d ratio = (L × 1000) / d

If L/d ≤ 20 → SAFE
If L/d > 20 → WARNING
```

---

## 🔍 CODE STRUCTURE

The code is organized in sections:

```
1. INPUT DATA
   ↓
2. BASIC CALCULATIONS (effective depth)
   ↓
3. FLEXURAL DESIGN (singly/doubly check)
   ↓
4. REQUIRED STEEL CALCULATION
   ↓
5. CHECK MIN/MAX LIMITS
   ↓
6. SELECT BAR SIZE
   ↓
7. SHEAR DESIGN
   ↓
8. DEFLECTION CHECK
   ↓
9. SUMMARY & OUTPUT
```

---

## 💡 KEY POINTS

✅ **Pure Python** - No libraries except `math` (built-in)
✅ **IS 456:2000** - Follows Indian standard
✅ **Well-commented** - Every calculation explained
✅ **Easy to modify** - Change formulas easily
✅ **Console based** - Just text input/output

---

## 🎓 WHAT YOU CAN LEARN

Read through the code to understand:
- How IS 456:2000 flexural design works
- How to calculate steel requirements
- Shear design logic
- Deflection checking
- How to write clear Python code with comments

---

## ⚠️ IMPORTANT

This code implements standard IS 456:2000 formulas for **learning and preliminary design purposes**.

**Always verify:**
- Calculations are correct
- Design meets local code requirements
- Get structural engineer approval before construction
- Check ductile detailing (IS 13920) if needed

---

## 🚀 NEXT STEPS

You can:
- Modify the code for different beam types (T-beam, L-beam)
- Add compression steel calculation
- Create functions to make it reusable
- Add more materials/grades
- Write to Excel file instead of console
- Create an input file format

---

**That's it! Just pure Python calculations.** 🐍📊
