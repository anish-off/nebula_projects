import streamlit as st
import os
import ezdxf
import networkx as nx
from shapely.geometry import Polygon

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background: #000000;  /* Solid black background */
        color: white;
        font-family: Arial, sans-serif;
    }
    
    .stApp {
        background: #000000;
    }

    h1 {
        font-size: 3rem;
        text-align: center;
        color: #4CAF50;
    }

    .upload-box {
        text-align: center;
        padding: 20px;
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        margin-top: 20px;
        background-color: rgba(255, 255, 255, 0.1);
    }

    .results-box {
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
        background-color: rgba(255, 255, 255, 0.1);
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 1.2rem;
        border: none;
        cursor: pointer;
    }

    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>Basement Area and Material Estimator</h1>", unsafe_allow_html=True)

# Function to safely extract numeric values
def safe_tuple_conversion(point):
    try:
        return (float(point[0]), float(point[1]))  # Convert coordinates to float
    except (ValueError, TypeError, IndexError):
        return None  # Return None if conversion fails

# Function to extract geometry from DXF file
def extract_geometry_from_dxf(file_path):
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()
    edges = []
    points = set()
    error_count = 0

    for entity in msp:
        try:
            if entity.dxftype() == "LINE":
                start = safe_tuple_conversion(entity.dxf.get("start", []))
                end = safe_tuple_conversion(entity.dxf.get("end", []))
                if start and end:
                    edges.append((start, end))
                    points.update([start, end])
            elif entity.dxftype() == "LWPOLYLINE":
                vertices = [safe_tuple_conversion(point[:2]) for point in entity.get_points() if len(point) >= 2]
                vertices = [v for v in vertices if v is not None]  # Remove None values
                for i in range(len(vertices)):
                    edges.append((vertices[i], vertices[(i + 1) % len(vertices)]))
                    points.update([vertices[i]])
        except Exception as e:
            error_count += 1

    if error_count > 0:
        st.warning(f"Skipped {error_count} entities due to errors in data formatting.")
    return list(points), edges

# Function to build graph and find closed cycles
def find_closed_cycles(points, edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    cycles = [cycle for cycle in nx.cycle_basis(G) if len(cycle) > 2]
    return cycles

# Function to calculate geometry (area)
def calculate_geometry(cycles):
    total_area = 0
    for cycle in cycles:
        try:
            polygon = Polygon(cycle)
            if polygon.is_valid and polygon.area > 0:
                total_area += polygon.area
        except Exception as e:
            st.error(f"Error processing cycle: {e}")
    return total_area

# File uploader
st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a DXF file", type=["dxf"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file is not None:
    # Save the uploaded file temporarily
    temp_file_path = "temp_uploaded.dxf"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Process the DXF file
    points, edges = extract_geometry_from_dxf(temp_file_path)
    cycles = find_closed_cycles(points, edges)
    basement_area = calculate_geometry(cycles)

    # Material estimations
    bricks = basement_area * 60  # Assuming 60 bricks per square unit
    cement = basement_area * 0.2  # Assuming 0.2 bags per square unit
    sand = basement_area * 0.5  # Assuming 0.5 cubic feet per square unit
    rebars = basement_area * 2  # Assuming 2 units of rebars per square unit
    tiles = basement_area * 1.1  # Assuming 1.1 tiles per square unit
    adhesive = basement_area * 4  # Assuming 4 kg adhesive per square unit
    paint = basement_area * 0.1  # Assuming 0.1 liters of paint per square unit
    cladding = basement_area * 0.67  # Assuming 0.67 panels per square unit
    putty = basement_area * 0.1  # Assuming 0.1 kg putty per square unit
    sealant = basement_area * 0.05  # Assuming 0.05 liters sealant per square unit

    # Display results
    st.markdown("<div class='results-box'>", unsafe_allow_html=True)
    st.write(f"### Walls")
    st.write(f"**Bricks Required:** {bricks:.0f}")
    st.write(f"**Cement Required:** {cement:.2f} bags")
    st.write(f"**Sand Required:** {sand:.2f} cubic feet")
    st.write(f"**Rebars Required:** {rebars:.2f} units")
    
    st.write(f"### Flooring")
    st.write(f"**Tiles Required:** {tiles:.0f}")
    st.write(f"**Adhesive Required:** {adhesive:.2f} kg")
    
    st.write(f"### Painting")
    st.write(f"**Paint Required:** {paint:.2f} liters")
    st.write(f"**Wall Cladding Required:** {cladding:.2f} panels")
    st.write(f"**Putty Required:** {putty:.2f} kg")
    st.write(f"**Sealant Required:** {sealant:.2f} liters")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Clean up temporary file
    os.remove(temp_file_path)