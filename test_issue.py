#!/usr/bin/env python3
"""
Minimal reproduction of the dataLim issue without numpy
"""

import sys
sys.path.insert(0, 'lib')

# Mock numpy array - simple list that numpy functions expect
class MockArray:
    def __init__(self, data):
        self.data = data
        self.shape = (len(data),) if hasattr(data[0], '__len__') else (1, len(data))
        self.dtype = float
    
    def __getitem__(self, idx):
        return self.data[idx]
    
    def __len__(self):
        return len(self.data)

# Add to sys.modules so imports work
sys.modules['numpy'] = type('numpy', (), {
    'array': lambda x: MockArray(x),
    'promote_types': lambda x, y: float,
    'float32': float,
    'row_stack': lambda x: MockArray(x),
    'cumsum': lambda x, axis=None, dtype=None: MockArray(x),
    'sum': sum,
    'zeros_like': lambda x: MockArray([0] * len(x)),
    'hstack': lambda x: MockArray([item for sublist in x for item in sublist]),
    'diff': lambda x: MockArray([x.data[i+1] - x.data[i] for i in range(len(x)-1)]),
})()

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

# Now we can test the specific issue
try:
    import matplotlib.pyplot as plt
    from matplotlib.transforms import Bbox

    def print_datalim(*ax):
        for ax_ in ax:
            print(ax_.dataLim.intervaly, end=' / ')
        print()

    # Simple test data
    x = [0, 1]
    y1 = [-22.7, 26.6]
    y2 = [-0.085, -2.98]

    print("Testing dataLim issue reproduction:")

    fig, ax1 = plt.subplots()

    # Test stackplot
    ax1.stackplot(x, y1)
    print("After stackplot on ax1:", end=" ")
    print_datalim(ax1)

    # Create twinx
    ax2 = ax1.twinx()  
    print("After creating twinx:", end=" ")
    print_datalim(ax1, ax2)

    # Plot on ax2
    ax2.plot(x, y2)
    print("After plot on ax2:", end=" ")
    print_datalim(ax1, ax2)

    plt.close('all')
    print("Test completed successfully")

except Exception as e:
    print(f"Error during test: {e}")
    import traceback
    traceback.print_exc()