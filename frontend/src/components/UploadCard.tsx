export default function UploadCard() {
  return (
    <div className="mt-4 border rounded p-4">
      <p>上传纸质病历拍照图片：</p>
      <input type="file" accept="image/*" />
    </div>
  );
}
