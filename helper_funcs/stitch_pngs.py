from PIL import Image

def stitch_pngs(image_paths, output_path):
    images = [Image.open(path) for path in image_paths]
    
    # Determine max height among all images
    max_height = max(img.height for img in images)
    
    # Resize each image to have the same height
    resized_images = []
    for img in images:
        if img.height != max_height:
            # Preserve aspect ratio
            new_width = int(img.width * (max_height / img.height))
            img = img.resize((new_width, max_height), Image.LANCZOS)
        resized_images.append(img)
    
    # Compute total width after resizing
    total_width = sum(img.width for img in resized_images)
    
    # Create blank stitched image
    stitched_image = Image.new('RGB', (total_width, max_height))
    
    # Paste images side by side
    x_offset = 0
    for img in resized_images:
        stitched_image.paste(img, (x_offset, 0))
        x_offset += img.width

    stitched_image.save(output_path)

if __name__ == "__main__":
    items = ['Energy Use', 'Energy Cost', 'Energy Use by sqft', 'Energy Cost by sqft', 'Carbon Emissions', 'Carbon Emissions by sqft']

    for item in items:
        path_one = './outputs/maximize/' + item.lower().replace(" ", "_") + '_savings_maximize.png'
        path_two = './outputs/maximize/' + item.lower().replace(" ", "_") + '_savings_bar_chart.png'
        output_path = './outputs/stitched/' + item.lower().replace(" ", "_") + '.png'
        stitch_pngs([path_one, path_two], output_path)


    stitch_pngs(['./outputs/maximize/num_buildings.png', './outputs/maximize/num_buildings_bar_chart.png'], './outputs/stitched/num_buildings.png')