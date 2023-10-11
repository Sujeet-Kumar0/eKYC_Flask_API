from PIL import ImageEnhance, ImageFilter
import torchvision.transforms.functional as F


def crop_image(cutout_img, bbox, padding=0):
    # # increasing the contrast
    # contrast_enhancer = ImageEnhance.Contrast(cutout_img)
    # image_high_contrast = contrast_enhancer.enhance(1.5)
    # cutout_img = image_high_contrast.filter(ImageFilter.UnsharpMask(radius=1, percent=100))


    # Define the padding values
    padding_top = padding
    padding_bottom = padding
    padding_left = padding
    padding_right = padding

    # Calculate the new bounding box coordinates with padding
    bbox_with_padding = (
        bbox[0].item() - padding_left,
        bbox[1].item() - padding_top,
        bbox[2].item() + padding_right,
        bbox[3].item() + padding_bottom,
    )

    # Crop the image using the new bounding box coordinates
    cutout_img = F.crop(
        cutout_img,
        bbox_with_padding[1],
        bbox_with_padding[0],
        bbox_with_padding[3] - bbox_with_padding[1],
        bbox_with_padding[2] - bbox_with_padding[0],
    )

    return cutout_img
