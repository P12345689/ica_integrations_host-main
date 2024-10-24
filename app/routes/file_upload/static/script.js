// Function to get URL parameter
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

// Function to copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('URL copied to clipboard');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

// Display user information
window.onload = function() {
    document.getElementById('displayTeamId').textContent = document.getElementById('teamId').value;
    document.getElementById('displayUserEmail').textContent = document.getElementById('userEmail').value;
};

// Function to handle clipboard paste
async function handlePaste(e) {
    e.preventDefault();
    const items = e.clipboardData.items;
    const previewArea = document.getElementById('previewArea');
    previewArea.innerHTML = ''; // Clear previous preview

    for (let i = 0; i < items.length; i++) {
        if (items[i].type.indexOf('image') !== -1) {
            const blob = items[i].getAsFile();
            const reader = new FileReader();
            reader.onload = function(event) {
                const img = document.createElement('img');
                img.src = event.target.result;
                img.style.maxWidth = '300px';
                img.style.maxHeight = '300px';
                previewArea.appendChild(img);
            };
            reader.readAsDataURL(blob);
            await uploadFile(blob, 'pasted_image.png');
        }
    }
}

// Function to upload file
async function uploadFile(file = null, fileName = null) {
    const key = document.getElementById('accessKey').value;
    const teamId = document.getElementById('teamId').value;
    const userEmail = document.getElementById('userEmail').value;
    const fileInput = document.getElementById('fileUpload');
    const resultDiv = document.getElementById('uploadResult');

    if (!key || !teamId || !userEmail) {
        resultDiv.innerHTML = 'Error: Access key, team ID, and user email are required';
        return;
    }

    const formData = new FormData();
    if (file) {
        formData.append('file', file, fileName);
    } else {
        formData.append('file', fileInput.files[0]);
    }
    formData.append('key', key);
    formData.append('team_id', teamId);
    formData.append('user_email', userEmail);

    try {
        const response = await fetch('/system/file_upload/upload', {
            method: 'POST',
            headers: {
                'Integrations-API-Key': 'dev-only-token'
            },
            body: formData
        });

        const data = await response.json();
        if (response.ok) {
            resultDiv.innerHTML = `File uploaded successfully: ${data.file_name} ` +
                                  `<button onclick="copyToClipboard('${data.file_url}')">Copy Full URL</button>`;
            listFiles(); // Refresh the file list
        } else {
            resultDiv.innerHTML = `Error: ${data.detail || 'File upload failed'}`;
        }
    } catch (error) {
        resultDiv.innerHTML = `Error: ${error.message}`;
    }
}

// Function to list files
async function listFiles() {
    const key = document.getElementById('accessKey').value;
    const teamId = document.getElementById('teamId').value;
    const userEmail = document.getElementById('userEmail').value;
    const fileListDiv = document.getElementById('fileList');

    if (!key || !teamId || !userEmail) {
        fileListDiv.innerHTML = 'Error: Access key, team ID, and user email are required';
        return;
    }

    try {
        const response = await fetch(`/system/file_upload/list?key=${key}&team_id=${teamId}&user_email=${userEmail}`, {
            method: 'GET',
            headers: {
                'Integrations-API-Key': 'dev-only-token'
            }
        });

        const data = await response.json();
        if (response.ok) {
            fileListDiv.innerHTML = data.files.map(file => {
                const fileUrl = `${window.location.origin}/system/file_upload/download/${file}?key=${key}&team_id=${teamId}&user_email=${userEmail}`;
                return `<div>
                    ${file}
                    <button onclick="copyToClipboard('${fileUrl}')">Copy Full URL</button>
                    <button onclick="deleteFile('${file}')">Delete</button>
                </div>`;
            }).join('');
        } else {
            fileListDiv.innerHTML = `Error: ${data.detail || 'Failed to list files'}`;
        }
    } catch (error) {
        fileListDiv.innerHTML = `Error: ${error.message}`;
    }
}

// Function to delete file
async function deleteFile(fileName) {
    const key = document.getElementById('accessKey').value;
    const teamId = document.getElementById('teamId').value;
    const userEmail = document.getElementById('userEmail').value;

    if (!key || !teamId || !userEmail) {
        alert('Error: Access key, team ID, and user email are required');
        return;
    }

    try {
        const response = await fetch(`/system/file_upload/delete/${fileName}?key=${key}&team_id=${teamId}&user_email=${userEmail}`, {
            method: 'DELETE',
            headers: {
                'Integrations-API-Key': 'dev-only-token'
            }
        });

        if (response.ok) {
            listFiles(); // Refresh the file list
        } else {
            const data = await response.json();
            alert(`Error: ${data.detail || 'Failed to delete file'}`);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Event listeners
document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    uploadFile();
});

document.getElementById('pasteButton').addEventListener('click', function() {
    document.getElementById('previewArea').innerHTML = 'Paste your screenshot here';
    document.getElementById('previewArea').focus();
});

document.addEventListener('paste', handlePaste);
