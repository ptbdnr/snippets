import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def explain_convolution():
    """
    Explain convolutional processing in simple terms with an animation.
    """
    # Create a more interesting picture (e.g., a simple pattern)
    picture = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])
    
    # Create a more interesting filter (e.g., edge detection)
    filter = np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ])
    
    # Convolution is like sliding this filter over the picture
    def apply_filter(picture, filter):
        filter_size = filter.shape[0]
        result = np.zeros((picture.shape[0] - filter_size + 1, picture.shape[1] - filter_size + 1))
        for i in range(result.shape[0]):
            for j in range(result.shape[1]):
                result[i, j] = np.sum(picture[i:i+filter_size, j:j+filter_size] * filter)
        return result
    
    # Create an animation to show the convolution process
    fig, axes = plt.subplots(1, 4, figsize=(15, 5))
    axes[0].set_title('Original Picture')
    axes[1].set_title('Filter')
    axes[2].set_title('Convolution Process')
    axes[3].set_title('Final Convolved Picture')
    img_original = axes[0].imshow(picture, cmap='gray')
    img_filter = axes[1].imshow(filter, cmap='gray')
    img_convolved = axes[2].imshow(picture, cmap='gray')
    img_final = axes[3].imshow(picture, cmap='gray')
    
    def update(frame):
        filter_size = filter.shape[0]
        i = frame // (picture.shape[1] - filter_size + 1)
        j = frame % (picture.shape[1] - filter_size + 1)
        picture_copy = picture.copy()
        picture_copy[i:i+filter_size, j:j+filter_size] = picture_copy[i:i+filter_size, j:j+filter_size] * filter
        
        # Highlight the filter area
        highlight = np.zeros_like(picture)
        highlight[i:i+filter_size, j:j+filter_size] = 1
        img_convolved.set_array(picture_copy + highlight * 0.5) # Add 0.5 to highlight the filter area
        return [img_convolved]
    
    frames = (picture.shape[0] - filter.shape[0] + 1) * (picture.shape[1] - filter.shape[0] + 1)
    ani = animation.FuncAnimation(fig, update, frames=frames, repeat=False)
    
    # Show the final stage after filtering
    convolved_picture = apply_filter(picture, filter)
    img_final.set_array(convolved_picture)
    
    plt.show()

if __name__ == "__main__":
    explain_convolution()