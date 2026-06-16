#!/usr/bin/env python3
"""
Demonstration of WarPy40K - A toy language using Warhammer 40K universe expressions.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from warpy40k import evaluate


def demo():
    """Run demonstration of WarPy40K language."""
    print("WarPy40K Language Demonstration")
    print("=" * 50)
    print()
    
    examples = [
        # Basic arithmetic
        ("1 + 2", "Basic addition"),
        ("2 * 3 + 4", "Arithmetic with precedence"),
        ("(1 + 2) * 3", "Parentheses override precedence"),
        ("10 / 2", "Division"),
        ("2 ^ 3", "Power operation"),
        
        # Boolean operations
        ("True AND False", "Logical AND"),
        ("True OR False", "Logical OR"),
        ("NOT True", "Logical NOT"),
        ("1 == 1", "Equality"),
        ("2 > 1", "Greater than"),
        
        # Warhammer 40K expressions
        ("Inquisition", "Inquisition - truth/judgment"),
        ("Inquisition 42", "Inquisition with target"),
        ("Emperor", "Emperor - divine power"),
        ("Emperor 100", "Emperor with target"),
        ("Chaos", "Chaos - corruption/randomness"),
        ("Bless 100", "Bless - positive modification"),
        ("Curse 100", "Curse - negative modification"),
        ("Purge 42", "Purge - destruction"),
        ("Exterminatus", "Exterminatus - total annihilation"),
        
        # Built-in constants
        ("FAITH", "FAITH constant"),
        ("CORRUPTION", "CORRUPTION constant"),
        ("POPULATION", "POPULATION constant"),
        
        # Built-in functions
        ("abs(-42)", "Absolute value"),
        ("min(1, 2, 3)", "Minimum value"),
        ("max(1, 2, 3)", "Maximum value"),
        ("pow(2, 3)", "Power function"),
        
        # Complex expressions
        ("Bless Emperor 100", "Combined: Bless + Emperor"),
        ("Inquisition Chaos", "Combined: Inquisition + Chaos"),
        ("2 + 3 * 4", "Mixed arithmetic"),
    ]
    
    for code, description in examples:
        try:
            result = evaluate(code)
            print(f"📝 {description}")
            print(f"   Code: {code}")
            print(f"   Result: {result}")
            print()
        except Exception as e:
            print(f"❌ {description}")
            print(f"   Code: {code}")
            print(f"   Error: {e}")
            print()
    
    print("=" * 50)
    print("Demo complete!")
    print()
    print("Try it yourself:")
    print("  python -c \"from warpy40k import evaluate; print(evaluate('your_code'))\"")


if __name__ == "__main__":
    demo()
