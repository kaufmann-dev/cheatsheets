import math

def calculate_positions(hex_width, spacing_distance):
    """
    Calculate transformation values for 6 objects positioned around a hexagonal pattern.
    The hexagon is rotated 180 degrees on Y-axis (flat sides on top/bottom).
    
    Args:
        hex_width (float): Width of the hexagon (flat side to flat side)
        spacing_distance (float): Additional spacing distance from center
    
    Returns:
        dict: Dictionary containing all calculated values and object positions
    """
    # Calculate hexagon depth (point to point distance)
    hex_depth = hex_width * (math.sqrt(3) / 2)
    
    # Calculate positioning values
    diagonal_x_offset = (hex_depth / 2) + (spacing_distance / 2)
    diagonal_z_offset = ((math.sqrt(3) / 2) * hex_depth) + (spacing_distance / 2)
    horizontal_offset = hex_depth + spacing_distance
    
    # Define object transformations
    objects = {
        "east": {"x": horizontal_offset, "z": 0},
        "west": {"x": -horizontal_offset, "z": 0},
        "south_east": {"x": diagonal_x_offset, "z": diagonal_z_offset},
        "south_west": {"x": -diagonal_x_offset, "z": diagonal_z_offset},
        "north_east": {"x": diagonal_x_offset, "z": -diagonal_z_offset},
        "north_west": {"x": -diagonal_x_offset, "z": -diagonal_z_offset}
    }
    
    return {
        "hex_width": hex_width,
        "spacing_distance": spacing_distance,
        "hex_depth": hex_depth,
        "diagonal_x_offset": diagonal_x_offset,
        "diagonal_z_offset": diagonal_z_offset,
        "horizontal_offset": horizontal_offset,
        "objects": objects
    }

def print_results(results):
    """Print the calculated results in a formatted way."""
    print("=" * 39)
    print("HEXAGONAL OBJECT POSITIONING CALCULATOR")
    print("=" * 39)
    print(f"{'Hexagon width':<20} : {results['hex_width']}")
    print(f"{'Spacing distance':<20} : {results['spacing_distance']}")
    print(f"{'Calculated hex depth':<20} : {results['hex_depth']:.4f}")
    print()
    print("Positioning Values")
    print("-" * 18)
    print(f"{'Diagonal X offset':<16} : {results['diagonal_x_offset']:.4f}")
    print(f"{'Diagonal Z offset':<16} : {results['diagonal_z_offset']:.4f}")
    print(f"{'Horizontal offset':<16} : {results['horizontal_offset']:.4f}")
    print()
    print("Object Transformations")
    print("-" * 22)
    
    # Find the maximum length of x values for proper alignment
    max_x_length = 0
    formatted_x_values = {}
    
    for obj_name, coords in results['objects'].items():
        x_val = f"{coords['x']:.4f}"
        if coords['x'] >= 0:
            x_val = " " + x_val
        formatted_x_values[obj_name] = x_val
        max_x_length = max(max_x_length, len(x_val))
    
    for obj_name, coords in results['objects'].items():
        formatted_name = obj_name.replace('_', ' ')
        x_val = formatted_x_values[obj_name]
        
        z_val = f"{coords['z']:.4f}"
        if coords['z'] >= 0:
            z_val = " " + z_val
        
        spaces_needed = max_x_length - len(x_val)
        print(f"Object {formatted_name:<11} : x= {x_val},{' ' * spaces_needed} z= {z_val}")

def main():
    """Main function to run the program."""
    try:
        # Get user input
        hex_width = float(input("Enter hexagon width (flat side to flat side): "))
        spacing_distance = float(input("Enter spacing distance: "))
        
        # Calculate positions
        results = calculate_positions(hex_width, spacing_distance)
        
        # Print results
        print_results(results)
        
    except ValueError:
        print("Error: Please enter valid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()