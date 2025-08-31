"""
Test for the twinx stackplot dataLim issue

This test reproduces the bug where dataLims get replaced by inf 
for charts with twinx if ax1 is a stackplot.
"""

import sys
sys.path.insert(0, '/home/runner/work/swe-bench-verified-matplotlib__matplotlib-26208/swe-bench-verified-matplotlib__matplotlib-26208/lib')

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms

def test_twinx_stackplot_datalim():
    """Test that dataLim doesn't get corrupted to inf when using twinx with stackplot."""
    
    # Test data
    x = np.array([0, 1])
    y1 = np.array([-22.7, 26.6])
    y2 = np.array([-0.085, -2.98])
    
    fig, ax1 = plt.subplots()
    
    # Create stackplot on ax1
    ax1.stackplot(x, y1)
    
    # Check ax1 has valid dataLim after stackplot
    ax1_datalim_y_before = ax1.dataLim.intervaly.copy()
    assert np.isfinite(ax1_datalim_y_before).all(), "ax1 dataLim should be finite after stackplot"
    print(f"ax1 dataLim y after stackplot: {ax1_datalim_y_before}")
    
    # Create twinx
    ax2 = ax1.twinx()
    
    # Check ax1 dataLim is still valid after twinx creation
    ax1_datalim_y_after_twinx = ax1.dataLim.intervaly.copy()
    assert np.isfinite(ax1_datalim_y_after_twinx).all(), "ax1 dataLim should still be finite after twinx"
    print(f"ax1 dataLim y after twinx: {ax1_datalim_y_after_twinx}")
    
    # Check ax2 has null/inf dataLim initially
    ax2_datalim_y_before = ax2.dataLim.intervaly.copy()
    print(f"ax2 dataLim y before plot: {ax2_datalim_y_before}")
    
    # Plot on ax2 - this is where the bug would occur
    ax2.plot(x, y2)
    
    # Check ax1 dataLim is still valid after plotting on ax2
    ax1_datalim_y_after_plot = ax1.dataLim.intervaly.copy()
    ax2_datalim_y_after_plot = ax2.dataLim.intervaly.copy()
    
    print(f"ax1 dataLim y after ax2.plot: {ax1_datalim_y_after_plot}")
    print(f"ax2 dataLim y after ax2.plot: {ax2_datalim_y_after_plot}")
    
    # This is the main test - ax1's dataLim should not become infinite
    assert np.isfinite(ax1_datalim_y_after_plot).all(), f"ax1 dataLim should not become infinite after plotting on ax2. Got: {ax1_datalim_y_after_plot}"
    assert np.isfinite(ax2_datalim_y_after_plot).all(), f"ax2 dataLim should be finite after plot. Got: {ax2_datalim_y_after_plot}"
    
    # Additional check: ax1's dataLim should be approximately the same as before
    # (allowing for small numerical differences)
    assert np.allclose(ax1_datalim_y_before, ax1_datalim_y_after_plot, rtol=1e-10), \
        f"ax1 dataLim should be preserved. Before: {ax1_datalim_y_before}, After: {ax1_datalim_y_after_plot}"
    
    plt.close('all')
    print("Test passed: ax1 dataLim preserved correctly!")

if __name__ == "__main__":
    try:
        test_twinx_stackplot_datalim()
        print("SUCCESS: All tests passed!")
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)