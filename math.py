import streamlit as st
import sympy as sp
import re

# --- STAGE 1: CONFIG ---
st.set_page_config(page_title="PCTB Ex 2.2 Final Solver", layout="centered")

# --- STAGE 2: SYNTAX FIXER ---
def clean_input(text):
    # Fixes implicit multiplication like 2x or ax
    text = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', text)
    text = re.sub(r'([a-ce-ln-z])([x])', r'\1*\2', text)
    return text

st.title("🎓 Punjab Board: Ch 2 Solver (Final Version)")
st.write("This version shows the subtraction of powers to reach the final answer.")

query = st.text_input("Enter Function:", value="(a*x+b)**3")

if query:
    try:
        # Define Symbols
        x, dx, a, b = sp.symbols('x delta_x a b')
        f = sp.sympify(clean_input(query))
        
        # Logic to extract base and exponent
        if f.is_Pow:
            p_base = f.base
            p_exp = f.exp
        else:
            p_base = f
            p_exp = 1

        # --- STEP I & II ---
        st.markdown("### Step I & II: Increments")
        f_inc = f.subs(x, x + dx)
        st.latex(f"y + \\delta y = {sp.latex(f_inc)}")
        
        # Expand inner part to isolate the 'a*dx' part
        inner_inc = sp.simplify(sp.expand(f_inc.base if f.is_Pow else f_inc) - p_base)
        
        st.write("Subtracting $y$ and factoring out the common term:")
        st.latex(f"\\delta y = {sp.latex(f)} \\left[ \\left( 1 + \\frac{{{sp.latex(inner_inc)}}}{{{sp.latex(p_base)}}} \\right)^{{{sp.latex(p_exp)}}} - 1 \\right]")

        # --- STEP III: DETAILED BINOMIAL EXPANSION ---
        st.markdown("### Step III: Binomial Series Expansion")
        st.write("Using formula: $(1+X)^n = 1 + nX + \\frac{n(n-1)}{2!}X^2 + \\dots$")
        
        # Display the substitution
        st.latex(f"\\delta y = {sp.latex(f)} \\left[ \\left( 1 + {sp.latex(p_exp)} \\left( \\frac{{{sp.latex(inner_inc)}}}{{{sp.latex(p_base)}}} \\right) + \\frac{{{sp.latex(p_exp)}({sp.latex(p_exp-1)})}}{{2!}} \\left( \\frac{{{sp.latex(inner_inc)}}}{{{sp.latex(p_base)}}} \\right)^2 + \\dots \\right) - 1 \\right]")
        
        st.write("Cancelling 1 and taking $\\delta x$ common:")
        
        # This is the coefficient inside the bracket: n*a / (ax+b)
        coeff_dx = sp.simplify(p_exp * (inner_inc / dx) / p_base)
        
        st.latex(f"\\delta y = {sp.latex(f)} \\cdot \\delta x \\left[ {sp.latex(coeff_dx)} + \\text{{terms with }} \\delta x \\right]")

        # --- STEP IV: LIMIT ---
        st.markdown("### Step IV: Taking Limit $\\delta x \\to 0$")
        st.latex(f"\\frac{{dy}}{{dx}} = \\lim_{{\\delta x \\to 0}} \\frac{{\\delta y}}{{\\delta x}}")
        
        # Step before final power simplification
        st.latex(f"\\frac{{dy}}{{dx}} = {sp.latex(f)} \\cdot \\left( {sp.latex(coeff_dx)} \\right)")
        
        # --- FINAL LEVEL SIMPLIFICATION ---
        # Forces subtraction of exponents: (ax+b)^3 * 1/(ax+b) -> (ax+b)^2
        # We calculate the final derivative directly via SymPy but format it nicely
        true_derivative = sp.diff(f, x)
        final_answer = sp.factor(true_derivative)

        st.write("Applying Laws of Exponents to combine $(ax+b)$ terms:")
        st.success(f"### Final Answer:  \n ${sp.latex(final_answer)}$")

    except Exception as e:
        st.error(f"Logic Error: {e}")
