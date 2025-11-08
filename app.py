import streamlit as st
from PIL import Image
import io

st.title("🧠 Smart Image Compressor")

def compress_image(image, quality=85, max_size=(1920, 1080)):
    """Compress an image with given quality and resize limit."""
    # Convert to RGB if needed (JPEG doesn’t support alpha)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    # Resize if larger than max_size while maintaining aspect ratio
    image.thumbnail(max_size, Image.Resampling.LANCZOS)

    # Save to BytesIO (in-memory buffer)
    buffer = io.BytesIO()
    image.save(buffer, "JPEG", optimize=True, quality=quality)
    buffer.seek(0)
    return buffer

# --- Upload section ---
uploaded = st.file_uploader("📂 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Original Image", use_column_width=True)

    quality = st.slider("🔧 Compression Quality", 10, 95, 85)
    max_width = st.slider("📏 Max Width (pixels)", 500, 4000, 1920)
    max_height = st.slider("📐 Max Height (pixels)", 500, 4000, 1080)

    if st.button("🚀 Compress Image"):
        compressed_buffer = compress_image(img, quality=quality, max_size=(max_width, max_height))

        st.image(Image.open(compressed_buffer), caption="Compressed Image", use_column_width=True)

        # Show size reduction info
        original_size = len(uploaded.getvalue()) / 1024
        compressed_size = compressed_buffer.getbuffer().nbytes / 1024
        reduction = 100 - (compressed_size / original_size * 100)
        st.success(
            f"📊 **Original:** {original_size:.2f} KB → **Compressed:** {compressed_size:.2f} KB "
            f"({reduction:.1f}% smaller)"
        )

        st.download_button(
            label="⬇️ Download Compressed Image",
            data=compressed_buffer,
            file_name="compressed.jpg",
            mime="image/jpeg"
        )
