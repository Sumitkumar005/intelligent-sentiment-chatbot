import React, { useRef } from 'react';
import './ImageUpload.css';
const ImageUpload = ({ onImageSelect }) => {
  const fileInputRef = useRef(null);
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        onImageSelect({
          file: file,
          preview: event.target.result,
          name: file.name
        });
      };
      reader.readAsDataURL(file);
    }
  };
  return (
    <>
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <button
        type="button"
        className="image-upload-btn"
        onClick={() => fileInputRef.current?.click()}
        title="Upload image"
      >
        📎
      </button>
    </>
  );
};
export default ImageUpload;