import sqlite3

colors = [
    "#f21818",
    "#f25918",
    "#f29b18",
    "#f2dc18",
    "#c6f218",
    "#85f218",
    "#43f218",
    "#18f22e",
    "#18f26f",
    "#18f2b0",
    "#18f2f2",
    "#18b0f2",
    "#186ff2",
    "#182ef2",
    "#4318f2",
    "#8518f2",
    "#c618f2",
    "#f218dc",
]
db_path = "test.db"
image_id = 2

def create_connection(db_file):  
    """ create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
    except sqlite3.Error as e:
        print(e)    
    conn.row_factory = sqlite3.Row  # Enable named column access
    conn.enable_load_extension(True)
    conn.load_extension("mod_spatialite")  
    return conn

conn = create_connection(db_path)
cursor = conn.cursor()

# Create SVG file for cuts polygons

cursor.execute(f"SELECT image_width, image_height FROM images WHERE image_id={image_id}")
image_row = cursor.fetchone()
image_width = image_row['image_width']
image_height = image_row['image_height']
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{image_width}" height="{image_height}" viewBox="0 0 {image_width} {image_height}">'
svg += '<rect width="100%" height="100%" fill="black"/>'

cursor.execute(f"SELECT tree_id, AsSVG(ScaleCoords(cut_poly, 1.0, -1.0),1) AS cut_poly_svg_path FROM cuts WHERE image_id={image_id}")
cut_rows = cursor.fetchall()

for i, cut_row in enumerate(cut_rows):
    cut_poly_svg_path = cut_row['cut_poly_svg_path']
    color = colors[i % len(colors)]
    svg += f'<path d="{cut_poly_svg_path}" fill="{color}"/>'
svg += '</svg>'
    
with open(f'img_{image_id}_cuts_polygons.svg', 'w') as f:
    f.write(svg)    
    
print(f"SVG file 'img_{image_id}_cuts_polygons.svg' created successfully.")

# Create SVG file for tree polygons

cursor.execute(f"SELECT image_width, image_height FROM images WHERE image_id={image_id}")
image_row = cursor.fetchone()
image_width = image_row['image_width']
image_height = image_row['image_height']
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{image_width}" height="{image_height}" viewBox="0 0 {image_width} {image_height}">'
svg += '<rect width="100%" height="100%" fill="black"/>'

cursor.execute(f"SELECT AsSVG(tree_poly,1) AS tree_poly_svg_path FROM trees WHERE image_id={image_id}")
tree_rows = cursor.fetchall()

for i, tree_row in enumerate(tree_rows):
    tree_poly_svg_path = tree_row['tree_poly_svg_path']
    color = colors[i % len(colors)]
    svg += f'<path d="{tree_poly_svg_path}" fill="{color}"/>'
svg += '</svg>'
    
with open(f'img_{image_id}_tree_polygons.svg', 'w') as f:
    f.write(svg)    
    
print(f"SVG file 'img_{image_id}_tree_polygons.svg' created successfully.")