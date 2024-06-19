function captureImage() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            const video = document.getElementById('video');
            video.srcObject = stream;
            video.play();

            const canvas = document.getElementById('canvas');
            const context = canvas.getContext('2d');

            document.getElementById('capture').addEventListener('click', () => {
                context.drawImage(video, 0, 0, canvas.width, canvas.height);
                const dataUrl = canvas.toDataURL('image/jpeg');
                document.getElementById('image').value = dataUrl;
                document.getElementById('attendance_form').submit();

                stream.getTracks().forEach(track => track.stop());
            });
        })
        .catch(err => {
            alert('Error accessing the camera: ' + err);
        });
}
