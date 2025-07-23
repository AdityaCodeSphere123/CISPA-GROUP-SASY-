import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

def calculate_d(e, v):
    """
    Calculate d = ceil(2*e/v) + 1
    
    Parameters:
    e: user input value
    v: user input value
    """
    if v == 0:
        return float('inf')
    return math.ceil(2 * e / v) + 1

def calculate_a(n, d):
    """
    Calculate a = n*d/4
    
    Parameters:
    n: variable from 1 to 100
    d: calculated value from calculate_d function
    """
    return n * d / 4

def calculate_expression(v, e, y, n):
    """
    Calculate x = v[1-(1-(a/v)^(y-1))] - yn
    where a = n*d/4 and d = ceil(2*e/v) + 1
    
    Parameters:
    v: user input value
    e: user input value
    y: variable from 1 to 1000
    n: variable from 1 to 100
    """
    # Handle edge cases to avoid division by zero or invalid operations
    if v == 0:
        return np.full_like(y, np.nan)
    
    # Calculate d for the given v and e
    d = calculate_d(e, v)
    
    # Calculate a for each n value
    a = calculate_a(n, d)
    
    # Calculate the expression step by step with overflow handling
    ratio = a / v
    
    # Use numpy's warning settings to handle overflow
    with np.errstate(over='ignore', invalid='ignore'):
        # Check for potential overflow before computing power
        # If ratio^(y-1) would be too large, set to inf
        log_ratio = np.log(np.abs(ratio))
        log_power = (y - 1) * log_ratio
        
        # Set a reasonable threshold to avoid overflow (e.g., exp(700) ≈ 10^304)
        overflow_threshold = 700
        
        power_term = np.where(
            log_power > overflow_threshold,
            np.inf,
            np.power(ratio, y - 1)
        )
        
        inner_bracket = 1 - power_term
        outer_bracket = 1 - inner_bracket
        first_term = v * outer_bracket
        second_term = y * n
        
        x = first_term - second_term
    
    # Handle inf and -inf values
    x = np.where(np.isinf(x), np.nan, x)
    
    return x

def main():
    # Get user input
    try:
        v = float(input("Enter the value of v: "))
        e = float(input("Enter the value of e: "))
    except ValueError:
        print("Please enter valid numeric values.")
        return
    
    # Calculate d
    d = calculate_d(e, v)
    print(f"Calculated d = ceil(2*e/v) + 1 = {d}")
    
    # Create ranges for y and n
    y_range = np.arange(1, 101)  # 1 to 1000
    n_range = np.arange(1, 101)   # 1 to 100
    
    # Create meshgrid for 3D plotting
    Y, N = np.meshgrid(y_range, n_range)
    
    # Calculate the expression for all combinations
    X = calculate_expression(v, e, Y, N)
    
    # Filter out NaN and infinite values for plotting
    valid_mask = np.isfinite(X)
    
    # Check if we have any valid data
    if not np.any(valid_mask):
        print("Error: All calculated values are infinite or NaN.")
        print("This might happen when the parameters lead to numerical overflow.")
        print("Try using smaller values for v and e, or modify the ranges for y and n.")
        return
    
    # Find the minimum value and its indices (only among finite values)
    finite_X = np.where(valid_mask, X, np.inf)
    min_idx = np.unravel_index(np.argmin(finite_X), finite_X.shape)
    min_value = X[min_idx]
    min_y = Y[min_idx]
    min_n = N[min_idx]
    
    # Print the minimum value immediately
    print(f"\nMinimum value found: {min_value:.6f}")
    print(f"At coordinates: y = {min_y}, n = {min_n}")
    
    # For plotting, we'll mask invalid values
    X_plot = np.ma.masked_where(~valid_mask, X)
    
    # Create 3D plot
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create surface plot
    surf = ax.plot_surface(Y, N, X_plot, cmap='viridis', alpha=0.8)
    
    # Mark the minimum point
    ax.scatter([min_y], [min_n], [min_value], color='red', s=100, label=f'Minimum: ({min_y}, {min_n})')
    
    # Set labels and title
    ax.set_xlabel('y')
    ax.set_ylabel('n')
    ax.set_zlabel('x = v[1-(1-(a/v)^(y-1))] - yn')
    ax.set_title(f'3D Surface Plot\nv = {v}, e = {e}, d = {d}')
    
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    # Add legend
    ax.legend()
    
    # Calculate a sample value of 'a' for reference (using n=1)
    sample_a = calculate_a(1, d)
    
    # Print results
    print(f"\nResults:")
    print(f"v = {v}")
    print(f"e = {e}")
    print(f"d = ceil(2*e/v) + 1 = {d}")
    print(f"a = n*d/4 (varies with n, e.g., a = {sample_a} when n = 1)")
    print(f"Minimum value of x: {min_value:.6f}")
    print(f"Occurs at y = {min_y}, n = {min_n}")
    print(f"At minimum point: a = {calculate_a(min_n, d):.6f}")
    
    # Show the plot
    plt.tight_layout()
    plt.show()
    
    # Print additional statistics only for finite values
    finite_values = X[valid_mask]
    print(f"\nAdditional Statistics (finite values only):")
    print(f"Maximum value of x: {np.max(finite_values):.6f}")
    print(f"Mean value of x: {np.mean(finite_values):.6f}")
    print(f"Standard deviation: {np.std(finite_values):.6f}")
    print(f"Number of finite values: {len(finite_values)} out of {X.size}")
    print(f"Percentage of finite values: {100 * len(finite_values) / X.size:.2f}%")

if __name__ == "__main__":
    main()